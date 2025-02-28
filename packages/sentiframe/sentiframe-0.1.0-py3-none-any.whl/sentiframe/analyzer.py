"""
Comment analysis functionality for YouTube comments.
"""

from typing import List, Dict, Any
import pandas as pd
from .youtube_api import YouTubeAPI

class CommentAnalyzer:
    """Analyzer for YouTube comments with various analysis features."""
    
    def __init__(self, api_key: str = None):
        """Initialize the comment analyzer.
        
        Args:
            api_key (str, optional): YouTube API key. If not provided, will try to load from .env
        """
        self.api = YouTubeAPI(api_key)
        
    def analyze_video(self, url: str, max_comments: int = 100) -> Dict[str, Any]:
        """Analyze comments from a YouTube video.
        
        Args:
            url (str): YouTube video URL
            max_comments (int, optional): Maximum number of comments to fetch. Defaults to 100.
            
        Returns:
            dict: Analysis results including metadata and processed comments
        """
        # Get raw data
        result = self.api.analyze_video(url, max_comments)
        
        # Convert comments to DataFrame for analysis
        df = pd.DataFrame(result['comments'])
        
        # Basic statistics
        stats = {
            'total_comments': len(df),
            'unique_authors': len(df['author'].unique()),
            'total_likes': df['likes'].sum(),
            'avg_likes': df['likes'].mean(),
            'most_liked_comment': df.loc[df['likes'].idxmax()].to_dict() if not df.empty else None,
            'most_active_author': df['author'].mode().iloc[0] if not df.empty else None,
            'author_comment_counts': df['author'].value_counts().to_dict()
        }
        
        return {
            'metadata': result['metadata'],
            'stats': stats,
            'comments': result['comments']
        }
    
    def get_top_comments(self, url: str, max_comments: int = 100, by: str = 'likes') -> List[Dict[str, Any]]:
        """Get top comments from a video sorted by specified criteria.
        
        Args:
            url (str): YouTube video URL
            max_comments (int, optional): Maximum number of comments to fetch. Defaults to 100.
            by (str, optional): Sort criteria ('likes' or 'date'). Defaults to 'likes'.
            
        Returns:
            list: Sorted list of comments
        """
        result = self.api.analyze_video(url, max_comments)
        df = pd.DataFrame(result['comments'])
        
        if by == 'likes':
            df = df.sort_values('likes', ascending=False)
        elif by == 'date':
            df = df.sort_values('published_at', ascending=False)
            
        return df.to_dict('records')
    
    def filter_comments(self, url: str, author: str = None, min_likes: int = None, 
                       max_comments: int = 100) -> List[Dict[str, Any]]:
        """Filter comments based on various criteria.
        
        Args:
            url (str): YouTube video URL
            author (str, optional): Filter by author name
            min_likes (int, optional): Minimum number of likes
            max_comments (int, optional): Maximum number of comments to fetch. Defaults to 100.
            
        Returns:
            list: Filtered list of comments
        """
        result = self.api.analyze_video(url, max_comments)
        df = pd.DataFrame(result['comments'])
        
        if author:
            df = df[df['author'] == author]
        if min_likes is not None:
            df = df[df['likes'] >= min_likes]
            
        return df.to_dict('records') 