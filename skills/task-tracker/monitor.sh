#!/bin/bash
# Auto-Detection Monitor for Task Tracker
# Monitors recent messages and detects task completions automatically

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_DETECT_SCRIPT="$SCRIPT_DIR/auto_detect.py"
LOG_FILE="/tmp/task-tracker-monitor.log"

# Function to log with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Function to check recent session messages for completion phrases
check_recent_messages() {
    # Target the main user session specifically
    CURRENT_SESSION="agent:main:main"
    
    # Verify the session exists
    SESSION_EXISTS=$(clawdbot sessions list --json 2>/dev/null | jq -r --arg session "$CURRENT_SESSION" '.sessions[] | select(.key == $session) | .key' 2>/dev/null)
    
    if [ -z "$SESSION_EXISTS" ]; then
        log_message "Main session not found or not active"
        return
    fi
    
    # Get recent messages from the current session (last 10 messages)
    RECENT_MESSAGES=$(clawdbot sessions history "$CURRENT_SESSION" --limit 10 --json 2>/dev/null | jq -r '.messages[]?.content // empty' 2>/dev/null)
    
    if [ -z "$RECENT_MESSAGES" ]; then
        log_message "No recent messages found"
        return
    fi
    
    # Check each message for completion patterns
    echo "$RECENT_MESSAGES" | while read -r message; do
        if [ -n "$message" ]; then
            # Check if message contains completion phrases
            result=$(python3 "$AUTO_DETECT_SCRIPT" check_message "$message" 2>/dev/null)
            if [ $? -eq 0 ] && [ -n "$result" ] && [ "$result" != "No completion detected" ]; then
                log_message "✅ Auto-completion detected: $result"
                echo "Auto-completion: $message -> $result"
            fi
        fi
    done
}

# Function to simulate message checking (for testing)
test_message_check() {
    local test_message="$1"
    
    log_message "🧪 Testing message: '$test_message'"
    
    result=$(python3 "$AUTO_DETECT_SCRIPT" check_message "$test_message" 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$result" ] && [ "$result" != "No completion detected" ]; then
        log_message "✅ Test completion detected: $result"
        echo "✅ $result"
    else
        log_message "❌ No completion detected in test message"
        echo "❌ No completion detected"
    fi
}

# Main execution
case "$1" in
    "check")
        log_message "Starting completion check"
        check_recent_messages
        ;;
    "test")
        if [ -n "$2" ]; then
            test_message_check "$2"
        else
            echo "Usage: monitor.sh test 'message text'"
        fi
        ;;
    "status")
        echo "Task Tracker Monitor Status:"
        echo "  Log file: $LOG_FILE"
        if [ -f "$LOG_FILE" ]; then
            echo "  Last 5 entries:"
            tail -5 "$LOG_FILE" | sed 's/^/    /'
        else
            echo "  No log file found"
        fi
        ;;
    *)
        echo "Task Tracker Auto-Detection Monitor"
        echo "Usage: $0 [command]"
        echo "Commands:"
        echo "  check  - Check recent messages for completions"
        echo "  test   - Test with a specific message"
        echo "  status - Show monitor status and recent logs"
        exit 1
        ;;
esac