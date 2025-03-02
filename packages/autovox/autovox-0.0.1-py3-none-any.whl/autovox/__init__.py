"""
AutoVox: Voice Connector for Real-time LLM Agent Voice Interfaces.

This package enables real-time bidirectional voice conversations with
LLM models through WebSocket-based APIs. It supports OpenAI and Gemini models.
"""

__version__ = "0.1.0"

# Core protocol
from autovox.core.protocol import (
    MessageType,
    VoiceMessage,
    RealTimeVoiceEngine,
    StreamSettings,
    VoiceSession
)

# Real-time voice engines
from autovox.engines.openai_realtime import OpenAIRealTime
from autovox.engines.gemini_realtime import GeminiRealTime

__all__ = [
    # Version
    "__version__",

    # Core protocol
    "MessageType",
    "VoiceMessage",
    "RealTimeVoiceEngine",
    "StreamSettings",
    "VoiceSession",

    # Real-time voice engines
    "OpenAIRealTime",
    "GeminiRealTime",
]
