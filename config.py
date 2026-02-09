# ========================================
# YouTube Competitor Analysis Configuration
# Using ScrapingDog API
# ========================================

import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    """Configuration for YouTube Competitor Analysis Automation"""
    
    # ============== ScrapingDog API ==============
    SCRAPINGDOG_API_KEY: str = os.getenv("SCRAPINGDOG_API_KEY")
    SCRAPINGDOG_BASE_URL: str = "https://api.scrapingdog.com/youtube"
    
    # ============== Search Queries for AI Niche ==============
    # These queries will be used to find trending videos in your niche
    SEARCH_QUERIES: List[str] = field(default_factory=lambda: [
        "AI tools 2024",
        "ChatGPT tutorial",
        "no code automation",
        "AI automation business",
        "startup ideas 2024",
        "make money with AI",
        "best AI tools",
        "AI agents tutorial",
        "no code app builder",
        "AI for beginners",
        "passive income AI",
        "Claude AI tutorial",
        "Midjourney tutorial",
        "automation tools",
        "solopreneur AI tools"
    ])
    
    # ============== Competitor Channels to Monitor ==============
    # These are popular AI/No-code/Automation YouTube channels
    COMPETITOR_CHANNELS: List[str] = field(default_factory=lambda: [
        "Matt Wolfe",          # AI tools reviews
        "All About AI",        # AI tutorials
        "AI Advantage",        # AI for business
        "Income stream surfers",  # AI money making
        "Liam Ottley",         # AI agency
        "AI Jason",            # AI tools
        "Skills Factory",      # No-code
        "Tina Huang",          # Tech/AI
        "Greg Isenberg",       # Startup ideas
        "My First Million",    # Business ideas
    ])
    
    # ============== Your Channel ==============
    YOUR_CHANNEL: str = "The Solo Entrepreneur"
    
    # ============== Outperformance Criteria ==============
    # Minimum views to be considered "outperforming" 
    MIN_VIEWS_THRESHOLD: int = 50000  # 50K+ views
    
    # Only analyze videos published in the last N days
    DAYS_TO_ANALYZE: int = 14  # Focus on recent videos
    
    # ============== Email Configuration (Gmail App Password) ==============
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECIPIENT: str = os.getenv("EMAIL_RECIPIENT")
    
    # ============== Logging ==============
    LOG_FILE: str = "youtube_analyzer.log"
    LOG_DIR: str = "logs"


# Create default config instance
config = Config()
