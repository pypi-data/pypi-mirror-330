"""Video transcription using Whisper."""

import subprocess
import os
from pathlib import Path
from typing import Optional


def transcribe_video(video_path: str, output_path: Optional[str] = None) -> str:
    """
    Transcribe a video file to SRT subtitles using Whisper.
    
    Args:
        video_path: Path to the video file
        output_path: Optional path to save the SRT file. If not provided,
                    saves to the same directory as the video with .srt extension
    
    Returns:
        Path to the created SRT file
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    if output_path is None:
        output_path = video_path.with_suffix(".srt")
    
    try:
        # Run whisper CLI to transcribe the video
        print(f"Starting Whisper transcription of {video_path}...")
        
        # Run whisper with verbose output
        command = [
            "whisper", 
            str(video_path),
            "--model", "small.en",  # Use small.en model for better English recognition
            "--output_format", "srt",
            "--output_dir", str(video_path.parent),
            "--verbose", "True",
        ]
        print(f"Running command: {' '.join(command)}")
        
        result = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
        )
        
        print(f"Whisper stdout: {result.stdout}")
        print(f"Whisper stderr: {result.stderr}")
        
        # Whisper creates the output filename by appending .srt to the input basename
        expected_output = video_path.with_suffix("").with_suffix(".srt")
        
        if not expected_output.exists():
            raise RuntimeError(f"Whisper did not create expected output file: {expected_output}")
        
        # If custom output path was specified, move the file
        if str(expected_output) != str(output_path):
            os.rename(expected_output, output_path)
        
        return str(output_path)
    
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Whisper transcription failed: {e.stderr}")