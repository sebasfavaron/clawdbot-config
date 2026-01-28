#!/bin/bash
# Create tracked reminder - combines cron job creation with tracking

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACKER_SCRIPT="$SCRIPT_DIR/track_completions.py"

if [ $# -lt 2 ]; then
    echo "Usage: create_tracked_reminder.sh <schedule> <task_description>"
    echo "Examples:"
    echo "  create_tracked_reminder.sh '2026-01-29T15:00:00' 'llamar dentista'"
    echo "  create_tracked_reminder.sh 'tomorrow 9am' 'revisar emails'"
    echo "  create_tracked_reminder.sh '0 9 * * 1' 'weekly team meeting'"
    exit 1
fi

SCHEDULE="$1"
TASK_DESC="$2"

# Create cron job name
JOB_NAME="Tracked: $TASK_DESC"

# Determine if it's a one-time or recurring job
if [[ "$SCHEDULE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2} ]] || [[ "$SCHEDULE" =~ ^(tomorrow|today) ]] || [[ "$SCHEDULE" =~ ^[0-9]+[mh]$ ]]; then
    # One-time job
    echo "🔔 Creating one-time tracked reminder..."
    
    JOB_OUTPUT=$(clawdbot cron add \
        --name "$JOB_NAME" \
        --at "$SCHEDULE" \
        --session isolated \
        --message "Recordatorio: $TASK_DESC. 

IMPORTANTE: Este recordatorio está siendo tracked. Responde 'listo', 'hecho', o 'completado' cuando termines la tarea para que no te siga recordando.

Tarea: $TASK_DESC" \
        --deliver \
        --channel last \
        --delete-after-run \
        --post-prefix "🔔")
    
else
    # Recurring job (assume cron format)
    echo "🔄 Creating recurring tracked reminder..."
    
    JOB_OUTPUT=$(clawdbot cron add \
        --name "$JOB_NAME" \
        --cron "$SCHEDULE" \
        --session isolated \
        --message "Recordatorio recurrente: $TASK_DESC.

Este es un recordatorio recurrente. Responde 'listo' cuando completes la tarea de hoy.

Tarea: $TASK_DESC" \
        --deliver \
        --channel last \
        --post-prefix "🔔")
fi

if [ $? -eq 0 ]; then
    echo "✅ Cron job created successfully"
    
    # Extract job ID from output (usually last line contains the ID)
    JOB_ID=$(echo "$JOB_OUTPUT" | grep -oE '[a-f0-9-]{36}' | tail -1)
    
    if [ -n "$JOB_ID" ]; then
        echo "📋 Job ID: $JOB_ID"
        
        # Mark as pending tracking (will be activated when job first runs)
        python3 "$TRACKER_SCRIPT" mark_pending "$JOB_ID" "$TASK_DESC" "$(date -Iseconds)"
        echo "✅ Tracking enabled for: $TASK_DESC"
    else
        echo "⚠️  Could not extract job ID, manual tracking setup required"
    fi
else
    echo "❌ Failed to create cron job"
    exit 1
fi

echo ""
echo "📱 Your tracked reminder is set!"
echo "💡 Respond 'listo', 'hecho', or 'completado' when you finish the task"