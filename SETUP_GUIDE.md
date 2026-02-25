# 🚀 YouTube Competitor Video Analyzer - Setup Guide

A powerful automation that monitors your competitors' YouTube channels and sends you daily email reports about their outperforming videos.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting YouTube API Key](#getting-youtube-api-key)
3. [Email Configuration](#email-configuration)
4. [Local Setup & Testing](#local-setup--testing)
5. [GitHub Actions Deployment (Free)](#github-actions-deployment-free)
6. [Hostinger KVM 2 Deployment](#hostinger-kvm-2-deployment)
7. [Customizing Competitors](#customizing-competitors)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

- Python 3.8 or higher
- ScrapingDog API Key (Free trial available)
- An email account (Gmail recommended)
- GitHub account (for free hosting) or Hostinger KVM

---

## 🔑 Getting ScrapingDog API Key

1. **Sign up at ScrapingDog**
   - Visit: https://www.scrapingdog.com/
   - Create a free account.

2. **Get your API Key**
   - Go to your Dashboard: https://api.scrapingdog.com/dashboard
   - Copy your **API Key**.

3. **Use in .env file**
   ```
   SCRAPINGDOG_API_KEY=your_api_key_here
   ```

> ⚠️ **Credits**: Each YouTube search consumes credits. Monitor your usage in the ScrapingDog dashboard.

---

## 📧 Email Configuration

### Option 1: Gmail (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Create App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Click "Generate"
   - Copy the 16-character password

3. **Use in .env file**
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_16_char_app_password
   ```

### Option 2: Hostinger Email

1. **Create email in Hostinger**
   - Go to hPanel → Emails → Create email account

2. **Use Hostinger SMTP**
   ```
   SMTP_SERVER=smtp.hostinger.com
   SMTP_PORT=587
   EMAIL_SENDER=your_email@yourdomain.com
   EMAIL_PASSWORD=your_email_password
   ```

---

## 💻 Local Setup & Testing

### Step 1: Clone/Download Files

Make sure all these files are in your project folder:
```
youtube-analyzer/
├── config.py
├── youtube_analyzer.py
├── email_sender.py
├── main.py
├── requirements.txt
├── .env.example
├── setup_cron.sh
└── SETUP_GUIDE.md
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
# On Windows: notepad .env
# On Linux: nano .env
```

### Step 5: Update config.py with Competitors

Edit `config.py` and update the `COMPETITOR_CHANNELS` list:

```python
COMPETITOR_CHANNELS = [
    "fireship",
    "aiadvantage",
    "mattvidpro",
    "allaboutai",
    "theaiguy",
    # Add your competitors here
]
```

### Step 6: Test the Automation

```bash
# Dry run (no email sent)
python main.py --dry-run

# Full run with email
python main.py
```

---

---

## 🚀 GitHub Actions Deployment (FREE)

This is the easiest way to host your bot for free. It will run automatically every day using GitHub's servers.

### Step 1: Push Code to GitHub
1. Create a **Private** repository on GitHub.
2. Push all your project files to the repository.

### Step 2: Set Up GitHub Secrets
1. In your GitHub repo, go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** for each of these:
   - `SCRAPINGDOG_API_KEY`: Your ScrapingDog API key.
   - `EMAIL_SENDER`: Your Gmail address.
   - `EMAIL_PASSWORD`: Your 16-character **Gmail App Password**.
   - `EMAIL_RECIPIENT`: Where you want to receive the email.

### Step 3: Enable the Workflow
1. Go to the **Actions** tab in your repository.
2. If it asks, click **"I understand my workflows, go ahead and enable them"**.
3. You should see a workflow named "Daily YouTube Report".
4. You can click **Run workflow** to test it immediately!

---

## 🌐 Hostinger KVM 2 Deployment

### Step 1: Connect via SSH

```bash
ssh root@your_server_ip
# Or use your Hostinger SSH credentials
```

### Step 2: Install Python (if not installed)

```bash
# Check Python version
python3 --version

# Install if needed (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 3: Upload Project Files

**Option A: Using SCP**
```bash
# From your local machine
scp -r /path/to/youtube-analyzer/ root@your_server_ip:/home/username/
```

**Option B: Using Git**
```bash
# On server
git clone your-repo-url /home/username/youtube-analyzer
```

**Option C: Using SFTP**
- Use FileZilla or similar
- Connect to your server
- Upload the project folder

### Step 4: Setup on Server

```bash
# Navigate to project
cd /home/username/youtube-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
nano .env  # Edit with your credentials
```

### Step 5: Test on Server

```bash
# Activate virtual environment
source venv/bin/activate

# Test run
python main.py --dry-run
```

### Step 6: Set Up Cron Job

```bash
# Make script executable
chmod +x setup_cron.sh

# Edit the script to update PROJECT_DIR
nano setup_cron.sh

# Run setup
./setup_cron.sh

# Or manually add cron entry
crontab -e
# Add this line (runs at 2 PM daily):
0 14 * * * cd /home/username/youtube-analyzer && /home/username/youtube-analyzer/venv/bin/python main.py >> /home/username/youtube-analyzer/logs/cron.log 2>&1
```

### Step 7: Verify Cron is Working

```bash
# List cron jobs
crontab -l

# Check cron service status
sudo systemctl status cron

# View logs after it runs
tail -f /home/username/youtube-analyzer/logs/cron.log
```

---

## 📺 Customizing Competitors

### Finding Competitor Channel Handles

1. Go to the competitor's YouTube channel
2. Look at the URL: `youtube.com/@channelhandle`
3. The handle is after the `@` symbol

### Recommended AI/Automation Niche Competitors

```python
COMPETITOR_CHANNELS = [
    # AI News & Reviews
    "mattvidpro",
    "aiadvantage", 
    "allaboutai",
    "theaiguy",
    
    # Tech & Coding
    "fireship",
    "techwithtim",
    "traversymedia",
    
    # No-Code & Automation
    "howtowithgoddy",
    "buildwithnishant",
    
    # Startup Ideas
    "myFirstMillion",
    "thefutur",
    
    # Add more as needed
]
```

### Adjusting Outperformance Threshold

In `config.py`:

```python
# Lower = more videos (1.5x means 50% above average)
OUTPERFORMANCE_MULTIPLIER = 1.5

# Higher = fewer but more viral videos (3x means 200% above average)
OUTPERFORMANCE_MULTIPLIER = 3.0
```

---

## 🔧 Troubleshooting

### API Errors

**"quotaExceeded"**
- You've exceeded the daily API quota
- Wait until midnight Pacific Time for reset
- Or request quota increase in Google Cloud Console

**"forbidden" or "accessNotConfigured"**
- Enable YouTube Data API v3 in Google Cloud Console
- Check API key restrictions

### Email Not Sending

**Gmail "Bad Credentials"**
- Make sure you're using an App Password, not your regular password
- Enable 2-Factor Authentication first

**Connection Timeout**
- Check SMTP server and port settings
- Verify firewall isn't blocking port 587

### Cron Not Running

**Check timezone**
```bash
# Check server timezone
timedatectl

# Set timezone if needed
sudo timedatectl set-timezone Your/Timezone
```

**Check cron service**
```bash
sudo systemctl status cron
sudo systemctl restart cron
```

**Check logs**
```bash
# System cron logs
sudo grep CRON /var/log/syslog

# Application logs
cat /home/username/youtube-analyzer/logs/cron.log
```

---

## 📞 Support

For issues or feature requests, please create an issue in the repository or contact the developer.

---

Made with ❤️ for @thesoloentrepreneur07
