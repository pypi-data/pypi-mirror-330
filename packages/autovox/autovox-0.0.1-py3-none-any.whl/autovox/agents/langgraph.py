"""
LangGraph integration for AutoVox.

This module provides the LangGraphConnector class that bridges the voice engines with LangGraph agents.
"""

import asyncio
from asyncio import Task
import logging
from typing import Any, AsyncGenerator, Dict, List, Optional, Union, Callable, Type, cast

from pydantic import BaseModel, Field

from autovox.core.protocol import (
    ConnectionType, EngineConfig, MessageType, RealTimeVoiceEngine, 
    StreamSettings, VoiceMessage, VoiceSession
)

logger = logging.getLogger(__name__)


class VoiceSessionConfig(BaseModel):
    """Configuration for a LangGraph voice session."""
    
    # Basic voice and model settings
    voice: str = "alloy"
    model: str = "gpt-4o"
    
    # Engine-specific settings
    gemini_voice: Optional[str] = None
    gemini_model: Optional[str] = None
    
    # LangGraph specific settings
    system_prompt: str = "You are a helpful voice assistant."
    
    # WebRTC settings
    connection_type: ConnectionType = ConnectionType.WEBSOCKET
    
    # Behavior settings
    allow_interruptions: bool = True
    
    # Additional settings
    additional_settings: Dict[str, Any] = Field(default_factory=dict)
    
    def to_stream_settings(self) -> StreamSettings:
        """Convert the config to StreamSettings for the voice engine."""
        return StreamSettings(
            voice=self.voice,
            model=self.model,
            gemini_voice=self.gemini_voice or "Puck",
            gemini_model=self.gemini_model or "gemini-2.0-flash-exp",
            connection_type=self.connection_type,
            allow_interruptions=self.allow_interruptions,
            additional_settings=self.additional_settings
        )


class LangGraphVoiceSession(VoiceSession):
    """A voice session that connects a voice engine to a LangGraph agent."""
    
    def __init__(
        self,
        engine: RealTimeVoiceEngine,
        agent: Any,
        config: VoiceSessionConfig,
        on_transcription: Optional[Callable[[str], None]] = None,
        on_thinking: Optional[Callable[[str], None]] = None,
        on_response_start: Optional[Callable[[], None]] = None,
        on_response_chunk: Optional[Callable[[Union[str, bytes]], None]] = None,
        on_response_end: Optional[Callable[[], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
    ):
        """Initialize the LangGraph voice session."""
        super().__init__(
            engine=engine,
            on_transcription=on_transcription,
            on_response_start=on_response_start,
            on_response_chunk=on_response_chunk,
            on_response_end=on_response_end,
            on_error=on_error,
            on_thinking=on_thinking,
        )
        self.agent = agent
        self.config = config
        self._agent_task: Optional[Task[None]] = None
        
    async def _run_agent(self, query: str) -> None:
        """Run the LangGraph agent with the given query."""
        try:
            # Signal response start
            if self.on_response_start:
                self.on_response_start()
                
            # Format agent input
            agent_input = {
                "messages": [
                    {"role": "system", "content": self.config.system_prompt},
                    {"role": "user", "content": query}
                ]
            }
            
            # Run the agent
            result = None
            async for chunk in self.agent.astream(agent_input):
                # Update the UI with intermediate steps and thinking
                if self.on_thinking and "intermediate_steps" in chunk:
                    for step in chunk["intermediate_steps"]:
                        if step and hasattr(step, "thinking"):
                            self.on_thinking(step.thinking)
                
                # Stream the response
                if "messages" in chunk and chunk["messages"]:
                    for message in chunk["messages"]:
                        if message["role"] == "assistant" and "content" in message:
                            content = message["content"]
                            if isinstance(content, str) and self.on_response_chunk:
                                self.on_response_chunk(content)
                            result = content
            
            # Signal response end
            if self.on_response_end:
                self.on_response_end()
                
            # If needed, convert response to speech
            if result:
                await self._text_to_speech(result)
                
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            if self.on_error:
                self.on_error(f"Error running agent: {e}")
    
    async def _text_to_speech(self, text: str) -> None:
        """Convert text to speech using the voice engine."""
        try:
            # If the engine has a text_to_speech method, use it
            if hasattr(self.engine, "text_to_speech"):
                tts_message = await self.engine.text_to_speech(text)
                if tts_message.type == MessageType.AUDIO and isinstance(tts_message.content, bytes):
                    # TODO: Play the audio if needed
                    pass
        except Exception as e:
            logger.error(f"Error in text to speech: {e}")
            
    async def _handle_responses(self) -> None:
        """Handle responses from the voice engine."""
        try:
            # Create a queue to receive messages
            message_queue: asyncio.Queue[VoiceMessage] = asyncio.Queue()
            
            # Start a task to receive messages and put them in the queue
            async def receive_messages():
                try:
                    async for message in self.engine.receive_response():
                        await message_queue.put(message)
                except Exception as e:
                    logger.error(f"Error receiving messages: {e}")
                    if self.on_error:
                        self.on_error(f"Error receiving messages: {e}")
            
            # Start the receive task
            receive_task = asyncio.create_task(receive_messages())
            
            # Process messages from the queue
            while True:
                message = await message_queue.get()
                
                if message.type == MessageType.TRANSCRIPTION:
                    # Handle transcription
                    transcription = message.content
                    if isinstance(transcription, str) and self.on_transcription:
                        self.on_transcription(transcription)
                        
                        # Start the agent with the transcription
                        if self._agent_task:
                            self._agent_task.cancel()
                            try:
                                await self._agent_task
                            except asyncio.CancelledError:
                                pass
                        
                        self._agent_task = asyncio.create_task(self._run_agent(transcription))
                        
                elif message.type == MessageType.ERROR:
                    # Handle error
                    error = message.content
                    if isinstance(error, str) and self.on_error:
                        self.on_error(error)
                        
                elif message.type == MessageType.AUDIO:
                    # Pass through audio chunks
                    if self.on_response_chunk and isinstance(message.content, bytes):
                        self.on_response_chunk(message.content)
                
                elif message.type == MessageType.TEXT:
                    # Pass through text chunks
                    if isinstance(message.content, str) and self.on_response_chunk:
                        self.on_response_chunk(message.content)
                
                elif message.type == MessageType.THINKING:
                    # Handle thinking/reasoning steps
                    if isinstance(message.content, str) and self.on_thinking:
                        self.on_thinking(message.content)
                
                message_queue.task_done()
        
        except asyncio.CancelledError:
            # Task was cancelled, this is expected
            if 'receive_task' in locals():
                receive_task.cancel()
            pass
        except Exception as e:
            logger.error(f"Error handling responses: {e}")
            if self.on_error:
                self.on_error(f"Error handling responses: {e}")


class LangGraphConnector:
    """Connector for LangGraph agents to AutoVox voice engines."""
    
    def __init__(self, engine: RealTimeVoiceEngine, agent: Any):
        """Initialize the connector."""
        self.engine = engine
        self.agent = agent
        
    async def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize the voice engine."""
        await self.engine.initialize(api_key, **kwargs)
    
    @classmethod
    async def create(cls, engine_config: EngineConfig, agent: Any) -> "LangGraphConnector":
        """Create a new connector with a pre-configured engine."""
        # Create the engine based on the config
        engine_type = engine_config.engine_type.lower()
        
        if engine_type == "openai":
            from autovox.engines.openai_realtime import OpenAIRealTime
            engine = OpenAIRealTime()
        elif engine_type == "gemini":
            from autovox.engines.gemini_realtime import GeminiRealTime
            engine = GeminiRealTime()
        else:
            raise ValueError(f"Unsupported engine type: {engine_type}")
        
        # Initialize the engine if API key is provided
        if engine_config.api_key:
            await engine.initialize(engine_config.api_key, **engine_config.settings)
        
        # Create and return the connector
        return cls(engine, agent)
        
    async def start_voice_session(self, config: VoiceSessionConfig) -> LangGraphVoiceSession:
        """Start a new voice session with the provided configuration."""
        # Create the session
        session = LangGraphVoiceSession(
            engine=self.engine,
            agent=self.agent,
            config=config
        )
        
        # Initialize and start the session
        settings = config.to_stream_settings()
        await session.start(settings)
        
        return session


class SupervisorConnector(LangGraphConnector):
    """Specialized connector for LangGraph multi-agent supervisor."""
    
    def __init__(self, engine: RealTimeVoiceEngine, supervisor: Any):
        """Initialize the supervisor connector."""
        super().__init__(engine, supervisor)
        self.supervisor = supervisor
    
    @classmethod
    async def create(cls, engine_config: EngineConfig, supervisor: Any) -> "SupervisorConnector":
        """Create a new connector with a pre-configured engine."""
        base_connector = await LangGraphConnector.create(engine_config, supervisor)
        return cls(base_connector.engine, supervisor)
    
    async def start_voice_session(
        self, 
        config: VoiceSessionConfig, 
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> LangGraphVoiceSession:
        """Start a new voice session with the provided configuration."""
        # Apply any callbacks
        if callbacks is None:
            callbacks = {}
        
        # Create the session
        session = LangGraphVoiceSession(
            engine=self.engine,
            agent=self.supervisor,
            config=config,
            on_transcription=callbacks.get("on_transcription"),
            on_thinking=callbacks.get("on_thinking"),
            on_response_start=callbacks.get("on_response_start"),
            on_response_chunk=callbacks.get("on_response_chunk"),
            on_response_end=callbacks.get("on_response_end"),
            on_error=callbacks.get("on_error"),
        )
        
        # Initialize and start the session
        settings = config.to_stream_settings()
        await session.start(settings)
        
        return session 