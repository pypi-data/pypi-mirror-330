#!/usr/bin/env python3
"""Command-line interface for cleaning parallel text datasets."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from rich.console import Console
from rich.logging import RichHandler

from c3po.cleaning import ParallelTextCleaner

# Configure logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("c3po")
console = Console()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Clean parallel text datasets for machine translation.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
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
    
    # Output paths
    parser.add_argument(
        "--output-source", "-os",
        help="Path to save cleaned source text (default: clean_<source>)"
    )
    parser.add_argument(
        "--output-target", "-ot",
        help="Path to save cleaned target text (default: clean_<target>)"
    )
    parser.add_argument(
        "--stats-output", "-so",
        help="Path to save cleaning statistics as JSON"
    )
    parser.add_argument(
        "--filtered-source", "-fs",
        help="Path to save filtered source text"
    )
    parser.add_argument(
        "--filtered-target", "-ft",
        help="Path to save filtered target text"
    )
    parser.add_argument(
        "--json-output", "-jo",
        help="Path to save cleaned data as JSON"
    )
    parser.add_argument(
        "--instruction", "-i",
        help="Instruction to include in JSON output"
    )
    
    # Cleaning parameters
    parser.add_argument(
        "--min-chars", 
        type=int, 
        default=1,
        help="Minimum number of characters for a text to be valid"
    )
    parser.add_argument(
        "--max-chars", 
        type=int, 
        default=1000,
        help="Maximum number of characters for a text to be valid"
    )
    parser.add_argument(
        "--min-words", 
        type=int, 
        default=1,
        help="Minimum number of words for a text to be valid"
    )
    parser.add_argument(
        "--max-words", 
        type=int, 
        default=150,
        help="Maximum number of words for a text to be valid"
    )
    parser.add_argument(
        "--contamination", 
        type=float, 
        default=0.1,
        help="Expected proportion of statistical outliers"
    )
    parser.add_argument(
        "--random-state", 
        type=int, 
        default=42,
        help="Random seed for reproducibility"
    )
    
    # Boolean flags
    parser.add_argument(
        "--no-remove-urls", 
        action="store_true",
        help="Don't remove URLs from texts"
    )
    parser.add_argument(
        "--no-remove-emails", 
        action="store_true",
        help="Don't remove email addresses from texts"
    )
    parser.add_argument(
        "--no-normalize-unicode", 
        action="store_true",
        help="Don't normalize Unicode characters"
    )
    parser.add_argument(
        "--no-remove-control-chars", 
        action="store_true",
        help="Don't remove control characters"
    )
    parser.add_argument(
        "--lowercase", 
        action="store_true",
        help="Convert texts to lowercase"
    )
    parser.add_argument(
        "--no-remove-extra-whitespace", 
        action="store_true",
        help="Don't normalize whitespace"
    )
    
    # Domain filtering
    parser.add_argument(
        "--enable-domain-filtering", 
        action="store_true",
        help="Enable domain-based filtering using sentence embeddings"
    )
    parser.add_argument(
        "--embedding-model", 
        default="all-MiniLM-L6-v2",
        help="Name of the sentence transformer model to use"
    )
    parser.add_argument(
        "--domain-contamination", 
        type=float, 
        default=0.1,
        help="Expected proportion of domain outliers"
    )
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=32,
        help="Batch size for embedding generation"
    )
    parser.add_argument(
        "--cpu", 
        action="store_true",
        help="Force using CPU for embedding generation"
    )
    
    # Verbosity
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def args_to_config(args: argparse.Namespace) -> Dict[str, Any]:
    """Convert command-line arguments to configuration dictionary.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Configuration dictionary
    """
    config = {
        "min_chars": args.min_chars,
        "max_chars": args.max_chars,
        "min_words": args.min_words,
        "max_words": args.max_words,
        "contamination": args.contamination,
        "random_state": args.random_state,
        "remove_urls": not args.no_remove_urls,
        "remove_emails": not args.no_remove_emails,
        "normalize_unicode": not args.no_normalize_unicode,
        "remove_control_chars": not args.no_remove_control_chars,
        "lowercase": args.lowercase,
        "remove_extra_whitespace": not args.no_remove_extra_whitespace,
        "enable_domain_filtering": args.enable_domain_filtering,
        "embedding_model": args.embedding_model,
        "domain_contamination": args.domain_contamination,
        "batch_size": args.batch_size,
    }
    
    # Force CPU if requested
    if args.cpu:
        config["device"] = "cpu"
    
    return config


def validate_args(args: argparse.Namespace) -> Optional[str]:
    """Validate command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Error message if validation fails, None otherwise
    """
    # Check that source and target files exist
    if not Path(args.source).exists():
        return f"Source file does not exist: {args.source}"
    
    if not Path(args.target).exists():
        return f"Target file does not exist: {args.target}"
    
    # Check that contamination is between 0 and 0.5
    if not 0 < args.contamination < 0.5:
        return f"Contamination must be between 0 and 0.5, got {args.contamination}"
    
    # Check that domain contamination is between 0 and 0.5
    if not 0 < args.domain_contamination < 0.5:
        return f"Domain contamination must be between 0 and 0.5, got {args.domain_contamination}"
    
    # Check that batch size is positive
    if args.batch_size <= 0:
        return f"Batch size must be positive, got {args.batch_size}"
    
    return None


def main() -> int:
    """Main entry point for the command-line interface.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    args = parse_args()
    
    # Set log level
    if args.verbose:
        logging.getLogger("c3po").setLevel(logging.DEBUG)
    
    # Validate arguments
    error = validate_args(args)
    if error:
        console.print(f"[bold red]Error:[/] {error}")
        return 1
    
    try:
        # Create cleaner with configuration from arguments
        config = args_to_config(args)
        cleaner = ParallelTextCleaner(config)
        
        # Clean files
        original_count, cleaned_count = cleaner.clean_files(
            source_file=args.source,
            target_file=args.target,
            output_source=args.output_source,
            output_target=args.output_target,
            stats_output=args.stats_output,
            filtered_source=args.filtered_source,
            filtered_target=args.filtered_target,
            json_output=args.json_output,
            instruction=args.instruction
        )
        
        # Print summary
        console.print("\n[bold green]Cleaning completed successfully![/]")
        console.print(f"Original pairs: {original_count}")
        console.print(f"Cleaned pairs: {cleaned_count}")
        console.print(f"Filtered pairs: {original_count - cleaned_count}")
        
        if original_count > 0:
            reduction = (original_count - cleaned_count) / original_count * 100
            console.print(f"Reduction: {reduction:.2f}%")
        
        return 0
    
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        if args.verbose:
            console.print_exception()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 