"""
OpenAI real-time voice engine implementation using the new WebSocket-based streaming API.

This engine implements real-time bidirectional voice conversations with OpenAI's models.
"""

import asyncio
import json
import logging
from typing import Any, AsyncIterator, Dict, Optional, List, Union

import websockets
from openai import AsyncOpenAI

from autovox.core.protocol import MessageType, RealTimeVoiceEngine, StreamSettings, VoiceMessage


logger = logging.getLogger(__name__)


class OpenAIRealTime(RealTimeVoiceEngine):
    """OpenAI real-time voice engine implementation."""

    def __init__(self):
        """Initialize the OpenAI real-time voice engine."""
        self.client = None
        self.websocket = None
        self.session_id = None
        self._receive_queue = asyncio.Queue()
        self._receive_task = None
        self._initialized = False

    async def initialize(self, api_key: str, **kwargs) -> None:
        """Initialize the OpenAI client."""
        self.client = AsyncOpenAI(api_key=api_key)
        self._initialized = True

    async def start_session(self, settings: Optional[StreamSettings] = None) -> None:
        """Start a new streaming session with OpenAI."""
        if not self._initialized:
            raise RuntimeError(
                "OpenAI engine not initialized. Call initialize() first.")

        if self.websocket:
            await self.end_session()

        if not settings:
            settings = StreamSettings()

        # Create a new WebSocket connection
        uri = "wss://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {self.client.api_key}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "realtime"
        }

        self.websocket = await websockets.connect(uri, additional_headers=headers)

        # Configure the session
        await self.websocket.send(json.dumps({
            "model": settings.model,
            "voice": settings.voice,
            "stream": True,
            "input_mode": "speech",
            "output_mode": "speech",
            "settings": {
                "sampling_rate": settings.sample_rate,
                "can_interrupt": settings.allow_interruptions,
                "interruption_threshold": 500,  # ms
                "client_settings": settings.additional_settings
            }
        }))

        # Wait for confirmation
        response = await self.websocket.recv()
        session_data = json.loads(response)
        self.session_id = session_data.get("session_id")

        logger.info(f"Started OpenAI real-time session: {self.session_id}")

        # Start background task to handle incoming messages
        self._receive_task = asyncio.create_task(self._receive_messages())

    async def end_session(self) -> None:
        """End the current streaming session."""
        if self._receive_task:
            self._receive_task.cancel()
            self._receive_task = None

        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.session_id = None

    async def send_audio_chunk(self, audio_chunk: bytes) -> None:
        """Send a chunk of audio to the streaming session."""
        if not self.websocket:
            raise RuntimeError("No active session")

        # Send an audio message
        await self.websocket.send(audio_chunk)

    async def receive_response(self) -> AsyncIterator[VoiceMessage]:
        """Receive streaming responses from the model."""
        if not self.websocket:
            raise RuntimeError("No active session")

        while True:
            message = await self._receive_queue.get()
            yield message
            self._receive_queue.task_done()

    async def send_text(self, text: str, end_turn: bool = True) -> None:
        """Send text input to the model."""
        if not self.websocket:
            raise RuntimeError("No active session")

        # Send a text message
        await self.websocket.send(json.dumps({
            "type": "text",
            "content": text,
            "end_turn": end_turn
        }))

    async def interrupt(self) -> None:
        """Interrupt the current model generation."""
        if not self.websocket:
            return

        # Send an interrupt message
        await self.websocket.send(json.dumps({
            "type": "interrupt"
        }))

    async def text_to_speech(self, text: str, **kwargs) -> VoiceMessage:
        """Convert text to speech (non-streaming)."""
        if not self._initialized:
            raise RuntimeError(
                "OpenAI engine not initialized. Call initialize() first.")

        # Use the regular TTS API for non-streaming requests
        model = kwargs.get("model", "tts-1")
        voice = kwargs.get("voice", "alloy")

        response = await self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        audio_data = await response.read()

        return VoiceMessage(
            type=MessageType.AUDIO,
            content=audio_data,
            metadata={
                "model": model,
                "voice": voice,
                "format": "mp3",
            }
        )

    async def speech_to_text(self, audio: bytes, **kwargs) -> VoiceMessage:
        """Convert speech to text (non-streaming)."""
        if not self._initialized:
            raise RuntimeError(
                "OpenAI engine not initialized. Call initialize() first.")

        # Import tempfile here to avoid circular import
        import tempfile

        model = kwargs.get("model", "whisper-1")

        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
            temp_file.write(audio)
            temp_file.flush()

            with open(temp_file.name, "rb") as audio_file:
                response = await self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file
                )

        return VoiceMessage(
            type=MessageType.TRANSCRIPTION,
            content=response.text,
            metadata={
                "model": model,
            }
        )

    async def _receive_messages(self) -> None:
        """Background task to receive and process messages from the WebSocket."""
        try:
            while True:
                message = await self.websocket.recv()

                # Handle binary audio data
                if isinstance(message, bytes):
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.AUDIO,
                        content=message,
                        metadata={"format": "mp3"}
                    ))
                    continue

                # Handle JSON messages
                try:
                    data = json.loads(message)
                    message_type = data.get("type")

                    if message_type == "text":
                        # Text from the model
                        await self._receive_queue.put(VoiceMessage(
                            type=MessageType.TEXT,
                            content=data.get("content", ""),
                            metadata={
                                "turn_complete": data.get("end_turn", False)
                            }
                        ))
                    elif message_type == "error":
                        # Error message
                        await self._receive_queue.put(VoiceMessage(
                            type=MessageType.ERROR,
                            content=data.get("content", "Unknown error"),
                            metadata={}
                        ))
                    elif message_type == "transcription":
                        # Speech-to-text transcription
                        await self._receive_queue.put(VoiceMessage(
                            type=MessageType.TRANSCRIPTION,
                            content=data.get("content", ""),
                            metadata={
                                "final": data.get("final", False)
                            }
                        ))
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await self._receive_queue.put(VoiceMessage(
                        type=MessageType.ERROR,
                        content=f"Error processing message: {e}",
                        metadata={}
                    ))
        except asyncio.CancelledError:
            # Task was cancelled, this is expected
            pass
        except Exception as e:
            logger.error(f"Error in receive task: {e}")
            await self._receive_queue.put(VoiceMessage(
                type=MessageType.ERROR,
                content=f"Connection error: {e}",
                metadata={}
            ))
