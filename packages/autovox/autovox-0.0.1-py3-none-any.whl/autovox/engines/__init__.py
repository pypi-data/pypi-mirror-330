"""
Real-time voice engines for AutoVox.

This module provides real-time voice engines for different providers:
- OpenAI: Uses OpenAI's real-time WebSocket-based API
- Gemini: Uses Google's Gemini Multimodal Live API
"""

from autovox.engines.openai_realtime import OpenAIRealTime
from autovox.engines.gemini_realtime import GeminiRealTime

__all__ = [
    "OpenAIRealTime",
    "GeminiRealTime",
]
