"""Logging utilities for the c3po package."""

import logging
import sys
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler


def configure_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    module_name: str = "c3po"
) -> logging.Logger:
    """Configure logging for the c3po package.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to save logs to a file
        module_name: Name of the module to get logger for
        
    Returns:
        Configured logger
    """
    # Create handlers
    handlers = [
        RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            omit_repeated_times=False,
            show_path=False
        )
    ]
    
    # Add file handler if log_file is provided
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers
    )
    
    # Get and return logger for the specified module
    logger = logging.getLogger(module_name)
    return logger


def get_console() -> Console:
    """Get a rich console for pretty printing.
    
    Returns:
        Rich console
    """
    return Console() 