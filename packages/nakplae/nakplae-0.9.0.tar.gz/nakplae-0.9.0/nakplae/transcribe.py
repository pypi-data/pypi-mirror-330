"""Video transcription using Whisper."""

import subprocess
import os
import sys
import platform
from pathlib import Path
from typing import Optional

# For GPU detection
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

# Check if we're on Windows with a non-Unicode terminal
if platform.system() == "Windows":
    IS_UNICODE_TERMINAL = False
    try:
        IS_UNICODE_TERMINAL = sys.stdout.encoding.lower() == 'utf-8'
    except:
        pass
else:
    # Assume Unix-based systems support Unicode
    IS_UNICODE_TERMINAL = True


def transcribe_video(video_path: str, output_path: Optional[str] = None, model: str = "small") -> str:
    """
    Transcribe a video file to SRT subtitles using Whisper.
    
    Args:
        video_path: Path to the video file
        output_path: Optional path to save the SRT file. If not provided,
                    saves to the same directory as the video with .srt extension
        model: Whisper model to use. Options:
               - Language agnostic: tiny, base, small, medium, large
               - English-specific: tiny.en, base.en, small.en, medium.en
               Smaller models are faster but less accurate. 
               .en models are faster but only work well with English content.
    
    Returns:
        Path to the created SRT file
    """
    video_path = Path(video_path)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    if output_path is None:
        output_path = video_path.with_suffix(".srt")
    
    try:
        print(f"Starting Whisper transcription of {video_path}...")
        
        # Determine if GPU is available and set device
        device = "cpu"
        if HAS_TORCH:
            if torch.cuda.is_available():
                device = "cuda"
            elif platform.system() == "Darwin" and hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                # For Apple Silicon GPU
                device = "mps"
        
        if IS_UNICODE_TERMINAL:
            print(f"🖥️ Using device: {device}")
        else:
            print(f"Using device: {device}")
        
        # Run whisper with standard settings, ensuring GPU is used when available
        command = [
            "whisper", 
            str(video_path),
            "--model", model,       # Use specified model (default: small)
            "--output_format", "srt",
            "--output_dir", str(video_path.parent),
            "--device", device,     # Use GPU when available
            "--verbose", "True",
            "--fp16", "True",       # Enable fp16 for faster GPU processing
        ]
        
        print(f"Running whisper command: {' '.join(command)}")
        print("----------- Actual whisper output below -----------")
        
        # Run whisper without capturing output so user can see real progress
        result = subprocess.run(
            command,
            check=True,
            timeout=1800  # 30 minute timeout
        )
        
        print("----------- Whisper output end -----------")
        if IS_UNICODE_TERMINAL:
            print("✅ Transcription complete")
        else:
            print(">> Transcription complete")
        
        # Whisper creates the output filename by appending .srt to the input basename
        expected_output = video_path.with_suffix("").with_suffix(".srt")
        
        if not expected_output.exists():
            raise RuntimeError(f"Whisper did not create expected output file: {expected_output}")
        
        # If custom output path was specified, move the file
        if str(expected_output) != str(output_path):
            os.rename(expected_output, output_path)
        
        return str(output_path)
    
    except subprocess.CalledProcessError as e:
        print(f"Whisper transcription failed")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error details: {e.stderr}")
        raise RuntimeError(f"Whisper transcription failed")
    except subprocess.TimeoutExpired as e:
        print(f"Whisper process timed out after {e.timeout} seconds")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error details: {e.stderr}")
        raise RuntimeError(f"Whisper transcription timed out after {e.timeout} seconds")
    except Exception as e:
        print(f"Unexpected error during transcription: {type(e).__name__}: {e}")
        raise