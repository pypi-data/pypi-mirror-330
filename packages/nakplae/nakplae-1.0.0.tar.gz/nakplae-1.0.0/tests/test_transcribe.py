"""Tests for the transcription module."""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from nakplae.transcribe import transcribe_video


def test_transcribe_video_file_not_found():
    """Test transcribe_video with a non-existent file."""
    with pytest.raises(FileNotFoundError):
        transcribe_video("/path/to/nonexistent/video.mp4")


@patch("subprocess.run")
@patch("os.rename")
@patch("pathlib.Path.exists")
def test_transcribe_video_success(mock_exists, mock_rename, mock_run):
    """Test successful video transcription."""
    # Mock file existence checks
    mock_exists.side_effect = lambda x: True

    # Create mock for subprocess.run
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_run.return_value = mock_process

    # Test with default output path
    result = transcribe_video("/path/to/video.mp4")
    assert result == "/path/to/video.srt"

    # Verify whisper was called with correct parameters
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert "whisper" in args
    assert "/path/to/video.mp4" in args
    assert "--output_format" in args
    assert "srt" in args

    # Verify no rename was performed (using default output path)
    mock_rename.assert_not_called()


@patch("subprocess.run")
@patch("os.rename")
@patch("pathlib.Path.exists")
def test_transcribe_video_custom_output(mock_exists, mock_rename, mock_run):
    """Test transcription with custom output path."""
    # Mock file existence checks
    mock_exists.side_effect = lambda x: True

    # Create mock for subprocess.run
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_run.return_value = mock_process

    # Test with custom output path
    result = transcribe_video("/path/to/video.mp4", "/custom/output.srt")
    assert result == "/custom/output.srt"

    # Verify whisper was called
    mock_run.assert_called_once()

    # Verify rename was performed to move to custom location
    mock_rename.assert_called_once()
