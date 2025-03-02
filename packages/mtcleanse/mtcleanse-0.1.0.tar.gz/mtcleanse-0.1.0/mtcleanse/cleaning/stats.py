"""Module for tracking and reporting text cleaning statistics."""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Any

import numpy as np

# Configure logging
logger = logging.getLogger("mtcleanse")


def convert_to_serializable(obj: Any) -> Any:
    """Convert numpy types to Python native types for JSON serialization.
    
    Args:
        obj: Object to convert
        
    Returns:
        Serializable version of the object
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_serializable(item) for item in obj]
    return round(obj, 2) if isinstance(obj, float) else obj


@dataclass
class FilteredSamples:
    """Store samples of filtered text pairs for analysis.
    
    This class stores examples of text pairs that were filtered out during
    the cleaning process, categorized by the reason for filtering.
    
    Attributes:
        empty_samples: Samples that were empty after cleaning
        too_short_samples: Samples that were too short
        too_long_samples: Samples that were too long
        word_count_samples: Samples that had too few or too many words
        statistical_outliers_samples: Samples identified as statistical outliers
        domain_outliers_samples: Samples identified as domain outliers
    """
    
    empty_samples: List[Tuple[str, str]] = None
    too_short_samples: List[Tuple[str, str]] = None
    too_long_samples: List[Tuple[str, str]] = None
    word_count_samples: List[Tuple[str, str]] = None
    statistical_outliers_samples: List[Tuple[str, str]] = None
    domain_outliers_samples: List[Tuple[str, str]] = None
    
    def __post_init__(self):
        """Initialize empty lists."""
        self.empty_samples = []
        self.too_short_samples = []
        self.too_long_samples = []
        self.word_count_samples = []
        self.statistical_outliers_samples = []
        self.domain_outliers_samples = []
    
    def to_dict(self, max_samples: int = 5) -> Dict:
        """Convert samples to dictionary, limiting each category to max_samples examples.
        
        Args:
            max_samples: Maximum number of samples to include per category
            
        Returns:
            Dictionary of sample categories
        """
        samples_dict = {}
        
        # Only include non-empty sample categories
        if self.empty_samples:
            samples_dict["empty_samples"] = self.empty_samples[:max_samples]
        if self.too_short_samples:
            samples_dict["too_short_samples"] = self.too_short_samples[:max_samples]
        if self.too_long_samples:
            samples_dict["too_long_samples"] = self.too_long_samples[:max_samples]
        if self.word_count_samples:
            samples_dict["word_count_samples"] = self.word_count_samples[:max_samples]
        if self.statistical_outliers_samples:
            samples_dict["statistical_outliers_samples"] = self.statistical_outliers_samples[:max_samples]
        if self.domain_outliers_samples:
            samples_dict["domain_outliers_samples"] = self.domain_outliers_samples[:max_samples]
        
        return samples_dict


@dataclass
class CleaningStats:
    """Statistics for each cleaning step.
    
    This class tracks statistics about the cleaning process, including
    counts of filtered texts and reasons for filtering.
    
    Attributes:
        total_pairs: Total number of text pairs processed
        empty_after_cleaning: Number of pairs that were empty after cleaning
        too_short: Number of pairs that were too short
        too_long: Number of pairs that were too long
        word_count_filtered: Number of pairs filtered by word count
        statistical_outliers: Number of pairs identified as statistical outliers
        domain_outliers: Number of pairs identified as domain outliers
        final_pairs: Number of pairs remaining after cleaning
        min_chars: Minimum character count used for filtering
        max_chars: Maximum character count used for filtering
        length_stats: Statistics about text lengths
        filtered_samples: Examples of filtered text pairs
    """
    total_pairs: int = 0
    empty_after_cleaning: int = 0
    too_short: int = 0
    too_long: int = 0
    word_count_filtered: int = 0
    statistical_outliers: int = 0
    domain_outliers: int = 0
    final_pairs: int = 0
    min_chars: int = 0
    max_chars: int = 0
    length_stats: Dict = None
    filtered_samples: FilteredSamples = None

    def __post_init__(self):
        """Initialize nested objects."""
        self.length_stats = {}
        self.filtered_samples = FilteredSamples()

    def to_dict(self) -> Dict:
        """Convert stats to dictionary format for JSON export.
        
        Returns:
            Dictionary of cleaning statistics
        """
        stats_dict = {
            "total_pairs": int(self.total_pairs),
            "empty_after_cleaning": int(self.empty_after_cleaning),
            "too_short": int(self.too_short),
            "too_long": int(self.too_long),
            "word_count_filtered": int(self.word_count_filtered),
            "statistical_outliers": int(self.statistical_outliers),
            "domain_outliers": int(self.domain_outliers),
            "final_pairs": int(self.final_pairs),
            "min_chars": int(self.min_chars),
            "max_chars": int(self.max_chars),
            "length_stats": convert_to_serializable(self.length_stats),
            "filtered_samples": self.filtered_samples.to_dict(),
        }
        
        # Calculate reduction percentage if there were any pairs
        if self.total_pairs > 0:
            stats_dict["reduction_percentage"] = float((self.total_pairs - self.final_pairs) / self.total_pairs * 100)
        else:
            stats_dict["reduction_percentage"] = 0.0
            
        return stats_dict

    def save_to_json(self, output_path: str) -> None:
        """Save statistics to a JSON file.
        
        Args:
            output_path: Path to save the statistics to
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info(f"Cleaning statistics saved to: {output_path}")

    def log_stats(self) -> None:
        """Log the cleaning statistics."""
        logger.info("Cleaning Statistics:")
        logger.info(f"Total pairs processed: {self.total_pairs}")
        logger.info(f"Pairs empty after basic cleaning: {self.empty_after_cleaning}")
        logger.info(f"Pairs too short (<{self.min_chars} chars): {self.too_short}")
        logger.info(f"Pairs too long (>{self.max_chars} chars): {self.too_long}")
        logger.info(f"Pairs filtered by word count: {self.word_count_filtered}")
        logger.info(f"Pairs identified as statistical outliers: {self.statistical_outliers}")
        logger.info(f"Pairs identified as domain outliers: {self.domain_outliers}")
        logger.info(f"Final pairs remaining: {self.final_pairs}")
        
        if self.total_pairs > 0:
            reduction = (self.total_pairs - self.final_pairs) / self.total_pairs * 100
            logger.info(f"Total reduction: {reduction:.2f}%")
        else:
            logger.info("Total reduction: 0.00%") 