"""Command-line interface for Nakplae."""

import argparse
import sys
import time
import platform
import os
from pathlib import Path
from typing import List, Optional

import random
from tqdm import tqdm

# Fix for Windows terminal Unicode issues
if platform.system() == "Windows":
    try:
        # Force UTF-8 encoding for stdout/stderr
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        # For older Python versions
        pass

    # Set PYTHONIOENCODING for child processes
    os.environ["PYTHONIOENCODING"] = "utf-8"

    # Terminal detection - check if we're in a proper Unicode terminal
    IS_UNICODE_TERMINAL = False
    try:
        # Check if terminal supports UTF-8
        IS_UNICODE_TERMINAL = sys.stdout.encoding.lower() == "utf-8"
    except:
        pass
else:
    # Assume Unix-based systems support Unicode
    IS_UNICODE_TERMINAL = True

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

    parser.add_argument(
        "--model",
        default="small",
        choices=[
            "tiny",
            "base",
            "small",
            "medium",
            "large",
            "tiny.en",
            "base.en",
            "small.en",
            "medium.en",
        ],
        help="Whisper model to use (default: small). Use generic models for non-English content, or .en models for English-only content (faster).",
    )

    return parser.parse_args(args)


def show_welcome():
    """Display a cool welcome message."""
    # Use ASCII characters as fallback on Windows non-Unicode terminals
    if not IS_UNICODE_TERMINAL:
        welcome_text = [
            "## Welcome to Nakplae! ##",
            "** Video Transcription & Translation Tool **",
            "",
            ">> Transcribing with Whisper models (small by default)",
            ">> Translating with Google Gemini 2.0 Flash",
        ]
    else:
        welcome_text = [
            "🎬 Welcome to Nakplae! 🎬",
            "✨ Video Transcription & Translation Tool ✨",
            "",
            "🎤 Transcribing with Whisper models (small by default)",
            "🌍 Translating with Google Gemini 2.0 Flash",
        ]

    # Print the welcome message with a typing animation
    for line in welcome_text:
        for char in line:
            print(char, end="", flush=True)
            time.sleep(0.01)  # Adjust for typing speed
        print()
    print()


def show_summary(video_path, srt_file, translated_file=None, target_lang=None):
    """Display a summary of what was done."""
    print("\n" + "=" * 60)

    if IS_UNICODE_TERMINAL:
        print("✅ Process Complete!")
    else:
        print(">> Process Complete!")

    print("=" * 60)

    if IS_UNICODE_TERMINAL:
        video_icon = "📹"
        transcript_icon = "📝"
        translate_icon = "🌍"
        tip_icon = "💡"
        thanks_icon = "🙏"
    else:
        video_icon = "[VIDEO]"
        transcript_icon = "[TRANSCRIPT]"
        translate_icon = "[TRANSLATE]"
        tip_icon = "[TIP]"
        thanks_icon = "Thanks!"

    print(f"{video_icon} Source video: {video_path}")
    print(f"{transcript_icon} Transcription: {srt_file}")

    if translated_file:
        print(f"{translate_icon} Translation ({target_lang}): {translated_file}")

    # Add some fun facts
    fun_facts = [
        "Did you know? Whisper was trained on 680,000 hours of multilingual data!",
        "Fun fact: An average movie has about 1,500 subtitle entries.",
        "Tip: Subtitles improve content accessibility by up to 80%!",
        "Nakplae means 'translate' in an ancient fictional language.",
        "Whisper can recognize over 96 languages!",
    ]

    print(f"\n{tip_icon} " + random.choice(fun_facts))
    print(f"\nThanks for using Nakplae! {thanks_icon}")


def main(args: Optional[List[str]] = None) -> int:
    """Run the main program."""
    # Show welcome message
    show_welcome()

    parsed_args = parse_args(args)
    video_path = Path(parsed_args.video_file)

    if not video_path.exists():
        print(f"❌ Error: Video file not found: {video_path}", file=sys.stderr)
        return 1

    # Check for Gemini API key if translation is requested
    if not parsed_args.transcribe_only and not os.environ.get("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        print(
            "Translation requires a valid Gemini API key. Please set this environment variable:",
            file=sys.stderr,
        )
        print("   export GEMINI_API_KEY=your_api_key_here", file=sys.stderr)
        print(
            "\nAlternatively, run with --transcribe-only to skip translation.",
            file=sys.stderr,
        )
        return 1

    output_dir = parsed_args.output
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        srt_path = output_dir / f"{video_path.stem}.srt"
    else:
        srt_path = None

    try:
        # Add a small loading animation
        with tqdm(
            total=1, desc="🚀 Initializing", bar_format="{desc}", leave=False
        ) as pbar:
            time.sleep(0.5)
            pbar.update(1)

        # Step 1: Transcribe the video to SRT
        srt_file = transcribe_video(
            str(video_path),
            str(srt_path) if srt_path else None,
            model=parsed_args.model,
        )

        translated_file = None
        # Step 2: Translate the SRT if requested
        if not parsed_args.transcribe_only:
            if output_dir:
                translated_srt = (
                    output_dir / f"{video_path.stem}_{parsed_args.lang}.srt"
                )
            else:
                translated_srt = None

            translated_file = translate_srt(
                srt_file,
                parsed_args.lang,
                str(translated_srt) if translated_srt else None,
            )

        # Show summary
        show_summary(video_path, srt_file, translated_file, parsed_args.lang)

        return 0

    except KeyboardInterrupt:
        print("\n\n🛑 Process interrupted by user.")
        return 130

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
