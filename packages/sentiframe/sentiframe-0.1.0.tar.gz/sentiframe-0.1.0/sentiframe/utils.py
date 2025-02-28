import os
from typing import Optional
from dotenv import load_dotenv

def load_api_key() -> Optional[str]:
    """Load YouTube API key from environment variables."""
    load_dotenv()
    return os.getenv('YOUTUBE_API_KEY')

def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to a more readable format."""
    from datetime import datetime
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S') 