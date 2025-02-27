"""Nakplae - Video transcription and translation tool."""

__version__ = "1.1.3"

# Public API exports
from .transcribe import transcribe_video  # noqa: F401
from .translate import translate_srt  # noqa: F401
from .__main__ import main  # noqa: F401
