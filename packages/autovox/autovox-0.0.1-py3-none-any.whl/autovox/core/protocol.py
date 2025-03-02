"""
Core protocol definitions for AutoVox.

This module defines the interfaces and protocols for real-time voice engines to connect with LangGraph agents.
"""

from enum import Enum
from typing import Any, AsyncIterator, Dict, Optional, Union, Protocol, List, Callable, TypeVar, AsyncGenerator, cast
import asyncio

from pydantic import BaseModel, Field


T = TypeVar('T')


class ConnectionType(Enum):
    """Types of connections that can be used with voice engines."""
    WEBSOCKET = "websocket"  # Traditional WebSocket connection
    WEBRTC = "webrtc"        # WebRTC peer connection
    HTTP = "http"            # HTTP-based connection (non-streaming)


class MessageType(Enum):
    """Types of messages that can be exchanged between voice engines and agents."""
    TEXT = "text"
    AUDIO = "audio"
    TRANSCRIPTION = "transcription"
    ERROR = "error"
    INFO = "info"             # Added for informational messages
    THINKING = "thinking"     # Added for agent reasoning steps
    TOOL_CALL = "tool_call"   # Added for function/tool calls
    TOOL_RESULT = "tool_result" # Added for function/tool results


class VoiceMessage(BaseModel):
    """A message exchanged between voice engines and agents."""
    type: MessageType
    content: Union[str, bytes, Dict[str, Any]]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StreamSettings(BaseModel):
    """Settings for real-time streaming voice engines."""
    # Connection settings
    connection_type: ConnectionType = ConnectionType.WEBSOCKET
    
    # Audio sampling and encoding settings
    sample_rate: int = 16000  # 16kHz for input
    output_sample_rate: int = 24000  # 24kHz for output (Gemini uses this)
    bit_depth: int = 16  # 16-bit PCM
    channels: int = 1  # Mono audio
    
    # Voice settings
    voice: str = "alloy"  # Default voice (OpenAI)
    gemini_voice: str = "Puck"  # Default Gemini voice
    
    # Model settings
    model: str = "gpt-4o"  # Default OpenAI model
    gemini_model: str = "gemini-2.0-flash-exp"  # Default Gemini model
    
    # WebRTC settings
    ice_servers: List[Dict[str, Any]] = Field(default_factory=lambda: [
        {"urls": ["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"]}
    ])
    
    # Behavior settings
    allow_interruptions: bool = True  # Whether to allow interrupting the model
    
    # Additional settings
    additional_settings: Dict[str, Any] = Field(default_factory=dict)


class EngineConfig(BaseModel):
    """Pre-configured engine settings."""
    engine_type: str  # "openai", "gemini", etc.
    api_key: Optional[str] = None
    connection_type: ConnectionType = ConnectionType.WEBSOCKET
    settings: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        protected_namespaces = ()


class RealTimeVoiceEngine(Protocol):
    """Protocol for real-time voice engines."""
    
    async def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize the voice engine with the given API key."""
        ...
    
    async def start_session(self, settings: Optional[StreamSettings] = None) -> None:
        """Start a new streaming session."""
        ...
    
    async def end_session(self) -> None:
        """End the current streaming session."""
        ...
    
    async def send_audio_chunk(self, audio_chunk: bytes) -> None:
        """Send a chunk of audio to the streaming session."""
        ...
    
    async def receive_response(self) -> AsyncIterator[VoiceMessage]:
        """Receive streaming responses from the model.
        
        Returns:
            An async iterator that yields VoiceMessage objects.
        """
        ...
    
    async def send_text(self, text: str, end_turn: bool = True) -> None:
        """Send text input to the model."""
        ...
    
    async def interrupt(self) -> None:
        """Interrupt the current model generation."""
        ...
    
    async def text_to_speech(self, text: str, **kwargs) -> VoiceMessage:
        """Convert text to speech (non-streaming)."""
        ...
    
    async def speech_to_text(self, audio: bytes, **kwargs) -> VoiceMessage:
        """Convert speech to text (non-streaming)."""
        ...
    
    @classmethod
    async def create_from_config(cls, config: EngineConfig) -> "RealTimeVoiceEngine":
        """Create a new engine instance from a configuration."""
        engine = cls()
        if config.api_key:
            await engine.initialize(config.api_key, **config.settings)
        return engine


class WebRTCVoiceEngine(RealTimeVoiceEngine, Protocol):
    """Protocol extending RealTimeVoiceEngine for WebRTC-specific features."""
    
    async def create_offer(self) -> str:
        """Create a WebRTC SDP offer."""
        ...
    
    async def set_answer(self, answer: str) -> None:
        """Set the WebRTC SDP answer."""
        ...
    
    async def handle_ice_candidate(self, candidate: Dict[str, Any]) -> None:
        """Handle an ICE candidate from the peer."""
        ...
    
    async def get_ephemeral_key(self) -> str:
        """Get an ephemeral API key for client-side use."""
        ...


class VoiceSession:
    """A session for real-time voice interaction with an AI agent."""
    
    def __init__(self, 
                 engine: RealTimeVoiceEngine,
                 on_transcription: Optional[Callable[[str], None]] = None,
                 on_response_start: Optional[Callable[[], None]] = None,
                 on_response_chunk: Optional[Callable[[Union[str, bytes]], None]] = None,
                 on_response_end: Optional[Callable[[], None]] = None,
                 on_error: Optional[Callable[[str], None]] = None,
                 on_thinking: Optional[Callable[[str], None]] = None):
        """Initialize a voice session.
        
        Args:
            engine: The real-time voice engine to use.
            on_transcription: Callback when transcription is received.
            on_response_start: Callback when model starts responding.
            on_response_chunk: Callback for each chunk of the response.
            on_response_end: Callback when the model finishes responding.
            on_error: Callback when an error occurs.
            on_thinking: Callback when agent thinking/reasoning is available.
        """
        self.engine = engine
        self.on_transcription = on_transcription
        self.on_response_start = on_response_start
        self.on_response_chunk = on_response_chunk
        self.on_response_end = on_response_end
        self.on_error = on_error
        self.on_thinking = on_thinking
        self._session_active = False
        self._response_task: Optional[asyncio.Task] = None
    
    async def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize the voice engine."""
        await self.engine.initialize(api_key, **kwargs)
    
    async def start(self, settings: Optional[StreamSettings] = None) -> None:
        """Start the voice session."""
        if self._session_active:
            return
        
        await self.engine.start_session(settings)
        self._session_active = True
        
        # Start background task to handle responses
        self._response_task = asyncio.create_task(self._handle_responses())
    
    async def stop(self) -> None:
        """Stop the voice session."""
        if not self._session_active:
            return
        
        if self._response_task:
            self._response_task.cancel()
            self._response_task = None
        
        await self.engine.end_session()
        self._session_active = False
    
    async def send_audio(self, audio: bytes) -> None:
        """Send audio data to the session."""
        if not self._session_active:
            raise RuntimeError("Session not active")
        
        await self.engine.send_audio_chunk(audio)
    
    async def send_text(self, text: str, end_turn: bool = True) -> None:
        """Send text to the session."""
        if not self._session_active:
            raise RuntimeError("Session not active")
        
        await self.engine.send_text(text, end_turn)
    
    async def interrupt(self) -> None:
        """Interrupt the current model response."""
        if not self._session_active:
            return
        
        await self.engine.interrupt()
    
    async def _handle_responses(self) -> None:
        """Background task to handle incoming responses."""
        try:
            started = False
            async for message in self.engine.receive_response():
                if not started and message.type not in [MessageType.ERROR, MessageType.THINKING, MessageType.INFO] and self.on_response_start:
                    self.on_response_start()
                    started = True
                
                if message.type == MessageType.TEXT:
                    if self.on_response_chunk and isinstance(message.content, str):
                        self.on_response_chunk(message.content)
                elif message.type == MessageType.AUDIO:
                    if self.on_response_chunk and isinstance(message.content, bytes):
                        self.on_response_chunk(message.content)
                elif message.type == MessageType.TRANSCRIPTION:
                    if self.on_transcription and isinstance(message.content, str):
                        self.on_transcription(message.content)
                elif message.type == MessageType.ERROR:
                    if self.on_error and isinstance(message.content, str):
                        self.on_error(message.content)
                elif message.type == MessageType.THINKING:
                    if self.on_thinking and isinstance(message.content, str):
                        self.on_thinking(message.content)
                
                if message.metadata.get("turn_complete", False):
                    started = False
                    if self.on_response_end:
                        self.on_response_end()
        except asyncio.CancelledError:
            # Session was stopped
            pass
        except Exception as e:
            if self.on_error:
                self.on_error(str(e)) 