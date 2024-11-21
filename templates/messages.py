import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Predefined Messages
WELCOME_MESSAGE = "Welcome to Umz Filter Bot! 🤖\nI am here to assist you with all your filter needs."

HELP_MESSAGE = (
    "Here are the commands you can use:\n"
    "/start - Check bot alive\n"
    "/settings - Get settings\n"
    "/ban_user - Ban a user\n"
    "/unban_user - Unban a user\n"
    "/stats - Get bot stats\n"
    "/broadcast - Send a message to all users\n"
    "/resize - Resize image\n"
    "/rotate - Rotate image\n"
    "/imdb - Get information from IMDb\n"
    "/filters - View or manage filters\n"  # Dynamically added filter management
)

# Error Messages
ERROR_GENERIC = "❌ Something went wrong. Please try again later."
ERROR_NO_PERMISSION = "❌ You do not have permission to perform this action."
ERROR_INVALID_COMMAND = "❌ Invalid command. Please use a valid command from /help."

# User Info
USER_INFO_TEMPLATE = (
    "👤 **User Info**:\n"
    "Name: {name}\n"
    "Username: @{username}\n"
    "User ID: {user_id}"
)

# Stats Template (for bot statistics)
STATS_TEMPLATE = (
    "📊 **Bot Stats**\n"
    "👤 **Total Users**: {user_count}\n"
    "⚙️ **Active Filters**: {filter_count}\n"
    "📥 **Processed Messages**: {message_count}\n"
    "💬 **Active Chats**: {active_chats}\n"
    "📅 **Uptime**: {uptime}"  # Added uptime to stats
)

# Custom Messages for various actions
def get_custom_message(action: str, user_name: str):
    """Generate a custom message based on the action and user."""
    if action == "ban":
        return f"User {user_name} has been banned."
    elif action == "unban":
        return f"User {user_name} has been unbanned."
    else:
        return f"Action {action} was performed for {user_name}."

# Function to handle errors in a specific way (e.g., for stats commands)
def handle_error(update, context, error_type="generic"):
    """Send an error message based on the error type."""
    error_message = ERROR_GENERIC
    if error_type == "permission":
        error_message = ERROR_NO_PERMISSION
    elif error_type == "invalid_command":
        error_message = ERROR_INVALID_COMMAND

    # Log the error for debugging
    logger.error(f"Error occurred: {error_message}")

    # Send the error message to the user
    update.message.reply_text(error_message)
