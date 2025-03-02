#!/usr/bin/env python3
"""Basic example of using the mtcleanse library for cleaning parallel text datasets."""

import argparse
import sys
from pathlib import Path
from textwrap import dedent

from mtcleanse.cleaning import ParallelTextCleaner
from mtcleanse.utils import configure_logging, get_console

# Configure logging
logger = configure_logging(level="INFO")
console = get_console()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Example of using mtcleanse for cleaning parallel text datasets."
    )
    
    parser.add_argument(
        "--source", "-s",
        required=True,
        help="Path to source language file"
    )
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Path to target language file"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="cleaned",
        help="Directory to save cleaned files"
    )
    parser.add_argument(
        "--enable-domain-filtering",
        action="store_true",
        help="Enable domain-based filtering (requires GPU)"
    )
    
    return parser.parse_args()


def main():
    """Run the example."""
    args = parse_args()
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get base filenames
    source_path = Path(args.source)
    target_path = Path(args.target)
    
    # Create output paths
    output_source = output_dir / f"clean_{source_path.name}"
    output_target = output_dir / f"clean_{target_path.name}"
    stats_output = output_dir / "stats.json"
    filtered_source = output_dir / f"filtered_{source_path.name}"
    filtered_target = output_dir / f"filtered_{target_path.name}"
    json_output = output_dir / "cleaned_data.json"
    
    # Create cleaner with custom configuration
    config = {
        "min_chars": 10,
        "max_chars": 500,
        "min_words": 3,
        "max_words": 50,
        "enable_domain_filtering": args.enable_domain_filtering,
        "domain_contamination": 0.2
    }
    
    cleaner = ParallelTextCleaner(config)
    
    # Example instruction for JSON output
    instruction = dedent("""
        Translate the following text from English to the target language.
        Maintain the same meaning, tone, and style in your translation.
    """).strip()
    
    # Clean files
    console.print(f"[bold]Cleaning files:[/] {args.source} and {args.target}")
    original_count, cleaned_count = cleaner.clean_files(
        source_file=args.source,
        target_file=args.target,
        output_source=output_source,
        output_target=output_target,
        stats_output=stats_output,
        filtered_source=filtered_source,
        filtered_target=filtered_target,
        json_output=json_output,
        instruction=instruction
    )
    
    # Print summary
    console.print("\n[bold green]Cleaning completed successfully![/]")
    console.print(f"Original pairs: {original_count}")
    console.print(f"Cleaned pairs: {cleaned_count}")
    console.print(f"Filtered pairs: {original_count - cleaned_count}")
    
    if original_count > 0:
        reduction = (original_count - cleaned_count) / original_count * 100
        console.print(f"Reduction: {reduction:.2f}%")
    
    console.print("\n[bold]Output files:[/]")
    console.print(f"Cleaned source: {output_source}")
    console.print(f"Cleaned target: {output_target}")
    console.print(f"Statistics: {stats_output}")
    console.print(f"Filtered source: {filtered_source}")
    console.print(f"Filtered target: {filtered_target}")
    console.print(f"JSON output: {json_output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 