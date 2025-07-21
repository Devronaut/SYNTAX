import re
from datetime import datetime
import sheets

SHEET_NAME = "SYNTAX_DATA"
WORKSHEET_NAME = "Habit"

# Parse habit name and quantity from message
# Example: "Water 2L" -> ("Water", "2L")
#          "Sleep 7 hours" -> ("Sleep", "7 hours")
def parse_habit_message(message: str):
    # Try to extract quantity (number + unit)
    match = re.match(r"([a-zA-Z ]+?)\s*(\d+\s*\w+)?$", message.strip())
    if match:
        habit = match.group(1).strip().capitalize()
        quantity = match.group(2).strip() if match.group(2) else ""
        return habit, quantity
    return message.strip().capitalize(), ""

# Log the habit update to Google Sheets
def log_habit_update(message: str):
    habit, quantity = parse_habit_message(message)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, habit, quantity]
    sheets.append_row(SHEET_NAME, row, WORKSHEET_NAME)
    return f"Habit '{habit}' logged{' with quantity ' + quantity if quantity else ''}." 