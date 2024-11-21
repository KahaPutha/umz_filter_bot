from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN

# Basic Command Handlers
async def start(update, context):
    """Start Command: Sends a welcome message."""
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}! Welcome to Umz Filter Bot! 🤖"
    )

async def help_command(update, context):
    """Help Command: Lists available commands."""
    await update.message.reply_text("Here are some commands you can use:\n/start - Check bot alive\n/settings - Get settings")

# Initialize the Bot
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Register Command Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Run the Bot
if __name__ == "__main__":
    print("Umz Filter Bot is running...")
    application.run_polling()
