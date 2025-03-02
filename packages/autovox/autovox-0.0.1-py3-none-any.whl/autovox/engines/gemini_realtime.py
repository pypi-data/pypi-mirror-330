"""
Gemini Multimodal Live API implementation.

This engine implements real-time bidirectional voice conversations with Google's Gemini models
using the Multimodal Live API.
"""

import asyncio
import logging
from typing import Any, AsyncGenerator, AsyncIterator, Dict, Optional, List, Union, Coroutine

# Ignore type checking for the google.genai module as it lacks type stubs
from google import genai  # type: ignore

from autovox.core.protocol import MessageType, RealTimeVoiceEngine, StreamSettings, VoiceMessage


logger = logging.getLogger(__name__)


class GeminiRealTime(RealTimeVoiceEngine):
    """Gemini real-time voice engine implementation."""

    def __init__(self):
        """Initialize the Gemini real-time voice engine."""
        self.client = None
        self.session = None
        self._receive_queue = asyncio.Queue()
        self._receive_task = None
        self._initialized = False
        self._api_version = "v1alpha"  # Required for Multimodal Live API
        self._session_manager = None
        self._session_active = False

    async def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize the Gemini client.

        Args:
            api_key: The Gemini API key
            **kwargs: Additional parameters
                - api_version: API version to use (default: v1alpha)
        """
        try:
            self.client = genai.Client(
                api_key=api_key,
                http_options={'api_version': self._api_version}
            )
            self._initialized = True
            logger.info(
                f"Initialized Gemini client with API version {self._api_version}")

            # Apply additional settings from kwargs
            if "api_version" in kwargs:
                self._api_version = kwargs["api_version"]
                logger.info(f"Updated API version to {self._api_version}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise RuntimeError(
                f"Failed to initialize Gemini client: {e}") from e

    async def start_session(self, settings: Optional[StreamSettings] = None) -> None:
        """Start a new streaming session with Gemini.

        This creates a WebSocket connection with the Gemini Multimodal Live API.

        Args:
            settings: Stream settings for the session
        """
        if not self._initialized:
            error_msg = "Gemini engine not initialized. Call initialize() first."
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        if self.session:
            logger.info("Ending existing session before starting a new one")
            await self.end_session()

        if not settings:
            settings = StreamSettings()

        # Configure the session
        config = {
            "response_modalities": ["TEXT", "AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": settings.gemini_voice
                    }
                }
            }
        }

        # Add system instruction if provided
        if "system_instruction" in settings.additional_settings:
            config["systemInstruction"] = settings.additional_settings["system_instruction"]

        # Add tools if provided
        if "tools" in settings.additional_settings:
            config["tools"] = settings.additional_settings["tools"]

        logger.info(
            f"Starting Gemini session with model {settings.gemini_model}")
        logger.debug(f"Session config: {config}")

        try:
            # Create the session using context manager properly
            self._session_manager = self.client.aio.live.connect(
                model=settings.gemini_model,
                config=config
            )

            # Enter the async context manager
            self.session = await self._session_manager.__aenter__()
            self._session_active = True

            logger.info(
                f"Started Gemini real-time session with model: {settings.gemini_model}")

            # Start background task to handle incoming messages
            self._receive_task = asyncio.create_task(self._receive_messages())
            logger.debug("Started background receive task")
        except Exception as e:
            logger.error(f"Failed to start Gemini session: {e}")
            # Clean up if session creation fails
            if self._session_manager:
                try:
                    await self._session_manager.__aexit__(type(e), e, None)
                    logger.info(
                        "Cleaned up session manager after session start failure")
                except Exception as cleanup_error:
                    logger.error(
                        f"Error during session cleanup: {cleanup_error}")

            self._session_manager = None
            self.session = None
            self._session_active = False

            # Put error in the queue for any listeners
            await self._receive_queue.put(VoiceMessage(
                type=MessageType.ERROR,
                content=f"Failed to start Gemini session: {e}",
                metadata={}
            ))

            raise RuntimeError(f"Failed to start Gemini session: {e}")

    async def end_session(self) -> None:
        """End the current streaming session."""
        logger.info("Ending Gemini session")

        # Cancel the receive task first
        if self._receive_task:
            logger.debug("Cancelling receive task")
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass  # Expected when cancelling
            except Exception as e:
                logger.error(f"Error while cancelling receive task: {e}")
            finally:
                self._receive_task = None

        # Close the session
        if self._session_active and self._session_manager:
            try:
                logger.debug("Exiting session manager context")
                await self._session_manager.__aexit__(None, None, None)
                logger.info("Successfully closed Gemini session")
            except Exception as e:
                logger.error(f"Error closing Gemini session: {e}")

        self.session = None
        self._session_manager = None
        self._session_active = False

    async def send_audio_chunk(self, audio_chunk: bytes) -> None:
        """Send a chunk of audio to the streaming session.

        Args:
            audio_chunk: Raw 16 bit PCM audio at 16kHz little-endian
        """
        if not self.session or not self._session_active:
            logger.error("No active session for send_audio_chunk")
            await self._receive_queue.put(VoiceMessage(
                type=MessageType.ERROR,
                content="No active session",
                metadata={}
            ))
            return

        try:
            # Send an audio message as realtime input
            logger.debug(f"Sending audio chunk: {len(audio_chunk)} bytes")
            await self.session.send(input=audio_chunk)
        except Exception as e:
            logger.error(f"Error sending audio to Gemini: {e}")
            await self._receive_queue.put(VoiceMessage(
                type=MessageType.ERROR,
                content=f"Failed to send audio: {e}",
                metadata={}
            ))

    async def receive_response(self) -> AsyncIterator[VoiceMessage]:
        """Receive streaming responses from the model.

        Returns:
            An async iterator that yields VoiceMessage objects
        """
        if not self.session:
            raise RuntimeError("No active session")

        while True:
            message = await self._receive_queue.get()
            yield message
            self._receive_queue.task_done()

    async def send_text(self, text: str, end_turn: bool = True) -> None:
        """Send text input to the model.

        Args:
            text: The text to send
            end_turn: Whether this is the end of the user's turn
        """
        if not self.session or not self._session_active:
            logger.error("No active session for send_text")
            await self._receive_queue.put(VoiceMessage(
                type=MessageType.ERROR,
                content="No active session",
                metadata={}
            ))
            return

        try:
            logger.debug(f"Sending text: '{text}', end_turn={end_turn}")
            # Send the text with end_of_turn flag
            await self.session.send(input=text, end_of_turn=end_turn)
        except Exception as e:
            logger.error(f"Error sending text to Gemini: {e}")
            await self._receive_queue.put(VoiceMessage(
                type=MessageType.ERROR,
                content=f"Failed to send text: {e}",
                metadata={}
            ))

    async def interrupt(self) -> None:
        """Interrupt the current model generation."""
        logger.info("Interrupting Gemini generation")
        if not self.session or not self._session_active:
            logger.warning("No active session to interrupt")
            return

        try:
            # Send an interrupt by starting a new turn with fresh input
            # This is the recommended way to interrupt in Gemini
            await self.session.send(input=" ", end_of_turn=True)
            logger.info("Sent interrupt signal to Gemini")
        except Exception as e:
            logger.error(f"Error interrupting Gemini: {e}")
            await self._receive_queue.put(VoiceMessage(
                type=MessageType.ERROR,
                content=f"Failed to interrupt: {e}",
                metadata={}
            ))

    async def text_to_speech(self, text: str, **kwargs) -> VoiceMessage:
        """Convert text to speech (non-streaming).

        Creates a temporary session to convert text to speech.

        Args:
            text: The text to convert
            **kwargs: Additional parameters
                - model: The model to use
                - voice: The voice to use

        Returns:
            A VoiceMessage containing the audio
        """
        # Gemini doesn't have a dedicated TTS API that's separate from the conversation
        # For non-streaming TTS, we'll create a temporary session
        if not self._initialized:
            error_msg = "Gemini engine not initialized. Call initialize() first."
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        temp_settings = StreamSettings(
            gemini_model=kwargs.get("model", "gemini-2.0-flash-exp"),
            gemini_voice=kwargs.get("voice", "Puck")
        )

        temp_config = {
            "response_modalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": temp_settings.gemini_voice
                    }
                }
            }
        }

        logger.info(
            f"Creating temporary TTS session with voice {temp_settings.gemini_voice}")

        session_mgr = None
        try:
            session_mgr = self.client.aio.live.connect(
                model=temp_settings.gemini_model,
                config=temp_config
            )
            async with session_mgr as session:
                logger.debug(f"Sending text to TTS: '{text}'")
                await session.send(input=text, end_of_turn=True)

                audio_chunks = []

                async for response in session.receive():
                    if hasattr(response, "audio") and response.audio:
                        audio_chunks.append(response.audio)

                # Combine all audio chunks
                combined_audio = b"".join(audio_chunks)

                if not combined_audio:
                    logger.warning("No audio generated from TTS")
                    return VoiceMessage(
                        type=MessageType.ERROR,
                        content="No audio generated",
                        metadata={}
                    )

                logger.info(
                    f"Generated {len(combined_audio)} bytes of audio from TTS")
                return VoiceMessage(
                    type=MessageType.AUDIO,
                    content=combined_audio,
                    metadata={
                        "model": temp_settings.gemini_model,
                        "voice": temp_settings.gemini_voice,
                        "format": "wav",  # Gemini returns WAV format
                    }
                )
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            return VoiceMessage(
                type=MessageType.ERROR,
                content=f"Failed to generate speech: {e}",
                metadata={}
            )

    async def speech_to_text(self, audio: bytes, **kwargs) -> VoiceMessage:
        """Convert speech to text (non-streaming).

        Creates a temporary session to convert speech to text.

        Args:
            audio: Raw 16 bit PCM audio at 16kHz little-endian
            **kwargs: Additional parameters
                - model: The model to use

        Returns:
            A VoiceMessage containing the transcription
        """
        # For non-streaming STT, we'll create a temporary session
        if not self._initialized:
            error_msg = "Gemini engine not initialized. Call initialize() first."
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        temp_settings = StreamSettings(
            gemini_model=kwargs.get("model", "gemini-2.0-flash-exp"),
        )

        temp_config = {
            "response_modalities": ["TEXT"],
        }

        logger.info(
            f"Creating temporary STT session with {len(audio)} bytes of audio")

        session_mgr = None
        try:
            session_mgr = self.client.aio.live.connect(
                model=temp_settings.gemini_model,
                config=temp_config
            )
            async with session_mgr as session:
                logger.debug(f"Sending audio to STT, {len(audio)} bytes")
                await session.send(input=audio, end_of_turn=True)

                transcription = ""

                async for response in session.receive():
                    if response.text:
                        transcription += response.text

                logger.info(f"Transcription result: '{transcription}'")
                return VoiceMessage(
                    type=MessageType.TRANSCRIPTION,
                    content=transcription,
                    metadata={
                        "model": temp_settings.gemini_model,
                    }
                )
        except Exception as e:
            logger.error(f"Error in speech_to_text: {e}")
            return VoiceMessage(
                type=MessageType.ERROR,
                content=f"Failed to transcribe speech: {e}",
                metadata={}
            )

    async def _receive_messages(self) -> None:
        """Background task to receive and process messages from the Gemini session."""
        logger.info("Starting message receive loop")
        try:
            async for response in self.session.receive():
                # Log the response
                logger.debug(f"Received response from Gemini: {response}")
                
                # Handle info messages
                if hasattr(response, "type") and response.type == "info":
                    logger.info(f"Received info from Gemini: {response.text}")
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.TEXT,
                        content=response.text,
                        metadata={"info": True}
                    ))

                # Handle text responses
                if hasattr(response, "text") and response.text is not None:
                    logger.debug(
                        f"Received text: '{response.text[:50]}...' (truncated)")
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.TEXT,
                        content=response.text,
                        metadata={
                            "turn_complete": getattr(response, "end_of_turn", False),
                        }
                    ))

                # Handle audio responses
                if hasattr(response, "audio") and response.audio:
                    logger.debug(
                        f"Received audio: {len(response.audio)} bytes")
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.AUDIO,
                        content=response.audio,
                        metadata={
                            "format": "wav",  # Gemini returns WAV format
                            "turn_complete": getattr(response, "end_of_turn", False),
                        }
                    ))

                # Handle transcriptions
                if hasattr(response, "transcription") and response.transcription:
                    logger.debug(
                        f"Received transcription: '{response.transcription}'")
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.TRANSCRIPTION,
                        content=response.transcription,
                        metadata={
                            "final": getattr(response, "is_final", False),
                        }
                    ))

                # Handle interrupted flag
                if hasattr(response, "interrupted") and response.interrupted:
                    logger.info("Generation was interrupted")
                    # Use MessageType.TEXT instead of INFO which isn't available
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.TEXT,
                        content="Generation interrupted",
                        metadata={
                            "interrupted": True,
                        }
                    ))

                # Handle tool calls (function calling)
                if hasattr(response, "tool_calls") and response.tool_calls:
                    tool_calls = response.tool_calls
                    logger.info(f"Received tool calls: {tool_calls}")
                    # Pass through tool calls as text for now
                    tool_calls_text = f"Function call requested: {tool_calls}"
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.TEXT,
                        content=tool_calls_text,
                        metadata={
                            "tool_calls": tool_calls,
                        }
                    ))

                # Handle errors
                if hasattr(response, "error") and response.error:
                    logger.error(
                        f"Received error from Gemini: {response.error}")
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.ERROR,
                        content=str(response.error),
                        metadata={}
                    ))

        except asyncio.CancelledError:
            # Task was cancelled, this is expected
            logger.info("Receive task was cancelled")
        except Exception as e:
            logger.error(f"Error in receive task: {e}")
            await self._receive_queue.put(VoiceMessage(
                type=MessageType.ERROR,
                content=f"Connection error: {e}",
                metadata={}
            ))
