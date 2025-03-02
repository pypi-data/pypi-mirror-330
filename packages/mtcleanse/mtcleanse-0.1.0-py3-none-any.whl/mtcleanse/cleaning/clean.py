"""Core module for cleaning parallel text datasets."""

import re
import json
import logging
import unicodedata
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Union, Any

import numpy as np
import torch
from sklearn.ensemble import IsolationForest
from sentence_transformers import SentenceTransformer

from mtcleanse.cleaning.config import CleaningConfig
from mtcleanse.cleaning.stats import CleaningStats

# Configure logging
logger = logging.getLogger("mtcleanse")


class TextCleaner:
    """Class for cleaning text data with various options.
    
    This class provides methods for cleaning parallel text datasets,
    including filtering by length, removing noise, and detecting outliers.
    """
    
    def __init__(self, config: Optional[CleaningConfig] = None):
        """Initialize the cleaner with given configuration.
        
        Args:
            config: Configuration for the cleaning process
        """
        self.config = config or CleaningConfig()
        self.stats = CleaningStats()
        
        # Compile regex patterns
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        self.control_char_pattern = re.compile(r'[\x00-\x1F\x7F-\x9F]')

        # Initialize sentence transformer if domain filtering is enabled
        self.sentence_transformer = None
        if self.config.enable_domain_filtering:
            logger.info(f"Loading sentence transformer model: {self.config.embedding_model}")
            self.sentence_transformer = SentenceTransformer(self.config.embedding_model)
            self.sentence_transformer.to(self.config.device)
    
    def _get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts using batched processing.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            Array of embeddings
        """
        embeddings = []
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            with torch.no_grad():
                batch_embeddings = self.sentence_transformer.encode(
                    batch,
                    convert_to_numpy=True,
                    device=self.config.device,
                    show_progress_bar=False
                )
            embeddings.append(batch_embeddings)
        return np.vstack(embeddings)

    def _detect_domain_outliers(self, source_texts: List[str], target_texts: List[str]) -> List[bool]:
        """Detect domain outliers using sentence embeddings and isolation forest.
        
        Args:
            source_texts: List of source language texts
            target_texts: List of target language texts
            
        Returns:
            Boolean mask indicating which texts are inliers (True) and outliers (False)
        """
        if not self.config.enable_domain_filtering:
            return [True] * len(source_texts)  # Return all as inliers if domain filtering is disabled

        logger.info("Generating embeddings for domain filtering...")
        
        # Generate embeddings for source and target texts
        source_embeddings = self._get_embeddings(source_texts)
        target_embeddings = self._get_embeddings(target_texts)
        
        # Concatenate source and target embeddings for joint analysis
        combined_embeddings = np.concatenate([source_embeddings, target_embeddings], axis=1)
        
        # Initialize and fit isolation forest
        iso_forest = IsolationForest(
            contamination=self.config.domain_contamination,
            random_state=self.config.random_state
        )
        
        # Predict returns 1 for inliers and -1 for outliers
        predictions = iso_forest.fit_predict(combined_embeddings)
        
        # Store samples of domain outliers
        outlier_indices = np.where(predictions == -1)[0]
        for idx in outlier_indices[:5]:  # Store up to 5 examples
            self.stats.filtered_samples.domain_outliers_samples.append(
                (source_texts[idx], target_texts[idx])
            )
        
        # Update statistics
        self.stats.domain_outliers = np.sum(predictions == -1)
        
        return predictions == 1
    
    def _detect_length_outliers(self, source_texts: List[str], target_texts: List[str]) -> List[bool]:
        """Detect outliers based on statistical analysis of text lengths.
        
        Args:
            source_texts: List of source language texts
            target_texts: List of target language texts
            
        Returns:
            Boolean mask indicating which texts are inliers (True) and outliers (False)
        """
        # Extract features (lengths of source and target texts)
        src_lengths = np.array([len(text) for text in source_texts])
        tgt_lengths = np.array([len(text) for text in target_texts])
        
        # Calculate and store length statistics
        self.stats.length_stats = {
            "source": {
                "mean": float(src_lengths.mean()),
                "std": float(src_lengths.std()),
                "min": int(src_lengths.min()),
                "max": int(src_lengths.max()),
                "median": float(np.median(src_lengths)),
                "percentiles": {
                    "25": float(np.percentile(src_lengths, 25)),
                    "75": float(np.percentile(src_lengths, 75))
                }
            },
            "target": {
                "mean": float(tgt_lengths.mean()),
                "std": float(tgt_lengths.std()),
                "min": int(tgt_lengths.min()),
                "max": int(tgt_lengths.max()),
                "median": float(np.median(tgt_lengths)),
                "percentiles": {
                    "25": float(np.percentile(tgt_lengths, 25)),
                    "75": float(np.percentile(tgt_lengths, 75))
                }
            }
        }
        
        # Log length statistics
        logger.info("Length Statistics:")
        logger.info(f"Source - Mean: {src_lengths.mean():.1f}, Std: {src_lengths.std():.1f}, "
                   f"Min: {src_lengths.min()}, Max: {src_lengths.max()}")
        logger.info(f"Target - Mean: {tgt_lengths.mean():.1f}, Std: {tgt_lengths.std():.1f}, "
                   f"Min: {tgt_lengths.min()}, Max: {tgt_lengths.max()}")
        
        # Combine features into 2D array
        X = np.column_stack([src_lengths, tgt_lengths])
        
        # Initialize and fit the isolation forest
        iso_forest = IsolationForest(
            contamination=self.config.contamination,
            random_state=self.config.random_state
        )
        
        # Predict returns 1 for inliers and -1 for outliers
        predictions = iso_forest.fit_predict(X)
        
        # Store samples of statistical outliers
        outlier_indices = np.where(predictions == -1)[0]
        for idx in outlier_indices[:5]:  # Store up to 5 examples
            self.stats.filtered_samples.statistical_outliers_samples.append(
                (source_texts[idx], target_texts[idx])
            )
        
        # Update statistics
        self.stats.statistical_outliers = np.sum(predictions == -1)
        
        # Convert to boolean mask (True for inliers)
        return predictions == 1
    
    def _clean_single_text(self, text: str) -> Tuple[str, Dict[str, bool]]:
        """Apply cleaning operations to a single text and return cleaning flags.
        
        Args:
            text: Text to clean
            
        Returns:
            Tuple of (cleaned text, flags dictionary)
        """
        if not text:
            return "", {"empty": True}
        
        flags = {
            "empty": False,
            "too_short": False,
            "too_long": False
        }
        
        # Basic whitespace normalization
        text = text.strip()
        
        # Remove URLs if configured
        if self.config.remove_urls:
            text = self.url_pattern.sub('', text)
            
        # Remove emails if configured
        if self.config.remove_emails:
            text = self.email_pattern.sub('', text)
            
        # Remove control characters if configured
        if self.config.remove_control_chars:
            text = self.control_char_pattern.sub('', text)
            
        # Unicode normalization if configured
        if self.config.normalize_unicode:
            text = unicodedata.normalize('NFKC', text)
            
        # Convert to lowercase if configured
        if self.config.lowercase:
            text = text.lower()
            
        # Remove extra whitespace if configured
        if self.config.remove_extra_whitespace:
            text = ' '.join(text.split())
            
        # Check character length constraints
        text_len = len(text)
        if text_len < self.config.min_chars:
            flags["too_short"] = True
            return "", flags
        elif text_len > self.config.max_chars:
            flags["too_long"] = True
            return "", flags
            
        return text, flags
    
    def clean_parallel_texts(
        self,
        source_texts: List[str],
        target_texts: List[str]
    ) -> Tuple[List[str], List[str]]:
        """Clean parallel texts and return filtered versions.
        
        Args:
            source_texts: List of source language texts
            target_texts: List of target language texts
            
        Returns:
            Tuple of (cleaned source texts, cleaned target texts)
        """
        if len(source_texts) != len(target_texts):
            raise ValueError("Source and target texts must have the same length")
        
        # Reset statistics
        self.stats = CleaningStats()
        self.stats.total_pairs = len(source_texts)
        self.stats.min_chars = self.config.min_chars
        self.stats.max_chars = self.config.max_chars
        
        cleaned_source = []
        cleaned_target = []
        
        # First pass: basic cleaning
        temp_source = []
        temp_target = []
        
        logger.info(f"Starting cleaning process for {len(source_texts)} text pairs...")
        
        for src, tgt in zip(source_texts, target_texts):
            # Store original texts for sample logging
            orig_src, orig_tgt = src, tgt
            
            # Apply basic cleaning to both
            src_clean, src_flags = self._clean_single_text(src)
            tgt_clean, tgt_flags = self._clean_single_text(tgt)
            
            # Update statistics and store samples based on flags
            if src_flags["empty"] or tgt_flags["empty"]:
                self.stats.empty_after_cleaning += 1
                if len(self.stats.filtered_samples.empty_samples) < 5:
                    self.stats.filtered_samples.empty_samples.append((orig_src, orig_tgt))
                continue
            
            if src_flags["too_short"] or tgt_flags["too_short"]:
                self.stats.too_short += 1
                if len(self.stats.filtered_samples.too_short_samples) < 5:
                    self.stats.filtered_samples.too_short_samples.append((orig_src, orig_tgt))
                continue
                
            if src_flags["too_long"] or tgt_flags["too_long"]:
                self.stats.too_long += 1
                if len(self.stats.filtered_samples.too_long_samples) < 5:
                    self.stats.filtered_samples.too_long_samples.append((orig_src, orig_tgt))
                continue
            
            # Check word counts
            src_words = len(src_clean.split())
            tgt_words = len(tgt_clean.split())
            
            if not (self.config.min_words <= src_words <= self.config.max_words and
                   self.config.min_words <= tgt_words <= self.config.max_words):
                self.stats.word_count_filtered += 1
                if len(self.stats.filtered_samples.word_count_samples) < 5:
                    self.stats.filtered_samples.word_count_samples.append((orig_src, orig_tgt))
                continue
            
            temp_source.append(src_clean)
            temp_target.append(tgt_clean)
        
        if not temp_source:  # If all texts were filtered out
            logger.warning("All text pairs were filtered out during basic cleaning!")
            self.stats.final_pairs = 0
            self.stats.log_stats()
            return [], []
        
        # Second pass: statistical outlier detection
        logger.info(f"Performing statistical outlier detection on {len(temp_source)} pairs...")
        length_inlier_mask = self._detect_length_outliers(temp_source, temp_target)
        
        # Third pass: domain filtering (if enabled)
        if self.config.enable_domain_filtering:
            logger.info(f"Performing domain filtering on {len(temp_source)} pairs...")
            domain_inlier_mask = self._detect_domain_outliers(temp_source, temp_target)
            # Combine masks - only keep samples that pass both filters
            final_mask = [a and b for a, b in zip(length_inlier_mask, domain_inlier_mask)]
        else:
            final_mask = length_inlier_mask
        
        # Keep only the inliers
        cleaned_source = [text for text, is_inlier in zip(temp_source, final_mask) if is_inlier]
        cleaned_target = [text for text, is_inlier in zip(temp_target, final_mask) if is_inlier]
        
        self.stats.final_pairs = len(cleaned_source)
        self.stats.log_stats()
        
        return cleaned_source, cleaned_target
    
    def clean_file(
        self,
        source_file: str,
        target_file: str,
        output_source: str,
        output_target: str,
        stats_output: Optional[str] = None,
        filtered_source: Optional[str] = None,
        filtered_target: Optional[str] = None,
        json_output: Optional[str] = None,
        instruction: Optional[str] = None
    ) -> Tuple[int, int]:
        """Clean parallel text files and save results.
        
        Args:
            source_file: Input source language file path
            target_file: Input target language file path
            output_source: Output path for cleaned source text
            output_target: Output path for cleaned target text
            stats_output: Optional path to save cleaning statistics
            filtered_source: Optional path to save filtered source text
            filtered_target: Optional path to save filtered target text
            json_output: Optional path to save cleaned data as JSON
            instruction: Optional instruction to include in JSON output
            
        Returns:
            Tuple of (original count, cleaned count)
        """
        logger.info(f"Reading files: {source_file} and {target_file}")
        
        with open(source_file, 'r', encoding='utf-8') as src_f, \
             open(target_file, 'r', encoding='utf-8') as tgt_f:
            source_texts = [line.strip() for line in src_f]
            target_texts = [line.strip() for line in tgt_f]
        
        # Store original texts for filtered output
        original_pairs = list(zip(source_texts, target_texts))
        
        cleaned_source, cleaned_target = self.clean_parallel_texts(source_texts, target_texts)
        
        # Create set of cleaned pairs for efficient lookup
        cleaned_pairs = set(zip(cleaned_source, cleaned_target))
        
        # Get filtered pairs (those in original but not in cleaned)
        filtered_pairs = [(src, tgt) for src, tgt in original_pairs if (src, tgt) not in cleaned_pairs]
        
        # Create output directories if they don't exist
        Path(output_source).parent.mkdir(parents=True, exist_ok=True)
        Path(output_target).parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Writing cleaned files: {output_source} and {output_target}")
        with open(output_source, 'w', encoding='utf-8') as src_f, \
             open(output_target, 'w', encoding='utf-8') as tgt_f:
            for src, tgt in zip(cleaned_source, cleaned_target):
                src_f.write(f"{src}\n")
                tgt_f.write(f"{tgt}\n")
        
        # Save filtered pairs if paths are provided
        if filtered_source and filtered_target:
            Path(filtered_source).parent.mkdir(parents=True, exist_ok=True)
            Path(filtered_target).parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Writing filtered files: {filtered_source} and {filtered_target}")
            with open(filtered_source, 'w', encoding='utf-8') as src_f, \
                 open(filtered_target, 'w', encoding='utf-8') as tgt_f:
                for src, tgt in filtered_pairs:
                    src_f.write(f"{src}\n")
                    tgt_f.write(f"{tgt}\n")
        
        # Save as JSON if output path is provided
        if json_output:
            logger.info(f"Writing JSON output to: {json_output}")
            json_data = []
            for src, tgt in zip(cleaned_source, cleaned_target):
                entry = {
                    "instruction": instruction or "",
                    "input": src,
                    "target": tgt
                }
                json_data.append(entry)
            
            Path(json_output).parent.mkdir(parents=True, exist_ok=True)
            with open(json_output, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        # Save statistics if output path is provided
        if stats_output:
            self.stats.save_to_json(stats_output)
                
        return len(source_texts), len(cleaned_source) 