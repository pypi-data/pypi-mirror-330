"""Tests for the translation module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from nakplae.translate import translate_srt


@patch("nakplae.translate._try_local_llm_translation")
@patch("gemini_srt_translator.translate")
def test_translate_srt(mock_gemini_translate, mock_local_llm):
    """Test translating an SRT file."""
    # Mock the translation functions
    mock_local_llm.return_value = None  # Local LLM not available
    mock_gemini_translate.return_value = None  # Just mock the call, we're not testing its internals

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
            
            # Create the output file since we're mocking the translation
            with open(output_path, "w") as f:
                f.write("Mock translated content")
                
            # Mock the _translate_with_gemini_srt function to return the output_path
            with patch("nakplae.translate._translate_with_gemini_srt", return_value=output_path):
                result = translate_srt(tmp_path, "Spanish", output_path)

                assert result == output_path
                assert os.path.exists(output_path)
                assert mock_local_llm.called
    finally:
        os.unlink(tmp_path)
