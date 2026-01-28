#!/bin/bash
# Task Tracker Wrapper for Clawdbot Integration

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACKER_SCRIPT="$SCRIPT_DIR/track_completions.py"

case "$1" in
    "setup")
        echo "🚀 Setting up Task Tracker..."
        
        # Test the tracker script
        python3 "$TRACKER_SCRIPT" daily_summary > /dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Task tracker initialized"
        else
            echo "❌ Error initializing task tracker"
            exit 1
        fi
        
        # Create daily summary cron job
        echo "📅 Creating daily follow-up cron job..."
        
        clawdbot cron add \
            --name "Task Follow-up Check" \
            --cron "0 9 * * *" \
            --session isolated \
            --message "Check for pending tasks and send follow-ups. Run: python3 $TRACKER_SCRIPT daily_summary" \
            --deliver \
            --channel last \
            --post-prefix "📋 Tasks"
        
        echo "✅ Setup complete! Daily task check at 9 AM"
        ;;
        
    "pending")
        python3 "$TRACKER_SCRIPT" list_pending
        ;;
        
    "complete")
        if [ -z "$2" ]; then
            echo "Usage: wrapper.sh complete <task_id>"
            exit 1
        fi
        python3 "$TRACKER_SCRIPT" mark_completed "$2"
        ;;
        
    "check_message")
        if [ -z "$2" ]; then
            echo "Usage: wrapper.sh check_message <message_text> [job_ids...]"
            exit 1
        fi
        shift  # Remove "check_message" 
        python3 "$TRACKER_SCRIPT" check_message "$@"
        ;;
        
    "daily")
        python3 "$TRACKER_SCRIPT" daily_summary
        ;;
        
    *)
        echo "Task Tracker Commands:"
        echo "  setup     - Initialize tracker and create cron jobs"
        echo "  pending   - List pending tasks"
        echo "  complete  - Mark task as completed"
        echo "  daily     - Show daily summary"
        echo "  check_message - Check if message indicates completion"
        exit 1
        ;;
esac