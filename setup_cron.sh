#!/bin/bash
# ========================================
# Cron Job Setup Script for Hostinger KVM 2
# Runs YouTube Analyzer at 2 PM daily
# ========================================

# Configuration - UPDATE THESE PATHS
PROJECT_DIR="/home/your_username/youtube-analyzer"  # Your project path
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"          # Virtual env Python
LOG_DIR="$PROJECT_DIR/logs"

# Create logs directory
mkdir -p "$LOG_DIR"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🕐 Setting up Daily 2 PM Cron Job                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Create the cron entry (2 PM = 14:00)
CRON_CMD="cd $PROJECT_DIR && $VENV_PYTHON main.py >> $LOG_DIR/cron_\$(date +\%Y\%m\%d).log 2>&1"
CRON_ENTRY="0 14 * * * $CRON_CMD"

echo "📋 Cron entry to add:"
echo ""
echo "   $CRON_ENTRY"
echo ""

# Check if cron entry already exists
if crontab -l 2>/dev/null | grep -q "youtube-analyzer\|main.py"; then
    echo "⚠️  An existing cron entry was found."
    echo "   Current crontab:"
    crontab -l | grep -E "youtube|main.py"
    echo ""
    read -p "Do you want to replace it? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "❌ Cancelled."
        exit 0
    fi
    # Remove old entry
    crontab -l | grep -v "youtube-analyzer\|main.py" | crontab -
fi

# Add new cron entry
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo ""
echo "✅ Cron job added successfully!"
echo ""
echo "📝 To verify: crontab -l"
echo "📊 Logs saved to: $LOG_DIR/"
echo ""
echo "⏰ The automation will run every day at 2:00 PM server time"
echo ""

# Show current timezone
echo "🌍 Current server timezone:"
timedatectl 2>/dev/null || date +%Z
echo ""

# Verify
echo "📋 Current crontab entries:"
crontab -l
