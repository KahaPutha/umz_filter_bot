import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level (INFO for normal logging)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("logs", "config.log"))  # Log config-related info
    ]
)

# Helper function to handle boolean environment variables safely
def get_bool_env(var_name, default=False):
    """Helper function to safely get boolean environment variables."""
    value = os.getenv(var_name, str(default))
    return value.lower() in ("true", "1", "t", "y", "yes")

# Check if required environment variables are available
required_vars = ["BOT_TOKEN", "API_ID", "API_HASH", "DATABASE_URL"]
for var in required_vars:
    if os.getenv(var) is None:
        logging.error(f"Missing required environment variable: {var}")
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Bot token from @BotFather
API_ID = int(os.getenv("API_ID"))  # Telegram API ID
API_HASH = os.getenv("API_HASH")  # Telegram API Hash

# Channels and Admins
CHANNELS = os.getenv("CHANNELS", "-1").split()  # Default to empty list or a placeholder channel ID
ADMINS = os.getenv("ADMINS", "").split()  # Default to empty list if no admins set

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")  # MongoDB URI
DATABASE_NAME = os.getenv("DATABASE_NAME", "umz_filter_bot")  # Default to 'umz_filter_bot'

# Logging and Support
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))  # Channel ID for logs, default to 0
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "")  # Username for support chat (without @)

# Optional Features
PICS = os.getenv("PICS", "").split()  # Telegraph links for images
USE_CAPTION_FILTER = get_bool_env("USE_CAPTION_FILTER", False)
CUSTOM_FILE_CAPTION = os.getenv("CUSTOM_FILE_CAPTION", "")  # Custom file caption format
CACHE_TIME = int(os.getenv("CACHE_TIME", "60"))  # Cache time for inline queries
IMDB = get_bool_env("IMDB", True)  # IMDb integration
SINGLE_BUTTON = get_bool_env("SINGLE_BUTTON", True)  # Single or double buttons for inline buttons
P_TTI_SHOW_OFF = get_bool_env("P_TTI_SHOW_OFF", False)  # Button type (callback vs url)

# URL Shortener Configuration
SHORT_URL = os.getenv("SHORT_URL", "")  # URL Shortener site
SHORT_API = os.getenv("SHORT_API", "")  # API key for the URL shortener

# Additional Custom Features
ENABLE_GLOBAL_FILTER = get_bool_env("ENABLE_GLOBAL_FILTER", False)  # Enable global filter
ENABLE_AUTO_DELETE = get_bool_env("ENABLE_AUTO_DELETE", True)  # Enable auto deletion for filters
ENABLE_JUNK_CLEAR = get_bool_env("ENABLE_JUNK_CLEAR", True)  # Enable junk user and group clearing

# Feature Flags (Toggles for optional features)
ENABLE_IMAGE_EDITOR = get_bool_env("ENABLE_IMAGE_EDITOR", False)  # Enable image editor
ENABLE_GROUP_MANAGER = get_bool_env("ENABLE_GROUP_MANAGER", True)  # Enable group management features
ENABLE_BROADCAST = get_bool_env("ENABLE_BROADCAST", True)  # Enable broadcasting feature

# Check for missing configuration variables and log them
def log_missing_var(var_name):
    """Log a missing environment variable."""
    logging.error(f"Environment variable '{var_name}' is missing or invalid.")
    raise EnvironmentError(f"Missing or invalid environment variable: {var_name}")

if not BOT_TOKEN:
    log_missing_var("BOT_TOKEN")
if not API_ID:
    log_missing_var("API_ID")
if not API_HASH:
    log_missing_var("API_HASH")
if not DATABASE_URL:
    log_missing_var("DATABASE_URL")

# Optionally, you can add a test to verify database connectivity or other critical setups
