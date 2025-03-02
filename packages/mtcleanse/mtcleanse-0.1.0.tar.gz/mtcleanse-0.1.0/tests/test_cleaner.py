"""Tests for the mtcleanse.cleaning module."""

import unittest
from pathlib import Path
import tempfile
import shutil

from mtcleanse.cleaning import ParallelTextCleaner, CleaningConfig


class TestParallelTextCleaner(unittest.TestCase):
    """Test the ParallelTextCleaner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.test_dir = Path(tempfile.mkdtemp())
        
        # Create test files
        self.source_file = self.test_dir / "source.txt"
        self.target_file = self.test_dir / "target.txt"
        
        # Sample data with some noise
        self.source_texts = [
            "This is a normal sentence.",
            "This is a very long sentence that exceeds the default maximum length limit for testing purposes. " * 10,
            "Short.",
            "http://example.com",
            "Email: test@example.com",
            "Normal sentence with some control chars: \x00\x01\x02",
            "Another normal sentence."
        ]
        
        self.target_texts = [
            "Dies ist ein normaler Satz.",
            "Dies ist ein sehr langer Satz, der die standardmäßige maximale Längenbegrenzung zu Testzwecken überschreitet. " * 10,
            "Kurz.",
            "http://beispiel.de",
            "E-Mail: test@beispiel.de",
            "Normaler Satz mit einigen Steuerzeichen: \x00\x01\x02",
            "Ein weiterer normaler Satz."
        ]
        
        # Write test files
        with open(self.source_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.source_texts))
        
        with open(self.target_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.target_texts))
        
        # Create cleaner with default config
        self.cleaner = ParallelTextCleaner()
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_clean_texts(self):
        """Test cleaning texts directly."""
        cleaned_source, cleaned_target = self.cleaner.clean_texts(
            self.source_texts, self.target_texts
        )
        
        # Check that some texts were filtered out
        self.assertLess(len(cleaned_source), len(self.source_texts))
        self.assertEqual(len(cleaned_source), len(cleaned_target))
        
        # Check that URLs and emails were removed
        for text in cleaned_source + cleaned_target:
            self.assertNotIn("http://", text)
            self.assertNotIn("@", text)
    
    def test_clean_files(self):
        """Test cleaning files."""
        output_source = self.test_dir / "clean_source.txt"
        output_target = self.test_dir / "clean_target.txt"
        
        original_count, cleaned_count = self.cleaner.clean_files(
            self.source_file,
            self.target_file,
            output_source,
            output_target
        )
        
        # Check that some texts were filtered out
        self.assertEqual(original_count, len(self.source_texts))
        self.assertLess(cleaned_count, original_count)
        
        # Check that output files were created
        self.assertTrue(output_source.exists())
        self.assertTrue(output_target.exists())
        
        # Check that output files have the same number of lines
        with open(output_source, "r", encoding="utf-8") as f:
            source_lines = f.readlines()
        
        with open(output_target, "r", encoding="utf-8") as f:
            target_lines = f.readlines()
        
        self.assertEqual(len(source_lines), len(target_lines))
        self.assertEqual(len(source_lines), cleaned_count)
    
    def test_custom_config(self):
        """Test cleaner with custom configuration."""
        # Create cleaner with custom config
        config = {
            "min_chars": 10,
            "max_chars": 100,  # Increased to allow longer sentences
            "min_words": 3,
            "max_words": 15,   # Increased to allow more words
            "remove_urls": False,  # Don't remove URLs
            "remove_emails": False,  # Don't remove emails
            "contamination": 0.01  # Lower contamination to avoid filtering out our test sentences
        }
        
        # Create test texts with URLs and emails in normal sentences that won't be filtered out
        test_source = [
            "This is a normal sentence with http://example.com URL.",
            "This is a normal sentence with test@example.com email address."
        ]
        
        test_target = [
            "Dies ist ein normaler Satz mit http://beispiel.de URL.",
            "Dies ist ein normaler Satz mit test@beispiel.de E-Mail-Adresse."
        ]
        
        custom_cleaner = ParallelTextCleaner(config)
        
        # Print the configuration to verify
        print(f"Custom config: {custom_cleaner.config}")
        
        # Print the original texts
        print("Original texts:")
        for i, text in enumerate(test_source):
            print(f"{i}: {text}")
        
        cleaned_source, cleaned_target = custom_cleaner.clean_texts(
            test_source, test_target
        )
        
        # Print the cleaned texts
        print("Cleaned texts:")
        for i, text in enumerate(cleaned_source):
            print(f"{i}: {text}")
        
        # Check that URLs and emails were not removed
        url_found = False
        email_found = False
        
        for text in cleaned_source:
            if "http://" in text:
                url_found = True
            if "@" in text:
                email_found = True
        
        if not url_found:
            self.fail("URLs were removed despite configuration")
            
        if not email_found:
            self.fail("Email addresses were removed despite configuration")
    
    def test_get_stats(self):
        """Test getting statistics."""
        self.cleaner.clean_texts(self.source_texts, self.target_texts)
        stats = self.cleaner.get_stats()
        
        # Check that stats contains expected keys
        self.assertIn("total_pairs", stats)
        self.assertIn("final_pairs", stats)
        self.assertIn("length_stats", stats)
        
        # Check that stats values are correct
        self.assertEqual(stats["total_pairs"], len(self.source_texts))
        self.assertLess(stats["final_pairs"], stats["total_pairs"])


if __name__ == "__main__":
    unittest.main() 