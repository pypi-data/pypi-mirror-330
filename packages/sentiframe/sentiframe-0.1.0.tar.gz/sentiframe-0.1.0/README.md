# Sentiframe

A flexible framework for scraping and analyzing YouTube comments. This framework provides an easy-to-use interface for fetching comments and metadata from YouTube videos.

## Features

- Easy-to-use API for fetching YouTube comments
- Support for various YouTube URL formats (standard, shorts, embedded)
- Fetch video metadata (title, views, likes, etc.)
- Configurable comment limit
- Built-in error handling
- Extensible base scraper class for adding more platforms

## Installation

You can install the package using pip:

```bash
pip install sentiframe
```

For web interface support, install with web extras:
```bash
pip install sentiframe[web]
```

## Setup

1. Get a YouTube Data API key:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Create credentials (API key)
   - Copy the API key

2. Set up your API key:
   - Create a `.env` file in your project root
   - Add your API key:
     ```
     YOUTUBE_API_KEY=your_api_key_here
     ```
   - Or provide it directly when initializing the scraper

## Usage

### Basic Usage

```python
from sentiframe import YouTubeScraper

# Initialize the scraper
scraper = YouTubeScraper()  # Will use API key from .env
# Or provide API key directly:
# scraper = YouTubeScraper(api_key="your_api_key_here")

# Analyze a video
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
result = scraper.analyze_video(video_url, max_comments=50)

# Access metadata
print(f"Title: {result['metadata']['title']}")
print(f"Views: {result['metadata']['view_count']}")

# Access comments
for comment in result['comments']:
    print(f"Author: {comment['author']}")
    print(f"Text: {comment['text']}")
```

### Advanced Usage

```python
# Fetch metadata only
video_id = scraper.extract_id(video_url)
metadata = scraper.fetch_metadata(video_id)

# Fetch comments only
comments = scraper.fetch_comments(video_id, max_results=100)

# Clear stored data
scraper.clear()
```

## Extending the Framework

You can create your own scrapers by inheriting from the `BaseScraper` class:

```python
from sentiframe import BaseScraper

class MyCustomScraper(BaseScraper):
    def extract_id(self, url):
        # Implement ID extraction
        pass
        
    def fetch_comments(self, content_id, max_results=100):
        # Implement comment fetching
        pass
        
    def fetch_metadata(self, content_id):
        # Implement metadata fetching
        pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 