"""Video transcription using Whisper."""

import subprocess
import os
import time
import threading
from pathlib import Path
from typing import Optional
from tqdm import tqdm


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
        
        # Create a cool progress bar for transcription
        pbar = tqdm(
            total=100, 
            desc="🎤 Transcribing", 
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            colour="green"
        )
        
        # Function to update progress bar while whisper is running
        stop_thread = threading.Event()
        def update_progress():
            progress = 0
            stages = ["Loading model", "Processing audio", "Detecting language", "Transcribing speech", "Generating subtitles"]
            stage_idx = 0
            
            while not stop_thread.is_set() and progress < 100:
                if progress < 95:  # Reserve the last bit for completion
                    # Update progress in steps
                    if progress < 20:
                        # Model loading stage
                        increment = 0.2
                        desc = f"🔍 {stages[0]}"
                    elif progress < 40:
                        # Processing audio
                        increment = 0.5
                        if stage_idx < 1:
                            stage_idx = 1
                            desc = f"🔊 {stages[1]}"
                    elif progress < 60:
                        # Language detection
                        increment = 1.0
                        if stage_idx < 2:
                            stage_idx = 2
                            desc = f"🌍 {stages[2]}"
                    elif progress < 90:
                        # Transcribing
                        increment = 0.3
                        if stage_idx < 3:
                            stage_idx = 3
                            desc = f"🎤 {stages[3]}"
                    else:
                        # Generating subtitles
                        increment = 0.1
                        if stage_idx < 4:
                            stage_idx = 4
                            desc = f"📝 {stages[4]}"
                    
                    progress += increment
                    pbar.n = int(progress)
                    pbar.set_description(desc)
                    pbar.refresh()
                
                time.sleep(0.1)
                
        # Start progress bar updating in a background thread
        progress_thread = threading.Thread(target=update_progress)
        progress_thread.daemon = True
        progress_thread.start()
        
        try:
            # Run whisper with verbose output
            command = [
                "whisper", 
                str(video_path),
                "--model", "small.en",  # Use small.en model for better English recognition
                "--output_format", "srt",
                "--output_dir", str(video_path.parent),
                "--verbose", "True",
            ]
            
            result = subprocess.run(
                command,
                check=True,
                text=True,
                capture_output=True,
            )
            
            # Complete the progress bar
            stop_thread.set()
            progress_thread.join(1.0)  # Wait for the thread to finish
            pbar.n = 100
            pbar.set_description("✅ Transcription complete")
            pbar.refresh()
            pbar.close()
            
        except Exception as e:
            # Make sure to stop the thread and close the progress bar on error
            stop_thread.set()
            if progress_thread.is_alive():
                progress_thread.join(1.0)
            pbar.set_description("❌ Transcription failed")
            pbar.close()
            raise e
        
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