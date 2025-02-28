"""
Sentiframe - A YouTube Comment Analysis Framework
"""

from .youtube_api import YouTubeAPI
from .analyzer import CommentAnalyzer

__version__ = "0.1.0"
__author__ = "Ayush Rawat"

__all__ = ['YouTubeAPI', 'CommentAnalyzer'] 