import os

from dotenv import load_dotenv
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Bot token from @BotFather
API_ID = int(os.getenv("API_ID"))  # Telegram API ID
API_HASH = os.getenv("API_HASH")  # Telegram API Hash

# Channels and Admins
CHANNELS = os.getenv("CHANNELS", "").split()  # Channel IDs (space-separated)
ADMINS = os.getenv("ADMINS", "").split()  # Admin user IDs (space-separated)

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")  # MongoDB URI
DATABASE_NAME = os.getenv("DATABASE_NAME", "umz_filter_bot")  # Database name

# Logging and Support
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))  # Channel ID for logs
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "")  # Username for support chat (without @)

# Optional Features
PICS = os.getenv("PICS", "").split()  # Telegraph links for images
USE_CAPTION_FILTER = bool(os.getenv("USE_CAPTION_FILTER", "False"))
SHORT_URL = os.getenv("SHORT_URL", "")  # URL Shortener
SHORT_API = os.getenv("SHORT_API", "")  # API Key for Shortener
