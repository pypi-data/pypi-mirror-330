# Nakplae

A simple, elegant tool for transcribing videos to SRT subtitles and translating them with minimal dependencies.

## Features

- Transcribe video files to SRT subtitles using Whisper locally (multiple model options)
- Support for multilingual content using language-agnostic models (tiny, base, small, medium, large)
- Faster English-specific models available (tiny.en, base.en, small.en, medium.en)
- Optimized for speed with multi-threading and reduced beam size
- Translate SRT subtitles using Google's Gemini 2.0 Flash model
- Supports translation to any language (defaults to Thai)
- GPU acceleration for faster transcription (CUDA and Apple Silicon MPS support)
- Real-time Whisper progress output for better visibility
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
   # Installation from PyPI (includes GPU support by default)
   pip install nakplae
   ```
   
   For developers:
   ```bash
   # Clone the repository
   git clone https://github.com/elimydlarz/nakplae.git
   cd nakplae
   
   # Install in development mode
   pip install -e ".[dev]"
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

After installation, you can use the nakplae command directly:

```bash
# Basic usage (translates to Thai by default)
nakplae video_file.mp4

# Translate to a different language
nakplae video_file.mp4 --lang "Spanish"

# Only transcribe, don't translate
nakplae video_file.mp4 --transcribe-only

# Specify output directory
nakplae video_file.mp4 --lang "French" --output /path/to/output

# Use a faster model for multilingual content
nakplae video_file.mp4 --model tiny

# Use English-specific model for faster English transcription
nakplae video_file.mp4 --model small.en 

# Use a more accurate model for important content
nakplae video_file.mp4 --model medium
```

If you installed in development mode, you can also run:

```bash
python -m nakplae video_file.mp4 --lang "Spanish"
```

The program will automatically use GPU acceleration if available (CUDA on NVIDIA GPUs or MPS on Apple Silicon).

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

## Publishing

To publish a new release to PyPI:

```bash
# 1. Update version in pyproject.toml

# 2. Build the package
python -m build

# 3. Upload to PyPI (requires API token)
python -m twine upload dist/*X.Y.Z* -u __token__ -p $PYPI_API_TOKEN
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
