# router.py

import habits

def route_message(message: str) -> str:
    msg = message.lower()
    if any(word in msg for word in ["gym", "meditate", "read", "habit", "water", "sleep"]):
        return habits.log_habit_update(message)
    elif any(word in msg for word in ["remind", "reminder"]):
        return "[Reminders Module] Reminder set!"
    elif any(word in msg for word in ["spent", "paid", "expense", "how much"]):
        return "[Finance Module] Expense logged or summary provided!"
    else:
        return "Sorry, I didn't understand that. Try 'help' for options." 