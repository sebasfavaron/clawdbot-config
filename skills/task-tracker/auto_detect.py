#!/usr/bin/env python3
"""
Auto-Detection System for Task Tracker

Monitors recent messages and automatically marks tasks as completed
when completion phrases are detected.
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from track_completions import TaskTracker

# Configuration
STATE_FILE = Path.home() / ".clawdbot" / "task-tracker-state.json"
RECENT_JOBS_FILE = Path.home() / ".clawdbot" / "recent-task-jobs.json"

class AutoDetector:
    def __init__(self):
        self.tracker = TaskTracker()
        self.state_file = STATE_FILE
        self.recent_jobs_file = RECENT_JOBS_FILE
        self.load_state()
        
    def load_state(self):
        """Load last processed message timestamp"""
        try:
            if self.state_file.exists():
                with open(self.state_file) as f:
                    self.state = json.load(f)
            else:
                self.state = {"last_check": 0}
        except:
            self.state = {"last_check": 0}
    
    def save_state(self):
        """Save current state"""
        try:
            self.state_file.parent.mkdir(exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f)
        except Exception as e:
            print(f"Error saving state: {e}")
    
    def get_recent_job_ids(self, hours=2):
        """Get job IDs that executed recently"""
        try:
            if self.recent_jobs_file.exists():
                with open(self.recent_jobs_file) as f:
                    recent_jobs = json.load(f)
                
                # Filter jobs from last N hours
                cutoff_time = datetime.now() - timedelta(hours=hours)
                cutoff_timestamp = cutoff_time.timestamp()
                
                active_jobs = []
                for job_id, timestamp in recent_jobs.items():
                    if timestamp > cutoff_timestamp:
                        active_jobs.append(job_id)
                
                return active_jobs
            return []
        except:
            return []
    
    def add_recent_job(self, job_id):
        """Add a job ID to recent executions"""
        try:
            recent_jobs = {}
            if self.recent_jobs_file.exists():
                with open(self.recent_jobs_file) as f:
                    recent_jobs = json.load(f)
            
            recent_jobs[job_id] = datetime.now().timestamp()
            
            # Clean old entries (>24 hours)
            cutoff = (datetime.now() - timedelta(hours=24)).timestamp()
            recent_jobs = {k: v for k, v in recent_jobs.items() if v > cutoff}
            
            self.recent_jobs_file.parent.mkdir(exist_ok=True)
            with open(self.recent_jobs_file, 'w') as f:
                json.dump(recent_jobs, f)
                
        except Exception as e:
            print(f"Error adding recent job: {e}")
    
    def check_for_completions(self, message_text, max_age_hours=2):
        """Check if message indicates task completion"""
        import re
        
        # First check if message contains completion phrases
        COMPLETION_PATTERNS = [
            r'\b(listo|hecho|completado|terminé|cumplido|finished|done)\b',
            r'\bya\s+(lo\s+)?(hice|terminé|completé)\b',
            r'\b(task|tarea)\s+completed?\b',
            r'\b(reminder|recordatorio)\s+(done|listo)\b'
        ]
        
        message_lower = message_text.lower()
        completion_detected = False
        
        for pattern in COMPLETION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                completion_detected = True
                break
        
        if not completion_detected:
            return None
        
        # Get recently executed job IDs
        recent_job_ids = self.get_recent_job_ids(max_age_hours)
        
        # Also check for any pending tasks
        pending_tasks = self.tracker.get_pending_tasks()
        
        results = []
        
        if recent_job_ids:
            # Mark recent job IDs as completed
            for job_id in recent_job_ids:
                if job_id in pending_tasks:
                    result = self.tracker.mark_completed(job_id, "auto_detected")
                    results.append(result)
        
        elif pending_tasks:
            # If no recent job IDs but we have pending tasks, mark the most recent one
            # This handles cases where the job executed but wasn't tracked properly
            most_recent_job = max(pending_tasks.keys(), 
                                key=lambda x: pending_tasks[x].get('created_at', '1970-01-01'))
            result = self.tracker.mark_completed(most_recent_job, "auto_detected_fallback")
            results.append(result)
        
        if results:
            print(f"✅ Auto-detected completion: {results}")
            return results
        
        return None
    
    def process_message(self, message_text, job_id=None):
        """Process a single message for completion detection"""
        # If this is a cron job executing, mark it as recent
        if job_id:
            self.add_recent_job(job_id)
            return f"📋 Added job {job_id} to recent tracking"
        
        # Otherwise, check for completion phrases
        results = self.check_for_completions(message_text)
        if results:
            return "\\n".join(results)
        
        return None


def main():
    """Main function for command-line usage"""
    detector = AutoDetector()
    
    if len(sys.argv) < 2:
        print("Usage: auto_detect.py [command] [args...]")
        print("Commands:")
        print("  check_message <message_text>     - Check message for completions")
        print("  add_job <job_id>                 - Mark job as recently executed")  
        print("  recent_jobs                      - List recent job IDs")
        print("  test_patterns                    - Test completion detection patterns")
        return
    
    command = sys.argv[1]
    
    if command == "check_message":
        if len(sys.argv) >= 3:
            message_text = sys.argv[2]
            result = detector.process_message(message_text)
            if result:
                print(result)
            else:
                print("No completion detected")
        else:
            print("Usage: auto_detect.py check_message <message_text>")
    
    elif command == "add_job":
        if len(sys.argv) >= 3:
            job_id = sys.argv[2]
            result = detector.process_message("", job_id=job_id)
            print(result)
        else:
            print("Usage: auto_detect.py add_job <job_id>")
    
    elif command == "recent_jobs":
        recent = detector.get_recent_job_ids(24)  # Last 24 hours
        if recent:
            print("Recent job IDs:")
            for job_id in recent:
                print(f"  {job_id}")
        else:
            print("No recent jobs")
    
    elif command == "test_patterns":
        # Create a dummy pending task for testing
        print("🧪 Testing completion patterns...")
        
        test_messages = [
            "listo",
            "ya está hecho", 
            "completado",
            "terminé la tarea",
            "task completed",
            "no tiene nada que ver",
            "Hola como estas",
            "done with the task",
            "hecho!",
            "LISTO"
        ]
        
        for msg in test_messages:
            # Test pattern matching only
            import re
            COMPLETION_PATTERNS = [
                r'\b(listo|hecho|completado|terminé|cumplido|finished|done)\b',
                r'\bya\s+(lo\s+)?(hice|terminé|completé)\b',
                r'\b(task|tarea)\s+completed?\b',
                r'\b(reminder|recordatorio)\s+(done|listo)\b'
            ]
            
            message_lower = msg.lower()
            completion_detected = False
            
            for pattern in COMPLETION_PATTERNS:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    completion_detected = True
                    break
            
            status = "✅ MATCH" if completion_detected else "❌ NO MATCH"
            print(f"{status}: '{msg}'")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()