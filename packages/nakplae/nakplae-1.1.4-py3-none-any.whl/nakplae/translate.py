"""SRT subtitle translation."""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Check if we're on Windows with a non-Unicode terminal
if platform.system() == "Windows":
    IS_UNICODE_TERMINAL = False
    try:
        IS_UNICODE_TERMINAL = sys.stdout.encoding.lower() == "utf-8"
    except Exception:  # pylint: disable=broad-except
        pass
else:
    # Assume Unix-based systems support Unicode
    IS_UNICODE_TERMINAL = True


def _try_local_llm_translation(
    srt_path: str, target_lang: str, output_path: str
) -> Optional[str]:
    """
    Attempt to translate an SRT file using a local LLM.

    Args:
        srt_path: Path to the SRT file
        target_lang: Target language
        output_path: Output path for translated file

    Returns:
        Output path if successful, None if not available
    """
    # Try to use llama.cpp if available
    try:
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()

        prompt = (
            f"Translate the following subtitle file to {target_lang}. "
            f"Maintain the original numbering and timestamps. "
            f"Only translate the text content:\n\n{content}"
        )

        # Attempt to use llama.cpp CLI
        result = subprocess.run(
            [
                "llama",
                "-m",
                os.environ.get("LLAMA_MODEL", "7B-chat.gguf"),
                "--temp",
                "0.1",
                "-p",
                prompt,
                "--no-display-prompt",
            ],
            check=True,
            text=True,
            capture_output=True,
            timeout=60,  # Longer timeout for full SRT translation
        )

        # Write to output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.stdout.strip())

        return output_path
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def _translate_with_gemini_srt(
    srt_path: str, target_lang: str, output_path: str
) -> str:
    """
    Translate SRT file using gemini-srt-translator package.

    Args:
        srt_path: Path to the SRT file
        target_lang: Target language
        output_path: Output path for translated file

    Returns:
        Path to the translated SRT file
    """
    try:
        import gemini_srt_translator as gst

        # Initialize the Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set. "
                "Translation requires a valid API key."
            )

        # Configure gemini-srt-translator
        if IS_UNICODE_TERMINAL:
            print(f"🌍 Using Gemini API to translate to {target_lang}...")
            print("🚀 Using gemini-srt-translator with model: gemini-2.0-flash")
        else:
            print(f"Using Gemini API to translate to {target_lang}...")
            print("Using gemini-srt-translator with model: gemini-2.0-flash")

        # Set parameters for translation
        gst.gemini_api_key = api_key
        gst.target_language = target_lang
        gst.input_file = srt_path
        gst.output_file = output_path
        gst.model_name = "gemini-2.0-flash"
        gst.batch_size = 30  # Process 30 subtitles at once (default)
        
        # The package handles progress display internally
        gst.translate()

        return output_path
    except Exception as e:
        print(f"Error using Gemini API: {e}")
        raise ValueError(f"Failed to translate using Gemini API: {e}") from e


def translate_srt(
    srt_path: str, target_lang: str, output_path: Optional[str] = None
) -> str:
    """
    Translate an SRT file to the target language.

    Args:
        srt_path: Path to the SRT file
        target_lang: Target language
        output_path: Optional path to save the translated SRT file

    Returns:
        Path to the translated SRT file
    """
    srt_path = Path(srt_path)

    if not srt_path.exists():
        raise FileNotFoundError(f"SRT file not found: {srt_path}")

    if output_path is None:
        output_path = str(srt_path.with_stem(f"{srt_path.stem}_{target_lang}"))

    # Try local LLM first
    local_translation = _try_local_llm_translation(
        str(srt_path), target_lang, output_path
    )
    if local_translation:
        return local_translation

    # Fall back to Gemini
    return _translate_with_gemini_srt(str(srt_path), target_lang, output_path)
