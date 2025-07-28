# router.py

import habits
import finance
import reminders

def route_message(message: str) -> str:
    msg = message.lower()
    if any(word in msg for word in ["gym", "meditate", "read", "habit", "water", "sleep"]):
        return habits.log_habit_update(message)
    elif any(word in msg for word in ["remind", "reminder", "list reminders", "show reminders"]):
        return reminders.handle_reminder_message(message)
    elif any(word in msg for word in ["spent", "paid", "₹", "expense", "summary"]):
        return finance.handle_finance_message(message)
    else:
        return "Sorry, I didn't understand that. Try:\n- Habit: 'Gym done'\n- Finance: 'Spent ₹500 on groceries'\n- Reminder: 'Remind me to call mom at 8 PM'\n- Summary: 'Show expense summary'" 