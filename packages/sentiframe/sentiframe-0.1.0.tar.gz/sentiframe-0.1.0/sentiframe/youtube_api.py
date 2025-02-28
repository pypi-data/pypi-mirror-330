"""
YouTube API handler for fetching video data and comments.
"""

import os
import re
from typing import Optional, Dict, List, Any
from googleapiclient.discovery import build
from dotenv import load_dotenv

class YouTubeAPI:
    """Handler for YouTube API operations."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the YouTube API handler.
        
        Args:
            api_key (str, optional): YouTube Data API key. If not provided, will try to load from .env
        """
        self.api_key = api_key or self._load_api_key()
        if not self.api_key:
            raise ValueError("YouTube API key is required. Please provide it or set YOUTUBE_API_KEY in .env file")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    @staticmethod
    def _load_api_key() -> Optional[str]:
        """Load API key from environment variables."""
        load_dotenv()
        return os.getenv('YOUTUBE_API_KEY')
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            str or None: Video ID if found, None otherwise
        """
        patterns = [
            r'(?:v=|/v/|youtu\.be/)([^"&?/\s]{11})',  # Standard YouTube URLs
            r'(?:embed/)([^"&?/\s]{11})',              # Embedded URLs
            r'(?:shorts/)([^"&?/\s]{11})'              # Shorts URLs
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_metadata(self, video_id: str) -> Dict[str, Any]:
        """Fetch video metadata from YouTube.
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video metadata including title, channel, views, likes, etc.
            
        Raises:
            ValueError: If video is not found or accessible
            Exception: For other API errors
        """
        try:
            response = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()
            
            if not response['items']:
                raise ValueError('Video not found or is not accessible')
                
            video = response['items'][0]
            snippet = video['snippet']
            statistics = video['statistics']
            
            return {
                'title': snippet['title'],
                'description': snippet['description'],
                'channel': snippet['channelTitle'],
                'published_at': snippet['publishedAt'],
                'view_count': statistics.get('viewCount', 0),
                'like_count': statistics.get('likeCount', 0),
                'comment_count': statistics.get('commentCount', 0)
            }
            
        except Exception as e:
            raise Exception(f'Failed to fetch video metadata: {str(e)}')
    
    def get_video_comments(self, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Fetch comments for a YouTube video.
        
        Args:
            video_id (str): YouTube video ID
            max_results (int, optional): Maximum number of comments to fetch. Defaults to 100.
            
        Returns:
            list: List of comment dictionaries containing author, text, likes, etc.
            
        Raises:
            Exception: If comments cannot be fetched
        """
        try:
            comments = []
            request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(max_results, 100),
                textFormat='plainText',
                order='time'
            )
            
            while request and len(comments) < max_results:
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'likes': comment['likeCount'],
                        'published_at': comment['publishedAt'],
                        'updated_at': comment.get('updatedAt', comment['publishedAt'])
                    })
                
                if len(comments) < max_results and 'nextPageToken' in response:
                    request = self.youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=min(max_results - len(comments), 100),
                        textFormat='plainText',
                        order='time',
                        pageToken=response['nextPageToken']
                    )
                else:
                    break
            
            return comments
            
        except Exception as e:
            raise Exception(f'Failed to fetch video comments: {str(e)}')
    
    def analyze_video(self, url: str, max_comments: int = 100) -> Dict[str, Any]:
        """Analyze a YouTube video by fetching its metadata and comments.
        
        Args:
            url (str): YouTube video URL
            max_comments (int, optional): Maximum number of comments to fetch. Defaults to 100.
            
        Returns:
            dict: Dictionary containing video metadata and comments
            
        Raises:
            ValueError: If URL is invalid or video is not accessible
            Exception: For other API errors
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            raise ValueError('Invalid YouTube URL')
            
        metadata = self.get_video_metadata(video_id)
        comments = self.get_video_comments(video_id, max_comments)
        
        return {
            'metadata': metadata,
            'comments': comments,
            'total_comments': len(comments)
        } 