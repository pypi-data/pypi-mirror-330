"""MTCleanse: Machine Translation Corpus Cleaning and Processing.

A Python library for cleaning and processing parallel text datasets,
particularly useful for machine translation and other NLP tasks.
"""

__version__ = "0.1.0"

from mtcleanse.cleaning import ParallelTextCleaner, CleaningConfig

__all__ = ['ParallelTextCleaner', 'CleaningConfig']
