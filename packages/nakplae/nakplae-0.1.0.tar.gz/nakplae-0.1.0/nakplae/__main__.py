"""Command-line interface for Nakplae."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .transcribe import transcribe_video
from .translate import translate_srt


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Nakplae - Transcribe and translate video subtitles"
    )
    
    parser.add_argument(
        "video_file",
        help="Path to the video file to transcribe",
    )
    
    parser.add_argument(
        "--lang",
        "-l",
        default="Thai",
        help="Target language for translation (default: Thai)",
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output directory for the transcription and translation files",
    )
    
    parser.add_argument(
        "--transcribe-only",
        action="store_true",
        help="Only transcribe the video, do not translate",
    )
    
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Run the main program."""
    parsed_args = parse_args(args)
    video_path = Path(parsed_args.video_file)
    
    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}", file=sys.stderr)
        return 1
    
    output_dir = parsed_args.output
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        srt_path = output_dir / f"{video_path.stem}.srt"
    else:
        srt_path = None
    
    try:
        # Step 1: Transcribe the video to SRT
        print(f"Transcribing {video_path}...")
        srt_file = transcribe_video(str(video_path), str(srt_path) if srt_path else None)
        print(f"Transcription saved to {srt_file}")
        
        # Step 2: Translate the SRT if requested
        if not parsed_args.transcribe_only:
            print(f"Translating to {parsed_args.lang}...")
            if output_dir:
                translated_srt = output_dir / f"{video_path.stem}_{parsed_args.lang}.srt"
            else:
                translated_srt = None
            
            translated_file = translate_srt(
                srt_file,
                parsed_args.lang,
                str(translated_srt) if translated_srt else None
            )
            print(f"Translation saved to {translated_file}")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())