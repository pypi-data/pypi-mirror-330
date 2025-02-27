#!/usr/bin/env python3
import os
import sys
# Insert the project root (containing main.py) so that main can be imported
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from main import process_input  # now main.py is accessible
import argparse
import dspy
import gradio as gr

def main():
    parser = argparse.ArgumentParser(
        description="wenbi: Convert video, audio, URL, or subtitle files to CSV and Markdown outputs."
    )
    parser.add_argument("input", help="Path or URL to the input file")
    parser.add_argument("--language", default="", help="Transcribe language (optional)")
    parser.add_argument("--rewrite-llm", default="", help="Rewrite LLM model identifier (optional)")
    parser.add_argument("--translate-llm", default="", help="Translation LLM model identifier (optional)")
    parser.add_argument("--multi-language", action="store_true", help="Enable multi-language processing")
    parser.add_argument("--translate-lang", default="Chinese", help="Target translation language (default: Chinese)")
    parser.add_argument("--output-dir", default="", help="Output directory (optional)")
    args = parser.parse_args()

    # Determine if the input is a URL
    is_url = args.input.startswith(('http://', 'https://', 'www.'))
    result = process_input(
                None if is_url else args.input,         # file_path
                args.input if is_url else "",            # url
                args.language,
                args.rewrite_llm,
                args.translate_llm,
                args.multi_language,
                args.translate_lang,
                args.output_dir
             )

    # Print relevant outputs (assuming process_input returns a tuple)
    print("Markdown Output:", result[0])
    print("Markdown File:", result[1])
    print("CSV File:", result[2])
    print("Filename (without extension):", result[3] if result[3] is not None else "")

if __name__ == "__main__":
    main()
