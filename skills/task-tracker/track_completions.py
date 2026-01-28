#!/usr/bin/env python3
"""
Task Completion Tracker for Clawdbot

Tracks cron job completions and creates follow-up reminders for pending tasks.
"""

import json
import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
COMPLETIONS_FILE = Path.home() / ".clawdbot" / "task-completions.json"
COMPLETION_PATTERNS = [
    r'\b(listo|hecho|completado|terminé|cumplido|finished|done)\b',
    r'\bya\s+(lo\s+)?(hice|terminé|completé)\b',
    r'\b(task|tarea)\s+completed?\b',
    r'\b(reminder|recordatorio)\s+(done|listo)\b'
]

class TaskTracker:
    def __init__(self):
        self.completions_file = COMPLETIONS_FILE
        self.completions_file.parent.mkdir(exist_ok=True)
        self.load_completions()
    
    def load_completions(self):
        """Load completion tracking data"""
        try:
            if self.completions_file.exists():
                with open(self.completions_file) as f:
                    self.completions = json.load(f)
            else:
                self.completions = {
                    "pending": {},      # jobId -> task info
                    "completed": {},    # jobId -> completion info
                    "overdue": {}       # jobId -> overdue count
                }
        except Exception as e:
            print(f"Error loading completions: {e}")
            self.completions = {"pending": {}, "completed": {}, "overdue": {}}
    
    def save_completions(self):
        """Save completion tracking data"""
        try:
            with open(self.completions_file, 'w') as f:
                json.dump(self.completions, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving completions: {e}")
    
    def mark_pending(self, job_id, task_name, scheduled_time):
        """Mark a task as pending completion"""
        self.completions["pending"][job_id] = {
            "task_name": task_name,
            "scheduled_time": scheduled_time,
            "created_at": datetime.now().isoformat(),
            "follow_up_count": 0
        }
        self.save_completions()
        return f"📋 Tracking task: {task_name}"
    
    def mark_completed(self, job_id, completion_method="manual"):
        """Mark a task as completed"""
        if job_id in self.completions["pending"]:
            task_info = self.completions["pending"].pop(job_id)
            self.completions["completed"][job_id] = {
                **task_info,
                "completed_at": datetime.now().isoformat(),
                "completion_method": completion_method
            }
            
            # Remove from overdue if present
            self.completions["overdue"].pop(job_id, None)
            
            self.save_completions()
            return f"✅ Completed: {task_info['task_name']}"
        else:
            return "❌ Task not found in pending list"
    
    def detect_completion(self, message_text, recent_job_ids=None):
        """Detect if a message indicates task completion"""
        message_lower = message_text.lower()
        
        # Check completion patterns
        for pattern in COMPLETION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                # If we have recent job IDs, mark them as completed
                if recent_job_ids:
                    results = []
                    for job_id in recent_job_ids:
                        result = self.mark_completed(job_id, "auto_detected")
                        results.append(result)
                    return results
                return ["🔍 Completion detected but no recent tasks to mark"]
        
        return None
    
    def get_pending_tasks(self):
        """Get all pending tasks"""
        return self.completions["pending"]
    
    def get_overdue_tasks(self, hours_threshold=24):
        """Get tasks that are overdue"""
        overdue = {}
        now = datetime.now()
        
        for job_id, task_info in self.completions["pending"].items():
            scheduled_time = datetime.fromisoformat(task_info["scheduled_time"])
            if (now - scheduled_time).total_seconds() > hours_threshold * 3600:
                overdue[job_id] = task_info
                
        return overdue
    
    def create_follow_up_message(self, job_id, task_info):
        """Create a follow-up reminder message"""
        follow_up_count = task_info.get("follow_up_count", 0)
        task_name = task_info["task_name"]
        
        if follow_up_count == 0:
            prefix = "🔔 Recordatorio"
        elif follow_up_count == 1:
            prefix = "🔄 Pendiente"
        elif follow_up_count == 2:
            prefix = "⚠️ Aún pendiente"
        else:
            prefix = "❗ PENDIENTE"
        
        # Update follow-up count
        self.completions["pending"][job_id]["follow_up_count"] = follow_up_count + 1
        self.save_completions()
        
        return f"{prefix}: {task_name}"
    
    def generate_daily_summary(self):
        """Generate daily summary of pending tasks"""
        pending = self.get_pending_tasks()
        overdue = self.get_overdue_tasks()
        
        if not pending and not overdue:
            return "✅ No tienes tareas pendientes"
        
        summary = []
        
        if overdue:
            summary.append("❗ **Tareas Vencidas:**")
            for job_id, task_info in overdue.items():
                follow_up_msg = self.create_follow_up_message(job_id, task_info)
                summary.append(f"  • {follow_up_msg}")
        
        if pending:
            recent_pending = {k: v for k, v in pending.items() if k not in overdue}
            if recent_pending:
                summary.append("\n📋 **Tareas Pendientes:**")
                for job_id, task_info in recent_pending.items():
                    task_name = task_info["task_name"]
                    summary.append(f"  • {task_name}")
        
        summary.append(f"\nResponde 'listo [tarea]' para marcar como completada")
        
        return "\n".join(summary)


def main():
    """Main function for command-line usage"""
    tracker = TaskTracker()
    
    if len(sys.argv) < 2:
        print("Usage: track_completions.py [command] [args...]")
        print("Commands:")
        print("  mark_pending <job_id> <task_name> <scheduled_time>")
        print("  mark_completed <job_id>")
        print("  check_message <message_text> [recent_job_ids...]")
        print("  daily_summary")
        print("  list_pending")
        return
    
    command = sys.argv[1]
    
    if command == "mark_pending":
        if len(sys.argv) >= 5:
            job_id, task_name, scheduled_time = sys.argv[2], sys.argv[3], sys.argv[4]
            result = tracker.mark_pending(job_id, task_name, scheduled_time)
            print(result)
        else:
            print("Usage: mark_pending <job_id> <task_name> <scheduled_time>")
    
    elif command == "mark_completed":
        if len(sys.argv) >= 3:
            job_id = sys.argv[2]
            result = tracker.mark_completed(job_id)
            print(result)
        else:
            print("Usage: mark_completed <job_id>")
    
    elif command == "check_message":
        if len(sys.argv) >= 3:
            message_text = sys.argv[2]
            recent_jobs = sys.argv[3:] if len(sys.argv) > 3 else None
            results = tracker.detect_completion(message_text, recent_jobs)
            if results:
                for result in results:
                    print(result)
            else:
                print("No completion detected")
        else:
            print("Usage: check_message <message_text> [recent_job_ids...]")
    
    elif command == "daily_summary":
        summary = tracker.generate_daily_summary()
        print(summary)
    
    elif command == "list_pending":
        pending = tracker.get_pending_tasks()
        if pending:
            print("📋 Pending Tasks:")
            for job_id, task_info in pending.items():
                print(f"  {job_id}: {task_info['task_name']}")
        else:
            print("✅ No pending tasks")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()