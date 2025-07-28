import re
from datetime import datetime, timedelta
import sheets

WORKSHEET_NAME = "Finance"

# Helper to parse period and category from summary requests
def parse_summary_request(message: str):
    msg = message.lower()
    # Default period is 'all', default category is None
    period = 'all'
    category = None
    if 'today' in msg:
        period = 'today'
    elif 'week' in msg:
        period = 'week'
    elif 'month' in msg:
        period = 'month'
    # Try to extract category (e.g., 'summary groceries')
    match = re.search(r'summary(?:\s+(today|week|month))?\s*(\w+)?', msg)
    if match:
        if match.group(2):
            category = match.group(2).title()
    return period, category

def parse_expense_message(message: str):
    """
    Parse expense messages like:
    - "Spent ₹500 on groceries"
    - "Paid ₹1200 for electricity"
    - "₹2000 for rent"
    Returns (amount, category, notes)
    """
    # Pattern to match: ₹amount followed by optional category/notes
    pattern = r'(?:spent |paid |₹)(\d+)(?:\s+(?:on|for)\s+(.+))?'
    match = re.search(pattern, message.lower())
    
    if match:
        amount = int(match.group(1))
        category_notes = match.group(2) if match.group(2) else "Uncategorized"
        # Split into category and notes if there's additional text
        parts = category_notes.split(' - ', 1)
        category = parts[0].strip().title()
        notes = parts[1].strip() if len(parts) > 1 else ""
        return amount, category, notes
    
    return None, None, None

def get_summary(message=None):
    """Get expense summary for the specified period"""
    rows = sheets.get_all_rows(worksheet=WORKSHEET_NAME)
    if not rows or len(rows) < 2:
        return "No expenses recorded yet."
    # Parse period and category from message
    period, category = parse_summary_request(message or "")
    now = datetime.now()
    filtered = []
    for row in rows:
        try:
            ts = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            amt = int(row[1])
            cat = row[2]
        except Exception:
            continue
        # Filter by period
        if period == 'today' and ts.date() != now.date():
            continue
        if period == 'week' and ts < now - timedelta(days=now.weekday()):
            continue
        if period == 'month' and (ts.year != now.year or ts.month != now.month):
            continue
        # Filter by category
        if category and cat.lower() != category.lower():
            continue
        filtered.append((ts, amt, cat))
    if not filtered:
        return "No expenses found for that period/category."
    total = sum(amt for _, amt, _ in filtered)
    if category:
        return f"Total {category} expenses for {period}: ₹{total}"
    return f"Total expenses for {period}: ₹{total}"

def log_expense(message: str):
    """Log an expense from the message"""
    amount, category, notes = parse_expense_message(message)
    
    if amount is None:
        return "Sorry, I couldn't understand the expense format. Please use format: 'Spent ₹X on Y'"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, str(amount), category, notes]
    
    sheets.append_row(row_values=row, worksheet=WORKSHEET_NAME)
    return f"Expense logged: ₹{amount} for {category}"

def handle_finance_message(message: str):
    """Route finance-related messages to appropriate handlers"""
    msg = message.lower()
    
    if any(word in msg for word in ["spent", "paid", "₹"]):
        return log_expense(message)
    elif "summary" in msg:
        return get_summary(message)
    else:
        return "Sorry, I didn't understand. You can:\n- Log expense: 'Spent ₹X on Y'\n- Get summary: 'Show expense summary', 'summary today', 'summary week groceries', etc." 