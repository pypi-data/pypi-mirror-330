"""Command-line interface for English-to-Thai transliteration."""

import argparse
import json
import os
import sys
from typing import List, Dict, Union

from .transliterator import En2ThTransliterator


def parse_args():
    parser = argparse.ArgumentParser(
        description='Transliterate English text to Thai using a ByT5 model')

    # Input/output options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text',
                       type=str,
                       help='English text to transliterate')
    group.add_argument('--file',
                       type=str,
                       help='File containing English text to transliterate')

    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--format',
                        type=str,
                        choices=['text', 'json', 'tsv'],
                        default='text',
                        help='Output format (text, json, or tsv)')

    # Model options
    parser.add_argument(
        '--model-path',
        type=str,
        help='Path to a local model (if not specified, will use HF model)')
    parser.add_argument('--max-length',
                        type=int,
                        default=100,
                        help='Maximum length of generated sequence')
    parser.add_argument('--num-beams',
                        type=int,
                        default=4,
                        help='Number of beams for beam search')
    parser.add_argument('--length-penalty',
                        type=float,
                        default=1.0,
                        help='Length penalty for generation')

    # Generation options
    parser.add_argument('--temperature',
                        type=float,
                        default=1.0,
                        help='Sampling temperature')
    parser.add_argument('--top-k', type=int, help='Top-k sampling parameter')
    parser.add_argument('--top-p', type=float, help='Top-p sampling parameter')

    # Performance options
    parser.add_argument('--batch-size',
                        type=int,
                        default=8,
                        help='Batch size for processing')
    parser.add_argument('--no-fp16',
                        action='store_true',
                        help='Disable mixed precision (fp16) for inference')
    parser.add_argument('--verbose',
                        action='store_true',
                        help='Enable verbose output')

    return parser.parse_args()


def read_input_file(file_path: str) -> List[str]:
    """Read input file and return a list of lines."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def write_output(english_texts: List[str],
                 thai_texts: List[str],
                 output_format: str,
                 output_path: str = None) -> None:
    """Write output in the specified format."""
    if output_format == 'text':
        output_content = '\n'.join(thai_texts)
    elif output_format == 'json':
        output_content = json.dumps([{
            'english': eng,
            'thai': thai
        } for eng, thai in zip(english_texts, thai_texts)],
                                    ensure_ascii=False,
                                    indent=2)
    elif output_format == 'tsv':
        output_content = '\n'.join(
            [f"{eng}\t{thai}" for eng, thai in zip(english_texts, thai_texts)])

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Output written to {output_path}")
    else:
        print(output_content)


def main():
    args = parse_args()

    # Initialize the transliterator
    transliterator = En2ThTransliterator(model_path=args.model_path,
                                         max_length=args.max_length,
                                         num_beams=args.num_beams,
                                         length_penalty=args.length_penalty,
                                         verbose=args.verbose,
                                         fp16=not args.no_fp16)

    # Prepare generation kwargs
    gen_kwargs = {}
    if args.temperature != 1.0:
        gen_kwargs['temperature'] = args.temperature
    if args.top_k is not None:
        gen_kwargs['top_k'] = args.top_k
    if args.top_p is not None:
        gen_kwargs['top_p'] = args.top_p

    # Process input
    if args.text:
        english_texts = [args.text]
        thai_texts = [transliterator.transliterate(args.text, **gen_kwargs)]
    else:
        english_texts = read_input_file(args.file)
        thai_texts = transliterator.batch_transliterate(
            english_texts, batch_size=args.batch_size, **gen_kwargs)

    # Write output
    write_output(english_texts, thai_texts, args.format, args.output)


if __name__ == "__main__":
    main()
