from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import sheets

class ReminderScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
        # Schedule the reminder check to run every minute
        self.scheduler.add_job(
            func=self.check_due_reminders,
            trigger=IntervalTrigger(minutes=1),
            id='reminder_check',
            name='Check for due reminders',
            replace_existing=True
        )
    
    def check_due_reminders(self):
        """Check for reminders that are due and send notifications"""
        try:
            print(f"🔍 Checking for due reminders at {datetime.now()}")
            rows = sheets.get_all_rows(worksheet="Reminders")
            print(f"Debug: Found {len(rows)} rows in sheet")
            
            if not rows or len(rows) < 2:
                print("No reminders found in sheet")
                return
            
            now = datetime.now()
            due_reminders = []
            
            for i, row in enumerate(rows[1:], start=2):  # Skip header, start from row 2
                print(f"Debug: Row {i}: {row}")
                # Status is in column G (index 6) due to spacing
                if len(row) >= 7 and row[6] == "Pending":
                    try:
                        scheduled_time = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")  # Scheduled time is in column E (index 4)
                        print(f"Checking reminder '{row[2]}' scheduled for {scheduled_time}")  # Reminder text is in column C (index 2)
                        if scheduled_time <= now:
                            due_reminders.append((row[2], scheduled_time))
                            print(f"Found due reminder: {row[2]}")
                    except ValueError as e:
                        print(f"Error parsing time for row {i}: {e}")
                        continue
                else:
                    print(f"Debug: Row {i} not pending or too short: len={len(row)}, status={row[6] if len(row) > 6 else 'N/A'}")
            
            # Process due reminders
            for reminder_text, scheduled_time in due_reminders:
                self.send_reminder_notification(reminder_text, scheduled_time)
                self.mark_reminder_completed(reminder_text, scheduled_time)
                
        except Exception as e:
            print(f"Error checking reminders: {e}")
    
    def send_reminder_notification(self, reminder_text, scheduled_time):
        """Send a reminder notification (for now, just print to console)"""
        print(f"🔔 REMINDER: {reminder_text}")
        print(f"   Scheduled for: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # TODO: In the future, this will send a WhatsApp message
        # For now, we just print to console
    
    def mark_reminder_completed(self, reminder_text, scheduled_time):
        """Mark a reminder as completed in the sheet"""
        try:
            rows = sheets.get_all_rows(worksheet="Reminders")
            for i, row in enumerate(rows[1:], start=2):  # Start from row 2
                if len(row) >= 7:
                    try:
                        row_scheduled_time = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
                        if (row[2] == reminder_text and 
                            row_scheduled_time == scheduled_time and 
                            row[6] == "Pending"):
                            # Update the status to "Completed"
                            ws = sheets.open_sheet("Reminders")
                            cell_address = f"G{i}"  # Status column
                            ws.update(cell_address, [["Completed"]])
                            print(f"Marked reminder '{reminder_text}' as completed")
                            break
                    except ValueError:
                        continue
        except Exception as e:
            print(f"Error marking reminder completed: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()

# Global scheduler instance
reminder_scheduler = ReminderScheduler() 