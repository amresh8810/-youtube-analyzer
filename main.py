#!/usr/bin/env python3
# ========================================
# YouTube Competitor Analysis Automation
# Main Entry Point
# ========================================
"""
Daily YouTube Competitor Analysis Automation for AI/Automation Niche

Features:
- Searches for viral videos using ScrapingDog YouTube API
- Identifies outperforming content (50K+ views, posted in last 14 days)
- Tracks specific competitor channels
- Sends beautiful HTML email reports

Usage:
    python main.py                    # Run full analysis and send email
    python main.py --dry-run          # Analyze without sending email
    python main.py --test-email       # Send a test email
    
Environment Variables:
    SCRAPINGDOG_API_KEY  - Your ScrapingDog API key (already configured)
    EMAIL_SENDER         - Gmail address to send from
    EMAIL_PASSWORD       - Gmail App Password
    EMAIL_RECIPIENT      - Email address to receive reports
"""

import argparse
import logging
import sys
import os
import io
from datetime import datetime
from typing import Optional

# Fix Windows console encoding for Unicode characters (emojis)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from youtube_analyzer import YouTubeAnalyzer, get_outperforming_videos
from email_sender import send_outperforming_videos_report, EmailSender

# Setup logging
os.makedirs(config.LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(config.LOG_DIR, config.LOG_FILE)),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print a cool banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🎯  YouTube Competitor Video Analyzer  🎯                      ║
║                                                                  ║
║   Find outperforming videos in the AI/Automation niche           ║
║   Built for @thesoloentrepreneur07                               ║
║                                                                  ║
║   Powered by ScrapingDog YouTube API                             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def validate_config(check_email: bool = True) -> bool:
    """Validate that all required configuration is present"""
    errors = []
    warnings = []
    
    # Check ScrapingDog API
    if not config.SCRAPINGDOG_API_KEY or config.SCRAPINGDOG_API_KEY == "YOUR_API_KEY_HERE":
        errors.append("❌ SCRAPINGDOG_API_KEY is not set")
        
    # Check email config only if needed
    if check_email:
        if not config.EMAIL_SENDER:
            errors.append("❌ EMAIL_SENDER is not set")
            
        if not config.EMAIL_PASSWORD:
            errors.append("❌ EMAIL_PASSWORD is not set")
            
        if not config.EMAIL_RECIPIENT:
            errors.append("❌ EMAIL_RECIPIENT is not set")
            
    # Check search queries
    if not config.SEARCH_QUERIES:
        warnings.append("⚠️  No search queries configured")
        
    if errors:
        print("\n🚨 CONFIGURATION ERRORS:")
        for error in errors:
            print(f"   {error}")
        print("\n📝 Please set environment variables or update config.py")
        print("   For Gmail: Create an App Password at https://myaccount.google.com/apppasswords")
        return False
        
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
            
    return True


def run_analysis(dry_run: bool = False) -> bool:
    """
    Run the full analysis pipeline
    
    Args:
        dry_run: If True, skip sending email
        
    Returns:
        True if successful, False otherwise
    """
    print_banner()
    
    start_time = datetime.now()
    logger.info(f"🕐 Starting analysis at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Validate configuration
    if not validate_config(check_email=not dry_run):
        return False
        
    print("\n" + "="*60)
    print("🔍 SEARCHING FOR VIRAL VIDEOS...")
    print("="*60)
    
    # Step 2: Analyze YouTube
    try:
        all_videos, competitor_videos = get_outperforming_videos()
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    # Step 3: Print results summary
    print("\n" + "="*60)
    print("📈 ANALYSIS RESULTS")
    print("="*60)
    
    if not all_videos:
        print("\n😔 No outperforming videos found today.")
        print("   This could mean:")
        print("   - API quota might be exceeded")
        print("   - Thresholds might be too high (check config.py)")
        print("   - Network issues")
    else:
        print(f"\n🎉 Found {len(all_videos)} outperforming videos!\n")
        
        print("📊 TOP 5 VIDEOS TODAY:")
        print("-" * 50)
        for i, video in enumerate(all_videos[:5], 1):
            print(f"\n{i}. {video.title[:55]}...")
            print(f"   👤 {video.channel_name}")
            print(f"   👁️ {video.view_count:,} views | 📅 {video.published_date}")
            print(f"   🔗 {video.video_url}")
            
        if competitor_videos:
            print(f"\n\n📺 COMPETITOR BREAKDOWN:")
            print("-" * 50)
            for channel, videos in competitor_videos.items():
                print(f"\n🎯 {channel}: {len(videos)} videos")
                for video in videos[:2]:
                    print(f"   • {video.title[:45]}... ({video.view_count:,} views)")
                
    # Step 4: Send email report
    if dry_run:
        logger.info("🔄 DRY RUN mode - skipping email")
        print("\n📧 DRY RUN: Email not sent")
        print("   Run without --dry-run to send the email report")
    elif all_videos:
        print("\n📧 Sending email report...")
        success = send_outperforming_videos_report(all_videos, competitor_videos)
        
        if success:
            print(f"\n✅ Email report sent to {config.EMAIL_RECIPIENT}")
        else:
            print("\n❌ Failed to send email report. Check logs for details.")
            return False
    else:
        logger.info("📭 No videos found - skipping email")
        
    # Done!
    end_time = datetime.now()
    duration = (end_time - start_time).seconds
    
    print(f"\n⏱️  Analysis completed in {duration} seconds")
    print("="*60)
    logger.info(f"✅ Analysis completed in {duration} seconds")
    
    return True


def test_email() -> bool:
    """Send a test email to verify configuration"""
    print_banner()
    print("\n📧 TESTING EMAIL CONFIGURATION...")
    print("="*60)
    
    if not validate_config(check_email=True):
        return False
        
    # Import test data
    from youtube_analyzer import VideoData
    
    test_videos = [
        VideoData(
            video_id="tKr6bj2sWBo",
            title="🤖 5 AI Tools That Will BLOW Your Mind in 2024",
            channel_name="AI Advantage",
            channel_link="https://youtube.com/@aiadvantage",
            published_date="1 day ago",
            view_count=325000,
            video_url="https://www.youtube.com/watch?v=tKr6bj2sWBo",
            thumbnail_url="https://i.ytimg.com/vi/tKr6bj2sWBo/hqdefault.jpg",
            length="15:42",
            is_verified=True
        ),
        VideoData(
            video_id="abc123xyz",
            title="No-Code Automation: Build Your First AI Agent Today",
            channel_name="Skills Factory",
            channel_link="https://youtube.com/@skillsfactory",
            published_date="2 days ago",
            view_count=89000,
            video_url="https://www.youtube.com/watch?v=abc123xyz",
            thumbnail_url="https://i.ytimg.com/vi/abc123xyz/hqdefault.jpg",
            length="28:15",
            is_verified=False
        ),
    ]
    
    test_competitors = {"AI Advantage": [test_videos[0]]}
    
    print("📝 Sending test email...")
    success = send_outperforming_videos_report(test_videos, test_competitors)
    
    if success:
        print(f"\n✅ Test email sent successfully to {config.EMAIL_RECIPIENT}")
        print("   Check your inbox (and spam folder)!")
    else:
        print("\n❌ Failed to send test email. Check the error messages above.")
        
    return success


def main():
    """Main entry point with CLI argument parsing"""
    
    parser = argparse.ArgumentParser(
        description='🎯 YouTube Competitor Video Analyzer for AI/Automation Niche',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    Full analysis with email
  python main.py --dry-run          Test without sending email  
  python main.py --test-email       Send a test email

Environment Variables:
  EMAIL_SENDER        Your Gmail address
  EMAIL_PASSWORD      Gmail App Password (not regular password!)
  EMAIL_RECIPIENT     Where to send reports
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run analysis without sending email'
    )
    
    parser.add_argument(
        '--test-email',
        action='store_true',
        help='Send a test email to verify configuration'
    )
    
    args = parser.parse_args()
    
    if args.test_email:
        success = test_email()
    else:
        success = run_analysis(dry_run=args.dry_run)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
