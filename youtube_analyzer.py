# ========================================
# YouTube Competitor Video Analyzer
# Using ScrapingDog API
# ========================================

import logging
import re
import sys
import io
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import os

from config import config

# Setup logging with UTF-8 encoding for Windows
os.makedirs(config.LOG_DIR, exist_ok=True)

# Create handlers with proper encoding
file_handler = logging.FileHandler(os.path.join(config.LOG_DIR, config.LOG_FILE), encoding='utf-8')
stream_handler = logging.StreamHandler(sys.stdout if sys.platform != 'win32' else io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger(__name__)


@dataclass
class VideoData:
    """Represents a YouTube video with its statistics"""
    video_id: str
    title: str
    channel_name: str
    channel_link: str
    published_date: str  # e.g., "2 days ago", "1 week ago"
    view_count: int
    video_url: str
    thumbnail_url: str
    description: str = ""
    length: str = ""
    is_verified: bool = False
    
    def __str__(self):
        return f"{self.title} ({self.view_count:,} views) - {self.channel_name}"


class ScrapingDogYouTubeAPI:
    """Interface to ScrapingDog YouTube API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.SCRAPINGDOG_API_KEY
        self.base_url = config.SCRAPINGDOG_BASE_URL
        
    def search(self, query: str, country: str = "us") -> Dict:
        """
        Search YouTube using ScrapingDog API
        
        Args:
            query: Search query string
            country: Country code (default: us)
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/search"
        params = {
            "api_key": self.api_key,
            "search_query": query,  # ScrapingDog uses 'search_query' not 'query'
            "country": country
        }
        
        try:
            logger.info(f"🔍 Searching: '{query}'")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API error for query '{query}': {e}")
            return {}
            
    def parse_views(self, views_str: str) -> int:
        """
        Parse view count string to integer
        e.g., "1,234,567 views" -> 1234567
        e.g., "1.2M views" -> 1200000
        """
        if not views_str:
            return 0
            
        # Remove "views" and clean up
        views_str = views_str.lower().replace("views", "").strip()
        views_str = views_str.replace(",", "")
        
        try:
            # Handle K, M, B suffixes
            if "k" in views_str:
                return int(float(views_str.replace("k", "")) * 1000)
            elif "m" in views_str:
                return int(float(views_str.replace("m", "")) * 1000000)
            elif "b" in views_str:
                return int(float(views_str.replace("b", "")) * 1000000000)
            else:
                return int(float(views_str))
        except (ValueError, TypeError):
            return 0
            
    def parse_published_date_to_days(self, date_str: str) -> int:
        """
        Convert published date string to days ago
        e.g., "2 days ago" -> 2
        e.g., "1 week ago" -> 7
        e.g., "3 months ago" -> 90
        """
        if not date_str:
            return 999  # Unknown, treat as old
            
        date_str = date_str.lower().strip()
        
        try:
            # Extract number
            numbers = re.findall(r'\d+', date_str)
            if not numbers:
                return 999
            num = int(numbers[0])
            
            if "hour" in date_str:
                return 0  # Same day
            elif "day" in date_str:
                return num
            elif "week" in date_str:
                return num * 7
            elif "month" in date_str:
                return num * 30
            elif "year" in date_str:
                return num * 365
            else:
                return 999
        except:
            return 999
            
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        if not url:
            return ""
        # Pattern: youtube.com/watch?v=VIDEO_ID
        match = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})', url)
        return match.group(1) if match else ""
        

class YouTubeAnalyzer:
    """Analyzes YouTube for outperforming videos in AI/Automation niche"""
    
    def __init__(self):
        self.api = ScrapingDogYouTubeAPI()
        self.found_videos: Dict[str, VideoData] = {}  # video_id -> VideoData
        
    def _process_video_results(self, results: List[Dict]) -> List[VideoData]:
        """Process raw API results into VideoData objects"""
        videos = []
        
        for item in results:
            try:
                video_url = item.get("link", "")
                video_id = self.api.extract_video_id(video_url)
                
                if not video_id or video_id in self.found_videos:
                    continue  # Skip duplicates
                    
                # Parse view count
                view_count = self.api.parse_views(item.get("views", "0"))
                
                # Parse published date
                published_date = item.get("published_date", "")
                days_ago = self.api.parse_published_date_to_days(published_date)
                
                # Filter: Only recent videos with good views
                if days_ago > config.DAYS_TO_ANALYZE:
                    continue
                    
                if view_count < config.MIN_VIEWS_THRESHOLD:
                    continue
                    
                # Get channel info
                channel_info = item.get("channel", {})
                channel_name = channel_info.get("name", "Unknown")
                channel_link = channel_info.get("link", "")
                is_verified = channel_info.get("verified", False)
                
                # Get thumbnail
                thumbnail = item.get("thumbnail", {})
                thumbnail_url = thumbnail.get("static", "") if isinstance(thumbnail, dict) else str(thumbnail)
                
                video = VideoData(
                    video_id=video_id,
                    title=item.get("title", "Untitled"),
                    channel_name=channel_name,
                    channel_link=channel_link,
                    published_date=published_date,
                    view_count=view_count,
                    video_url=video_url,
                    thumbnail_url=thumbnail_url,
                    description=item.get("description", ""),
                    length=item.get("length", ""),
                    is_verified=is_verified
                )
                
                videos.append(video)
                self.found_videos[video_id] = video
                
                logger.info(f"  ✓ Found: {video.title[:50]}... ({view_count:,} views, {published_date})")
                
            except Exception as e:
                logger.warning(f"Error processing video: {e}")
                continue
                
        return videos
        
    def search_niche_videos(self) -> List[VideoData]:
        """Search for outperforming videos using configured queries"""
        all_videos = []
        
        logger.info(f"🚀 Starting search with {len(config.SEARCH_QUERIES)} queries...")
        
        for query in config.SEARCH_QUERIES:
            try:
                response = self.api.search(query)
                
                # Process all video sections in the response
                video_sections = [
                    "video_results",
                    "popular_today", 
                    "channels_new_to_you",
                    "from_related_searches"
                ]
                
                for section in video_sections:
                    if section in response:
                        videos = self._process_video_results(response[section])
                        all_videos.extend(videos)
                        
            except Exception as e:
                logger.error(f"Error searching '{query}': {e}")
                continue
                
        # Remove duplicates and sort by views
        unique_videos = list(self.found_videos.values())
        unique_videos.sort(key=lambda x: x.view_count, reverse=True)
        
        logger.info(f"📊 Found {len(unique_videos)} unique outperforming videos")
        return unique_videos
        
    def filter_by_competitor_channels(self, videos: List[VideoData]) -> Dict[str, List[VideoData]]:
        """Group videos by whether they're from competitor channels"""
        competitor_videos = {}
        
        for video in videos:
            # Check if channel matches any competitor
            channel_lower = video.channel_name.lower()
            
            for competitor in config.COMPETITOR_CHANNELS:
                if competitor.lower() in channel_lower or channel_lower in competitor.lower():
                    if competitor not in competitor_videos:
                        competitor_videos[competitor] = []
                    competitor_videos[competitor].append(video)
                    break
                    
        return competitor_videos
        
    def analyze(self) -> Tuple[List[VideoData], Dict[str, List[VideoData]]]:
        """
        Run full analysis
        
        Returns:
            Tuple of (all_outperforming_videos, competitor_videos_dict)
        """
        logger.info("="*60)
        logger.info("🎬 YOUTUBE COMPETITOR ANALYSIS")
        logger.info("="*60)
        
        # Search for all high-performing videos
        all_videos = self.search_niche_videos()
        
        # Filter by competitor channels
        competitor_videos = self.filter_by_competitor_channels(all_videos)
        
        logger.info(f"\n📈 Summary:")
        logger.info(f"   Total outperforming videos: {len(all_videos)}")
        logger.info(f"   From tracked competitors: {sum(len(v) for v in competitor_videos.values())}")
        
        return all_videos, competitor_videos


def get_outperforming_videos() -> Tuple[List[VideoData], Dict[str, List[VideoData]]]:
    """Main entry point to get all outperforming videos"""
    analyzer = YouTubeAnalyzer()
    return analyzer.analyze()


if __name__ == "__main__":
    # Test run
    all_videos, competitor_videos = get_outperforming_videos()
    
    print("\n" + "="*60)
    print("🚀 OUTPERFORMING VIDEOS REPORT")
    print("="*60)
    
    print(f"\n📊 TOP 10 VIDEOS IN AI/AUTOMATION NICHE:\n")
    for i, video in enumerate(all_videos[:10], 1):
        print(f"{i}. {video.title[:60]}...")
        print(f"   Channel: {video.channel_name}")
        print(f"   Views: {video.view_count:,} | Published: {video.published_date}")
        print(f"   URL: {video.video_url}")
        print()
        
    if competitor_videos:
        print("\n" + "="*60)
        print("📺 COMPETITOR CHANNEL BREAKDOWN")
        print("="*60)
        
        for channel, videos in competitor_videos.items():
            print(f"\n🎯 {channel} ({len(videos)} videos)")
            print("-" * 40)
            for video in videos[:3]:
                print(f"   • {video.title[:50]}... ({video.view_count:,} views)")
