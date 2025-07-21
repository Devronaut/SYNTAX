# Syntax - Personal WhatsApp AI Agent

A personal AI agent that interacts via WhatsApp to help track daily habits, manage reminders, and monitor personal finances.

## Features

### Current Features
- **Daily Habit Tracking**: Log and track daily habits with quantities (e.g., "Water 2L", "Gym done").
- More features coming soon...

### Planned Features
- **Reminders**: Set and receive reminders via WhatsApp.
- **Personal Finance Management**: Track expenses and get spending summaries.

## Setup

1. Clone the repository
```bash
git clone <your-repo-url>
cd my_jarvis
```

2. Create and activate virtual environment
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up Google Cloud Project and enable Google Sheets API
- Create a project in Google Cloud Console
- Enable Google Sheets API
- Create a service account and download the JSON key
- Rename the key to `service_account.json` and place it in the project root
- Share your Google Sheet with the service account email

5. Start the server
```bash
uvicorn main:app --reload
```

## Environment Setup
- Python 3.10+
- FastAPI
- Google Sheets API
- More dependencies listed in `requirements.txt`

## Contributing
This is a personal project, but suggestions and improvements are welcome!

## License
MIT License 