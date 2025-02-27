# Nakplae

A simple, elegant tool for transcribing videos to SRT subtitles and translating them with minimal dependencies.

## Features

- Transcribe video files to SRT subtitles using Whisper locally (small.en model)
- Translate SRT subtitles using Google's Gemini 2.0 Flash model
- Supports translation to any language (defaults to Thai)
- Simple command-line interface
- Minimal dependencies

## Installation

### Setup Environment

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the package:
   ```bash
   # Basic installation
   pip install -e .

   # With all development tools
   pip install -e ".[dev,gemini]"

   # Or from requirements files
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

### Prerequisites

1. Ensure you have [FFmpeg](https://ffmpeg.org/download.html) installed (required by Whisper)
   - On macOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt install ffmpeg`
   - On Windows: Download from the official website or use chocolatey

2. For local LLM translation (optional):
   - Install [llama.cpp](https://github.com/ggerganov/llama.cpp) and ensure `llama` is in your PATH

3. For Gemini translation:
   - Set `GEMINI_API_KEY` environment variable with your API key:
     ```bash
     export GEMINI_API_KEY=your_api_key_here
     ```
   - Uses the Gemini 2.0 Flash model for translations

## Usage

```bash
# Basic usage (translates to Thai by default)
python -m nakplae video_file.mp4

# Translate to a different language
python -m nakplae video_file.mp4 --lang "Spanish"

# Only transcribe, don't translate
python -m nakplae video_file.mp4 --transcribe-only

# Specify output directory
python -m nakplae video_file.mp4 --lang "French" --output /path/to/output
```

## Development

```bash
# Run tests
pytest

# Format code
black .

# Run linter
ruff check .

# Run type checker
mypy nakplae
```

## Project Structure

```
nakplae/
├── nakplae/
│   ├── __init__.py
│   ├── __main__.py
│   ├── transcribe.py
│   └── translate.py
├── tests/
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## License

MIT
