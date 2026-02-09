# ========================================
# Email Report Sender
# Beautiful HTML Email Reports
# ========================================

import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List

from config import config
from youtube_analyzer import VideoData

logger = logging.getLogger(__name__)


class EmailSender:
    """Sends beautifully formatted email reports"""
    
    def __init__(self):
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.sender_email = config.EMAIL_SENDER
        self.sender_password = config.EMAIL_PASSWORD
        self.recipient_email = config.EMAIL_RECIPIENT
        
    def _generate_html_report(
        self, 
        all_videos: List[VideoData], 
        competitor_videos: Dict[str, List[VideoData]]
    ) -> str:
        """Generate a beautiful HTML email report"""
        
        date_str = datetime.now().strftime("%B %d, %Y")
        total_videos = len(all_videos)
        competitor_count = sum(len(v) for v in competitor_videos.values())
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0a0a0f;">
    <div style="max-width: 700px; margin: 0 auto; padding: 20px;">
        
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%); border-radius: 20px; padding: 40px 30px; text-align: center; margin-bottom: 24px; box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);">
            <h1 style="color: white; margin: 0; font-size: 32px; font-weight: 800; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                🎯 AI Niche Video Report
            </h1>
            <p style="color: rgba(255,255,255,0.95); margin: 12px 0 0 0; font-size: 18px; font-weight: 500;">
                {date_str}
            </p>
            <div style="margin-top: 20px; display: flex; justify-content: center; gap: 20px;">
                <div style="background: rgba(255,255,255,0.2); border-radius: 12px; padding: 15px 25px;">
                    <div style="color: white; font-size: 28px; font-weight: 700;">{total_videos}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Viral Videos</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); border-radius: 12px; padding: 15px 25px;">
                    <div style="color: white; font-size: 28px; font-weight: 700;">{len(competitor_videos)}</div>
                    <div style="color: rgba(255,255,255,0.9); font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Competitors</div>
                </div>
            </div>
        </div>
        
        <!-- Quick Stats -->
        <div style="background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); border-radius: 16px; padding: 24px; margin-bottom: 24px; border: 1px solid rgba(99, 102, 241, 0.2);">
            <h2 style="color: #a78bfa; margin: 0 0 16px 0; font-size: 16px; text-transform: uppercase; letter-spacing: 2px;">📊 Daily Insights</h2>
            <p style="color: #e2e8f0; margin: 0; font-size: 15px; line-height: 1.7;">
                Found <span style="color: #22d3ee; font-weight: 700;">{total_videos} outperforming videos</span> in the AI/Automation niche today.
                {f'<span style="color: #34d399; font-weight: 700;">{competitor_count} videos</span> are from your tracked competitors.' if competitor_count > 0 else ''}
            </p>
        </div>
"""

        # Top Videos Section
        html += """
        <!-- Top Videos Section -->
        <div style="background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); border-radius: 16px; padding: 24px; margin-bottom: 24px; border: 1px solid rgba(99, 102, 241, 0.2);">
            <h2 style="color: #f472b6; margin: 0 0 20px 0; font-size: 18px; border-bottom: 1px solid rgba(244, 114, 182, 0.3); padding-bottom: 12px;">
                🔥 Top Performing Videos Today
            </h2>
"""
        
        for i, video in enumerate(all_videos[:8], 1):
            # Color based on view count
            if video.view_count >= 500000:
                badge_color = "#ef4444"  # Red for 500K+
                badge_text = "🔥 VIRAL"
            elif video.view_count >= 200000:
                badge_color = "#f59e0b"  # Orange for 200K+
                badge_text = "⚡ HOT"
            else:
                badge_color = "#22d3ee"  # Cyan for 50K+
                badge_text = "📈 RISING"
            
            verified_badge = '<span style="color: #3b82f6; margin-left: 4px;">✓</span>' if video.is_verified else ''
            
            html += f"""
            <div style="background: rgba(15, 15, 26, 0.8); border-radius: 12px; padding: 16px; margin-bottom: 12px; border: 1px solid rgba(99, 102, 241, 0.1); transition: all 0.3s ease;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="width: 140px; vertical-align: top; padding-right: 16px;">
                            <a href="{video.video_url}" style="text-decoration: none;">
                                <img src="{video.thumbnail_url}" alt="Thumbnail" style="width: 140px; height: 79px; border-radius: 10px; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                            </a>
                        </td>
                        <td style="vertical-align: top;">
                            <div style="margin-bottom: 8px;">
                                <span style="background: {badge_color}; color: white; padding: 3px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;">
                                    {badge_text}
                                </span>
                                <span style="color: #64748b; font-size: 12px; margin-left: 10px;">{video.length}</span>
                            </div>
                            <a href="{video.video_url}" style="color: #f1f5f9; text-decoration: none; font-size: 14px; font-weight: 600; line-height: 1.4; display: block; margin-bottom: 8px;">
                                {video.title[:75]}{'...' if len(video.title) > 75 else ''}
                            </a>
                            <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
                                <span style="color: #94a3b8; font-size: 12px;">
                                    {video.channel_name}{verified_badge}
                                </span>
                                <span style="color: #22d3ee; font-size: 12px; font-weight: 600;">
                                    👁️ {video.view_count:,} views
                                </span>
                                <span style="color: #94a3b8; font-size: 12px;">
                                    📅 {video.published_date}
                                </span>
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
"""
        
        html += "        </div>\n"
        
        # Competitor Section (if any)
        if competitor_videos:
            html += """
        <!-- Competitor Breakdown -->
        <div style="background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); border-radius: 16px; padding: 24px; margin-bottom: 24px; border: 1px solid rgba(99, 102, 241, 0.2);">
            <h2 style="color: #34d399; margin: 0 0 20px 0; font-size: 18px; border-bottom: 1px solid rgba(52, 211, 153, 0.3); padding-bottom: 12px;">
                📺 Competitor Spotlight
            </h2>
"""
            for channel, videos in competitor_videos.items():
                html += f"""
            <div style="margin-bottom: 20px;">
                <h3 style="color: #a78bfa; margin: 0 0 12px 0; font-size: 15px;">
                    🎯 {channel} <span style="color: #64748b; font-weight: 400;">({len(videos)} videos)</span>
                </h3>
"""
                for video in videos[:2]:
                    html += f"""
                <a href="{video.video_url}" style="display: block; background: rgba(15, 15, 26, 0.6); border-radius: 8px; padding: 12px; margin-bottom: 8px; text-decoration: none; border: 1px solid rgba(99, 102, 241, 0.1);">
                    <div style="color: #e2e8f0; font-size: 13px; font-weight: 500; margin-bottom: 4px;">{video.title[:60]}...</div>
                    <div style="color: #22d3ee; font-size: 12px;">👁️ {video.view_count:,} views • {video.published_date}</div>
                </a>
"""
                html += "            </div>\n"
            html += "        </div>\n"
        
        # Content Ideas Section
        html += """
        <!-- Content Ideas -->
        <div style="background: linear-gradient(135deg, #1e3a5f 0%, #1a1a2e 100%); border-radius: 16px; padding: 24px; margin-bottom: 24px; border: 1px solid rgba(99, 102, 241, 0.2);">
            <h3 style="color: #fbbf24; margin: 0 0 16px 0; font-size: 16px;">💡 Content Ideas Based on Today's Trends</h3>
            <ul style="color: #cbd5e1; margin: 0; padding-left: 20px; font-size: 14px; line-height: 2;">
                <li>Study the <strong style="color: #22d3ee;">titles and thumbnails</strong> of viral videos</li>
                <li>Notice the <strong style="color: #34d399;">video lengths</strong> that perform well</li>
                <li>Look for <strong style="color: #f472b6;">patterns in topics</strong> getting high engagement</li>
                <li>Check if there are <strong style="color: #a78bfa;">gaps in content</strong> you could fill</li>
            </ul>
        </div>
        
        <!-- Footer -->
        <div style="text-align: center; padding: 30px 20px; color: #64748b; font-size: 12px;">
            <div style="margin-bottom: 10px;">
                <span style="font-size: 24px;">🚀</span>
            </div>
            <p style="margin: 0 0 8px 0; color: #94a3b8; font-weight: 500;">YouTube Competitor Analyzer</p>
            <p style="margin: 0;">Built for @thesoloentrepreneur07 • Powered by ScrapingDog API</p>
        </div>
    </div>
</body>
</html>
"""
        return html
        
    def _generate_text_report(
        self, 
        all_videos: List[VideoData], 
        competitor_videos: Dict[str, List[VideoData]]
    ) -> str:
        """Generate plain text fallback report"""
        
        date_str = datetime.now().strftime("%B %d, %Y")
        
        text = f"""
🎯 AI NICHE VIDEO REPORT
{date_str}
{'='*60}

📊 SUMMARY
- Total Outperforming Videos: {len(all_videos)}
- From Tracked Competitors: {sum(len(v) for v in competitor_videos.values())}

{'='*60}
🔥 TOP PERFORMING VIDEOS
{'='*60}

"""
        
        for i, video in enumerate(all_videos[:10], 1):
            text += f"""
{i}. {video.title}
   Channel: {video.channel_name}
   Views: {video.view_count:,} | Published: {video.published_date}
   URL: {video.video_url}
"""
        
        if competitor_videos:
            text += f"\n{'='*60}\n📺 COMPETITOR BREAKDOWN\n{'='*60}\n"
            
            for channel, videos in competitor_videos.items():
                text += f"\n🎯 {channel} ({len(videos)} videos)\n"
                for video in videos[:3]:
                    text += f"   • {video.title[:50]}... ({video.view_count:,} views)\n"
        
        text += f"""
{'='*60}
💡 CONTENT IDEAS
Study the titles, thumbnails, and topics of these 
outperforming videos. Look for patterns!

Built for @thesoloentrepreneur07
"""
        return text
        
    def send_report(
        self, 
        all_videos: List[VideoData], 
        competitor_videos: Dict[str, List[VideoData]]
    ) -> bool:
        """Send the email report"""
        
        if not all_videos:
            logger.info("📭 No outperforming videos found. Skipping email.")
            return True
            
        # Validate email config
        if not self.sender_email or not self.sender_password or not self.recipient_email:
            logger.error("❌ Email configuration incomplete. Please set EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECIPIENT")
            return False
            
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎯 Daily AI Video Report - {len(all_videos)} Viral Videos Found | {datetime.now().strftime('%b %d')}"
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            
            # Generate reports
            text_content = self._generate_text_report(all_videos, competitor_videos)
            html_content = self._generate_html_report(all_videos, competitor_videos)
            
            # Attach both versions
            msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            logger.info(f"📧 Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                
            logger.info(f"✅ Email report sent successfully to {self.recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ SMTP Authentication failed: {e}")
            logger.error("💡 For Gmail: Use an App Password, not your regular password")
            logger.error("   Create one at: https://myaccount.google.com/apppasswords")
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False


def send_outperforming_videos_report(
    all_videos: List[VideoData], 
    competitor_videos: Dict[str, List[VideoData]]
) -> bool:
    """Main entry point to send the report"""
    sender = EmailSender()
    return sender.send_report(all_videos, competitor_videos)


if __name__ == "__main__":
    # Test HTML generation
    from youtube_analyzer import VideoData
    
    test_videos = [
        VideoData(
            video_id="test123",
            title="Amazing AI Tool That Will Change How You Work Forever in 2024!",
            channel_name="AI Advantage",
            channel_link="https://youtube.com/@aiadvantage",
            published_date="2 days ago",
            view_count=250000,
            video_url="https://www.youtube.com/watch?v=test123",
            thumbnail_url="https://i.ytimg.com/vi/test123/hqdefault.jpg",
            description="Test description",
            length="12:34",
            is_verified=True
        ),
        VideoData(
            video_id="test456",
            title="No-Code Automation: Build a Complete SaaS in 24 Hours",
            channel_name="Skills Factory",
            channel_link="https://youtube.com/@skillsfactory",
            published_date="1 day ago",
            view_count=150000,
            video_url="https://www.youtube.com/watch?v=test456",
            thumbnail_url="https://i.ytimg.com/vi/test456/hqdefault.jpg",
            description="Test description",
            length="45:21",
            is_verified=False
        )
    ]
    
    test_competitors = {
        "AI Advantage": [test_videos[0]]
    }
    
    print("📝 Generating test email...")
    sender = EmailSender()
    html = sender._generate_html_report(test_videos, test_competitors)
    
    # Save test HTML
    with open("test_email.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Test email saved to test_email.html")
    print("   Open it in a browser to preview!")
