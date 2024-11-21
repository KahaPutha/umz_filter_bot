from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN
from modules.admin import ban_user, unban_user, leave
from modules.autofilter import auto_filter, send_file
from modules.broadcast import broadcast
from modules.group_manager import mute_user, unmute_user, promote_user, demote_user, check_user_status
from modules.image_editor import edit_image, resize_image, rotate_image
from modules.imdb import imdb
from modules.manualfilter import add_filter, view_filters, delete_filter, delete_all_filters, check_for_filter
from modules.stats import stats
from templates.captions import send_file_with_caption
from templates.messages import HELP_MESSAGE, STATS_TEMPLATE, USER_INFO_TEMPLATE
from utils.database import get_user_count, insert_user
from utils.helpers import format_size, log_activity
from utils.shortener import shorten_url
from utils.database import get_user_count, insert_user


# Basic Command Handlers
async def start(update: Update, context):
    """Start Command: Sends a welcome message."""
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}! Welcome to Umz Filter Bot! 🤖"
    )

async def help_command(update: Update, context):
    """Help Command: Lists available commands."""
    await update.message.reply_text(
        "Here are some commands you can use:\n"
        "/start - Check bot alive\n"
        "/help - Get help with commands\n"
        "/ban_user - Ban a user\n"
        "/unban_user - Unban a user\n"
        "/stats - Get stats\n"
        "/broadcast - Send a message to all users\n"
        "/resize - Resize image\n"
        "/rotate - Rotate image\n"
        "/imdb - Fetch info from IMDb\n"
        "/add_filter - Add a custom filter\n"
        "/view_filters - View active filters\n"
        "/delete_filter - Delete a filter\n"
        "/delete_all_filters - Delete all filters\n"
        "/mute_user - Mute a user\n"
        "/unmute_user - Unmute a user\n"
        "/promote_user - Promote a user to admin\n"
        "/demote_user - Demote a user from admin\n"
    )

# Initialize the Bot
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Register Basic Command Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Register Admin Command Handlers
application.add_handler(CommandHandler("ban_user", ban_user))
application.add_handler(CommandHandler("unban_user", unban_user))
application.add_handler(CommandHandler("leave", leave))

# Register Stats Command Handler
application.add_handler(CommandHandler("stats", stats))

# Register Autofilter Handlers
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_filter))  # Auto filter
application.add_handler(CallbackQueryHandler(send_file))  # Callback for sending file

# Register Broadcast Handler
application.add_handler(CommandHandler("broadcast", broadcast))

# Register Group Manager Handlers (Mute, Unmute, etc.)
application.add_handler(CommandHandler("mute_user", mute_user))
application.add_handler(CommandHandler("unmute_user", unmute_user))
application.add_handler(CommandHandler("promote_user", promote_user))
application.add_handler(CommandHandler("demote_user", demote_user))
application.add_handler(CommandHandler("check_user_status", check_user_status))

# Register Image Editing Handlers
application.add_handler(MessageHandler(filters.PHOTO, edit_image))
application.add_handler(CommandHandler("resize", resize_image))
application.add_handler(CommandHandler("rotate", rotate_image))

# Register IMDb Command Handler
application.add_handler(CommandHandler("imdb", imdb))

# Register Manual Filter Handlers
application.add_handler(CommandHandler("add_filter", add_filter))
application.add_handler(CommandHandler("view_filters", view_filters))
application.add_handler(CommandHandler("delete_filter", delete_filter))
application.add_handler(CommandHandler("delete_all_filters", delete_all_filters))

# Register the filter check handler
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_for_filter))

# Example usage when handling a file upload
async def handle_file(update, context):
    file = update.message.document  # Get the uploaded document
    file_path = "path_to_your_file"  # Replace with actual file path
    file_name = file.file_name

    # Call the function to send the file with the custom caption
    send_file_with_caption(update, context, file_path, file_name)


# Example usage of messages in the bot:
async def stats(update, context):
    # Fetch stats from your database
    user_count = get_user_count()  # Fetch the actual user count
    filter_count = 50  # Just an example, replace with actual logic
    message_count = 200  # Replace with actual message count
    active_chats = 10  # Replace with actual active chats count

    # Format the stats message
    stats_message = STATS_TEMPLATE.format(
        user_count=user_count,
        filter_count=filter_count,
        message_count=message_count,
        active_chats=active_chats
    )

    # Send the stats message to the user
    await update.message.reply_text(stats_message)


# Example usage for custom user info
async def info(update, context):
    user_name = update.effective_user.first_name
    username = update.effective_user.username
    user_id = update.effective_user.id

    user_info = USER_INFO_TEMPLATE.format(
        name=user_name,
        username=username,
        user_id=user_id
    )

    # Send the user info to the chat
    await update.message.reply_text(user_info)

# Example of using a helper function to format a file size
file_size = format_size(204800)  # 200 KB
print(file_size)

# Example of using the database functions
user_count = get_user_count()
print(f"Total users: {user_count}")

# Example of using the URL shortener
short_url = shorten_url("https://www.example.com/long-url")
print(f"Shortened URL: {short_url}")

# Run the Bot
if __name__ == "__main__":
    print("Umz Filter Bot is running...")
    application.run_polling()
