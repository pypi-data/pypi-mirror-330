import os
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

from googleapiclient.discovery import build
from dotenv import load_dotenv

from .base_scraper import BaseScraper
from .utils import load_api_key

class YouTubeScraper(BaseScraper):
    """YouTube comments scraper implementation."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key or load_api_key()
        if not self.api_key:
            raise ValueError("YouTube API key is required. Please provide it or set it in .env file.")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def extract_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats."""
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
    
    def fetch_metadata(self, video_id: str) -> Dict[str, Any]:
        """Fetch video metadata."""
        try:
            response = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()
            
            if not response['items']:
                raise ValueError('Video not found or is not accessible.')
                
            video = response['items'][0]
            snippet = video['snippet']
            statistics = video['statistics']
            
            self.metadata = {
                'title': snippet['title'],
                'description': snippet['description'],
                'channel': snippet['channelTitle'],
                'published_at': snippet['publishedAt'],
                'view_count': statistics.get('viewCount', 0),
                'like_count': statistics.get('likeCount', 0),
                'comment_count': statistics.get('commentCount', 0)
            }
            
            return self.metadata
            
        except Exception as e:
            raise Exception(f'Failed to fetch video metadata: {str(e)}')
    
    def fetch_comments(self, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Fetch comments for a YouTube video."""
        try:
            self.comments = []
            request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(max_results, 100),
                textFormat='plainText',
                order='time'
            )
            
            while request and len(self.comments) < max_results:
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    self.comments.append({
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'likes': comment['likeCount'],
                        'published_at': comment['publishedAt'],
                        'updated_at': comment['updatedAt']
                    })
                
                if len(self.comments) < max_results and 'nextPageToken' in response:
                    request = self.youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=min(max_results - len(self.comments), 100),
                        textFormat='plainText',
                        order='time',
                        pageToken=response['nextPageToken']
                    )
                else:
                    break
            
            return self.comments
            
        except Exception as e:
            raise Exception(f'Failed to fetch video comments: {str(e)}')
    
    def analyze_video(self, url: str, max_comments: int = 100) -> Dict[str, Any]:
        """Analyze a YouTube video by fetching metadata and comments."""
        video_id = self.extract_id(url)
        if not video_id:
            raise ValueError('Invalid YouTube URL')
            
        metadata = self.fetch_metadata(video_id)
        comments = self.fetch_comments(video_id, max_comments)
        
        return {
            'metadata': metadata,
            'comments': comments,
            'total_comments': len(comments)
        } 