import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

# Optional: API keys for research services
# Example: GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")