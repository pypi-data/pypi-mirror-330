from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseScraper(ABC):
    """Base class for all scrapers in the framework."""
    
    def __init__(self):
        self.comments = []
        self.metadata = {}
    
    @abstractmethod
    def extract_id(self, url: str) -> Optional[str]:
        """Extract the content ID from the given URL."""
        pass
    
    @abstractmethod
    def fetch_comments(self, content_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Fetch comments for the given content ID."""
        pass
    
    @abstractmethod
    def fetch_metadata(self, content_id: str) -> Dict[str, Any]:
        """Fetch metadata for the given content ID."""
        pass
    
    def clear(self):
        """Clear stored comments and metadata."""
        self.comments = []
        self.metadata = {} 