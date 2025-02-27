"""SRT subtitle translation."""

import re
import subprocess
import json
import os
import time
import random
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Union
from tqdm import tqdm


def _parse_srt(srt_path: str) -> List[Dict[str, Union[str, int]]]:
    """
    Parse an SRT file into a list of subtitle entries.
    
    Args:
        srt_path: Path to the SRT file
        
    Returns:
        List of subtitle entries with index, timestamp, and text
    """
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double newline to get each subtitle block
    subtitle_blocks = re.split(r'\n\n+', content.strip())
    subtitles = []
    
    for block in subtitle_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        
        subtitle_index = int(lines[0])
        timestamp = lines[1]
        text = '\n'.join(lines[2:])
        
        subtitles.append({
            'index': subtitle_index,
            'timestamp': timestamp,
            'text': text
        })
    
    return subtitles


def _format_srt(subtitles: List[Dict[str, Union[str, int]]]) -> str:
    """
    Format a list of subtitle entries back into SRT format.
    
    Args:
        subtitles: List of subtitle entries
        
    Returns:
        Formatted SRT content as string
    """
    srt_content = []
    
    for subtitle in subtitles:
        srt_content.append(f"{subtitle['index']}\n{subtitle['timestamp']}\n{subtitle['text']}")
    
    return '\n\n'.join(srt_content)


def _try_local_llm_translation(text: str, target_lang: str) -> Optional[str]:
    """
    Attempt to translate text using a local LLM.
    
    Args:
        text: Text to translate
        target_lang: Target language
        
    Returns:
        Translated text if successful, None if not available
    """
    # Try to use llama.cpp if available
    try:
        prompt = f"Translate the following text to {target_lang}. Only respond with the translation, no additional text:\n\n{text}"
        
        # Attempt to use llama.cpp CLI
        result = subprocess.run(
            [
                "llama", "-m", os.environ.get("LLAMA_MODEL", "7B-chat.gguf"),
                "--temp", "0.1", "-p", prompt, "--no-display-prompt"
            ],
            check=True,
            text=True,
            capture_output=True,
            timeout=30
        )
        
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def _translate_with_gemini(text: str, target_lang: str) -> str:
    """
    Translate text using Google's Gemini API.
    
    Args:
        text: Text to translate
        target_lang: Target language code
        
    Returns:
        Translated text
    """
    try:
        import google.generativeai as genai
        
        # Initialize the Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("GEMINI_API_KEY environment variable not set. Using a simple placeholder translation.")
            return f"[Translation to {target_lang}]: {text}"
        
        print(f"Using Gemini API to translate to {target_lang}...")
        genai.configure(api_key=api_key)
        
        # Use the specified model directly
        model_name = "models/gemini-2.0-flash"
        print(f"Using model: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        prompt = f"Translate the following text to {target_lang}. Only respond with the translation, no additional text or commentary:\n\n{text}"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error using Gemini API: {e}")
        print("Using a simple placeholder translation instead.")
        return f"[Translation to {target_lang}]: {text}"


def translate_text(text: str, target_lang: str) -> str:
    """
    Translate text to the target language.
    
    Args:
        text: Text to translate
        target_lang: Target language
        
    Returns:
        Translated text
    """
    # Try local LLM first
    local_translation = _try_local_llm_translation(text, target_lang)
    if local_translation:
        return local_translation
    
    # Fall back to Gemini
    return _translate_with_gemini(text, target_lang)


def translate_srt(srt_path: str, target_lang: str, output_path: Optional[str] = None) -> str:
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
        output_path = srt_path.with_stem(f"{srt_path.stem}_{target_lang}")
    
    # Parse the SRT file
    subtitles = _parse_srt(str(srt_path))
    
    # Set up a progress bar for translation
    translation_emojis = ["🌍", "🌎", "🌏", "🔤", "💬", "🗣️", "🧠", "✨", "🤖", "📝"]
    
    with tqdm(
        total=len(subtitles),
        desc=f"{random.choice(translation_emojis)} Translating to {target_lang}",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} subtitles [{elapsed}<{remaining}]",
        colour="blue"
    ) as pbar:
        # Translate each subtitle entry
        for i, subtitle in enumerate(subtitles):
            # Update progress bar with fun emoji
            if i % 5 == 0 and i > 0:  # Change emoji every 5 items
                pbar.set_description(f"{random.choice(translation_emojis)} Translating to {target_lang}")
            
            # Translate the text
            subtitle['text'] = translate_text(subtitle['text'], target_lang)
            
            # Update progress
            pbar.update(1)
            
            # Add a small delay to make the progress bar visible for small files
            if len(subtitles) < 5:
                time.sleep(0.2)
    
    # Format the translated subtitles
    translated_content = _format_srt(subtitles)
    
    # Write to the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    
    return str(output_path)