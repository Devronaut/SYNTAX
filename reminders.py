import re
import dateparser
from datetime import datetime, timedelta
import sheets

WORKSHEET_NAME = "Reminders"

def parse_reminder_message(message: str):
    """
    Parse reminder messages like:
    - "Remind me to call mom at 8 PM"
    - "Remind me to pay bill tomorrow at 10am"
    - "Remind me to buy groceries in 2 hours"
    - "Remind me to test in 5 minutes"
    Returns (reminder_text, scheduled_time) or (None, None) if parsing fails
    """
    # Remove "remind me" and similar phrases
    clean_msg = re.sub(r'remind\s+me\s+(?:to\s+)?', '', message.lower())
    print(f"Debug: clean_msg = '{clean_msg}'")
    
    # Try to find time indicators with more precise patterns
    time_patterns = [
        (r'\s+at\s+', 'at'),
        (r'\s+on\s+', 'on'),
        (r'\s+tomorrow\s+', 'tomorrow'),
        (r'\s+today\s+', 'today'),
        (r'\s+next\s+', 'next'),
        (r'\s+in\s+', 'in'),
        (r'\s+by\s+', 'by')
    ]
    
    # Find the time part
    time_part = None
    reminder_text = clean_msg
    
    for pattern, indicator in time_patterns:
        match = re.search(pattern, clean_msg)
        if match:
            # Split on the matched pattern
            parts = re.split(pattern, clean_msg, 1)
            if len(parts) > 1:
                reminder_text = parts[0].strip()
                time_part = indicator + parts[1].strip()
                print(f"Debug: Found indicator '{indicator}', reminder_text = '{reminder_text}', time_part = '{time_part}'")
                break
    
    if not time_part:
        print(f"Debug: No time part found")
        return None, None
    
    # Parse the time using dateparser
    try:
        scheduled_time = dateparser.parse(time_part)
        print(f"Debug: dateparser.parse('{time_part}') = {scheduled_time}")
        if scheduled_time:
            return reminder_text.title(), scheduled_time
    except Exception as e:
        print(f"Debug: dateparser.parse failed with error: {e}")
    
    print(f"Debug: Final result: None, None")
    return None, None

def log_reminder(message: str):
    """Log a reminder to Google Sheets"""
    print(f"Debug: log_reminder called with message: '{message}'")
    reminder_text, scheduled_time = parse_reminder_message(message)
    
    if not reminder_text or not scheduled_time:
        return "Sorry, I couldn't understand the reminder format. Try: 'Remind me to call mom at 8 PM' or 'Remind me to test in 5 minutes'"
    
    # Format the scheduled time
    scheduled_str = scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the row: [Timestamp, Reminder Text, Scheduled Time, Status]
    row = [timestamp, reminder_text, scheduled_str, "Pending"]
    
    sheets.append_row(row_values=row, worksheet=WORKSHEET_NAME)
    
    return f"Reminder set: '{reminder_text}' for {scheduled_time.strftime('%Y-%m-%d %H:%M')}"

def get_pending_reminders():
    """Get all pending reminders"""
    rows = sheets.get_all_rows(worksheet=WORKSHEET_NAME)
    if not rows or len(rows) < 2:
        return "No reminders set."
    
    pending = []
    for row in rows[1:]:  # Skip header
        if len(row) >= 4 and row[3] == "Pending":
            scheduled_time = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            if scheduled_time > datetime.now():
                pending.append((row[1], scheduled_time))
    
    if not pending:
        return "No pending reminders."
    
    result = "Pending reminders:\n"
    for text, time in pending:
        result += f"- {text} (due: {time.strftime('%Y-%m-%d %H:%M')})\n"
    
    return result

def handle_reminder_message(message: str):
    """Route reminder-related messages to appropriate handlers"""
    msg = message.lower()
    
    if "remind" in msg:
        return log_reminder(message)
    elif "list reminders" in msg or "show reminders" in msg:
        return get_pending_reminders()
    else:
        return "Sorry, I didn't understand. You can:\n- Set reminder: 'Remind me to call mom at 8 PM'\n- List reminders: 'Show reminders'" 