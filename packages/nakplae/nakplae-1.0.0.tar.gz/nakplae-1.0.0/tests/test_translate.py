"""Tests for the translation module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from nakplae.translate import _parse_srt, _format_srt, translate_srt


def test_parse_srt():
    """Test parsing an SRT file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False) as tmp:
        tmp.write(
            "1\n"
            "00:00:01,000 --> 00:00:04,000\n"
            "This is a test subtitle.\n\n"
            "2\n"
            "00:00:05,000 --> 00:00:08,000\n"
            "This is another test.\n"
            "With multiple lines.\n"
        )
        tmp_path = tmp.name

    try:
        subtitles = _parse_srt(tmp_path)
        assert len(subtitles) == 2
        assert subtitles[0]["index"] == 1
        assert subtitles[0]["timestamp"] == "00:00:01,000 --> 00:00:04,000"
        assert subtitles[0]["text"] == "This is a test subtitle."
        assert subtitles[1]["index"] == 2
        assert subtitles[1]["timestamp"] == "00:00:05,000 --> 00:00:08,000"
        assert subtitles[1]["text"] == "This is another test.\nWith multiple lines."
    finally:
        os.unlink(tmp_path)


def test_format_srt():
    """Test formatting subtitles back to SRT."""
    subtitles = [
        {
            "index": 1,
            "timestamp": "00:00:01,000 --> 00:00:04,000",
            "text": "This is a test subtitle.",
        },
        {
            "index": 2,
            "timestamp": "00:00:05,000 --> 00:00:08,000",
            "text": "This is another test.\nWith multiple lines.",
        },
    ]

    formatted = _format_srt(subtitles)
    expected = (
        "1\n"
        "00:00:01,000 --> 00:00:04,000\n"
        "This is a test subtitle.\n\n"
        "2\n"
        "00:00:05,000 --> 00:00:08,000\n"
        "This is another test.\n"
        "With multiple lines."
    )

    assert formatted == expected


@patch("nakplae.translate._try_local_llm_translation")
@patch("nakplae.translate._translate_with_gemini")
def test_translate_srt(mock_gemini, mock_local_llm):
    """Test translating an SRT file."""
    # Mock the translation functions
    mock_local_llm.return_value = None  # Local LLM not available
    mock_gemini.return_value = "Translated text"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".srt", delete=False) as tmp:
        tmp.write(
            "1\n"
            "00:00:01,000 --> 00:00:04,000\n"
            "This is a test subtitle.\n\n"
            "2\n"
            "00:00:05,000 --> 00:00:08,000\n"
            "This is another test.\n"
        )
        tmp_path = tmp.name

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "output.srt")
            result = translate_srt(tmp_path, "Spanish", output_path)

            assert result == output_path
            assert os.path.exists(output_path)

            # Verify gemini was called twice (once for each subtitle)
            assert mock_gemini.call_count == 2

            # Check the content of the output file
            with open(output_path, "r") as f:
                content = f.read()
                assert "Translated text" in content
    finally:
        os.unlink(tmp_path)
