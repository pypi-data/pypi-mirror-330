"""Configuration classes for text cleaning operations."""

from dataclasses import dataclass
import torch


@dataclass
class CleaningConfig:
    """Configuration for text cleaning operations.
    
    This class defines all the parameters that control the text cleaning process,
    including length constraints, statistical outlier detection, and domain filtering.
    
    Attributes:
        min_chars: Minimum number of characters for a text to be valid
        max_chars: Maximum number of characters for a text to be valid
        min_words: Minimum number of words for a text to be valid
        max_words: Maximum number of words for a text to be valid
        contamination: Expected proportion of statistical outliers
        random_state: Random seed for reproducibility
        remove_urls: Whether to remove URLs from texts
        remove_emails: Whether to remove email addresses from texts
        normalize_unicode: Whether to normalize Unicode characters
        remove_control_chars: Whether to remove control characters
        lowercase: Whether to convert texts to lowercase
        remove_extra_whitespace: Whether to normalize whitespace
        enable_domain_filtering: Whether to enable domain-based filtering
        embedding_model: Name of the sentence transformer model to use
        domain_contamination: Expected proportion of domain outliers
        batch_size: Batch size for embedding generation
        device: Device to use for embedding generation (cuda or cpu)
    """
    
    # Length-based cleaning
    min_chars: int = 1
    max_chars: int = 1000
    min_words: int = 1
    max_words: int = 150
    
    # Statistical outlier detection
    contamination: float = 0.1  # Expected proportion of outliers
    random_state: int = 42  # For reproducibility
    
    # Symbol cleaning
    remove_urls: bool = True
    remove_emails: bool = True
    normalize_unicode: bool = True
    remove_control_chars: bool = True
    
    # Additional options
    lowercase: bool = False
    remove_extra_whitespace: bool = True

    # Domain filtering options
    enable_domain_filtering: bool = False
    embedding_model: str = "all-MiniLM-L6-v2"  # Default lightweight model
    domain_contamination: float = 0.1  # Expected proportion of domain outliers
    batch_size: int = 32  # Batch size for embedding generation
    device: str = "cuda" if torch.cuda.is_available() else "cpu"  # Device for embedding generation
    
    @classmethod
    def from_dict(cls, config_dict=None):
        """Create a configuration from a dictionary.
        
        Args:
            config_dict: Dictionary of configuration parameters
            
        Returns:
            CleaningConfig: Configuration object
        """
        if config_dict is None:
            return cls()
        
        # Filter out any keys that are not valid parameters
        valid_params = {k: v for k, v in config_dict.items() 
                       if k in cls.__annotations__}
        
        return cls(**valid_params) 