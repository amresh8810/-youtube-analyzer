# 🎯 YouTube Competitor Video Analyzer

**Daily automated reports of viral videos in the AI/Automation niche**

Built for @thesoloentrepreneur07

## ✅ Quick Start (Local Testing)

### 1. Run a dry test (no email):
```bash
cd "c:\Users\Amresh kumar\Downloads\main.py\youtube"
python main.py --dry-run
```

### 2. Configure email (to receive reports):

Edit the config.py or set environment variables:

**For Gmail:**
1. Go to https://myaccount.google.com/apppasswords
2. Create an App Password for "Mail"
3. Set these in config.py or as environment variables:
   ```
   EMAIL_SENDER=your_gmail@gmail.com
   EMAIL_PASSWORD=your_16_char_app_password
   EMAIL_RECIPIENT=where_to_receive@email.com
   ```

### 3. Send a test email:
```bash
python main.py --test-email
```

### 4. Run full analysis with email:
```bash
python main.py
```

---

## 📁 Files Created

| File | Description |
|------|-------------|
| `config.py` | Configuration (API keys, search queries, thresholds) |
| `youtube_analyzer.py` | Core analyzer using ScrapingDog API |
| `email_sender.py` | Beautiful HTML email reports |
| `main.py` | CLI entry point |
| `requirements.txt` | Python dependencies |
| `setup_cron.sh` | Cron setup for Hostinger |

---

## 🔧 Configuration

### Search Queries (edit in config.py)
```python
SEARCH_QUERIES = [
    "AI tools 2024",
    "ChatGPT tutorial",
    "no code automation",
    # Add more...
]
```

### Competitor Channels (edit in config.py)
```python
COMPETITOR_CHANNELS = [
    "Matt Wolfe",
    "All About AI",
    "AI Advantage",
    # Add more...
]
```

### Thresholds
- `MIN_VIEWS_THRESHOLD`: Minimum views (default: 50,000)
- `DAYS_TO_ANALYZE`: How recent videos must be (default: 14 days)

---

## 🌐 Hostinger KVM 2 Deployment

### 1. Upload files to server
```bash
scp -r youtube/ user@your_server:/home/user/youtube-analyzer/
```

### 2. Setup on server
```bash
ssh user@your_server
cd youtube-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test
python main.py --dry-run
```

### 3. Setup cron for 2 PM daily
```bash
crontab -e
# Add this line (adjust paths):
0 14 * * * cd /home/user/youtube-analyzer && /home/user/youtube-analyzer/venv/bin/python main.py >> /home/user/youtube-analyzer/logs/cron.log 2>&1
```

---

## 🚀 Hosting on GitHub (Free Workflow)

You can host this for **FREE** using GitHub Actions. It will run automatically every day.

### 1. Create a Private GitHub Repository
- Create a new repository on GitHub (keep it **Private** to protect your code).
- Push all these files to your repository.

### 2. Configure GitHub Secrets
GitHub Actions uses "Secrets" to store your API keys and Passwords securely.
1. Go to your repository on GitHub.
2. Click **Settings** > **Secrets and variables** > **Actions**.
3. Create the following **New repository secrets**:

| Secret Name | Description |
|-------------|-------------|
| `SCRAPINGDOG_API_KEY` | Your ScrapingDog API Key |
| `EMAIL_SENDER` | Your Gmail address (e.g., `you@gmail.com`) |
| `EMAIL_PASSWORD` | Your 16-character **Gmail App Password** |
| `EMAIL_RECIPIENT` | The email address where you want to receive reports |

### 3. Check the Workflow
- The automation is defined in `.github/workflows/daily_report.yml`.
- It is scheduled to run daily at 8:00 AM UTC.
- You can manually test it: Go to **Actions** tab > Click **Daily YouTube Report** > **Run workflow**.

---

## 🔑 API Keys

### ScrapingDog (Already configured!)
- Your API key is already set in config.py
- Each search uses 5 credits
- Monitor usage at https://www.scrapingdog.com/dashboard

### Gmail App Password
1. Enable 2FA on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate password for "Mail"

---

## 📊 Sample Output

```
🎉 Found 7 outperforming videos!

📊 TOP 5 VIDEOS TODAY:
1. The Only 25 Ways to Make Money in 2026...
   👤 Dan Martell
   👁️ 433,576 views | 📅 2 weeks ago

2. The Only AI Tools You Need (12-Minute Guide)...
   👤 Jeff Su
   👁️ 205,491 views | 📅 2 weeks ago
   
...
```

---

## 🆘 Troubleshooting

### "No outperforming videos found"
- Lower `MIN_VIEWS_THRESHOLD` in config.py
- Increase `DAYS_TO_ANALYZE` 
- Check ScrapingDog API credits

### Email not sending
- Verify Gmail App Password (not regular password!)
- Check EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT are set
- Look at logs/youtube_analyzer.log for errors

### API errors
- Check ScrapingDog credits at dashboard
- Verify API key is correct

---

Built with ❤️ using ScrapingDog YouTube API
