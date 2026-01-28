# Task Tracker Skill

Track completion status of cron jobs and automatically follow up on pending tasks.

## What it does

- **Tracks cron job completions**: Monitors whether user confirmed completing tasks
- **Automatic follow-ups**: Reminds about pending tasks until explicitly marked as done
- **Smart detection**: Recognizes completion phrases like "done", "completed", "finished", etc.
- **Persistent tracking**: Maintains completion state across restarts

## Commands

### Creating Tracked Reminders
```bash
# Create a tracked reminder (auto-adds tracking)
/remind "llamar dentista mañana 3pm"
/remind "revisar email cada lunes 9am"
```

### Managing Completions
```bash
# Mark task as completed manually
/complete <task_id>

# List pending tasks
/pending

# Show completion history  
/completions [days]
```

### Completion Detection
The system automatically detects completion when you say:
- "listo", "hecho", "completado", "done", "finished"
- "ya lo hice", "terminé", "cumplido"
- References to the original task + completion phrase

## How it works

1. **Task Creation**: When you create a cron job reminder, it's automatically tracked
2. **Execution**: When the cron job fires, it's marked as "pending completion"
3. **Detection**: System monitors your messages for completion signals
4. **Follow-up**: If not marked complete, automatic reminders are sent
5. **Escalation**: Frequency increases for overdue tasks

## Files Created

- `task-completions.json` - Tracks completion status
- `completion-patterns.json` - Phrase patterns for detection
- Auto-created cron job for daily pending task review

## Integration

This skill automatically integrates with Clawdbot's cron system. When you create reminders through normal channels, they become trackable automatically.