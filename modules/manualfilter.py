from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler
from config import ADMINS  # Assuming you have a list of admins

# In-memory storage for filters (you can replace this with a database or file)
filters = []

# Helper function to check if a user is an admin
def is_admin(user_id: int) -> bool:
    """Check if the user is an admin."""
    return user_id in ADMINS

# Add a new manual filter
async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a new filter to the list."""
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ You do not have permission to add filters.")
        return

    if context.args:
        # Get the filter word/phrase
        new_filter = ' '.join(context.args).lower()
        filters.append(new_filter)
        await update.message.reply_text(f"✅ Filter '{new_filter}' added successfully!")
    else:
        await update.message.reply_text("❌ Please provide a word or phrase to add as a filter.")

# View all the active filters
async def view_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all active filters."""
    if not filters:
        await update.message.reply_text("❌ No filters are currently active.")
        return

    filters_list = "\n".join(filters)
    await update.message.reply_text(f"Here are the active filters:\n{filters_list}")

# Delete a specific filter
async def delete_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a specific filter."""
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ You do not have permission to delete filters.")
        return

    if context.args:
        # Get the filter to delete
        filter_to_delete = ' '.join(context.args).lower()
        if filter_to_delete in filters:
            filters.remove(filter_to_delete)
            await update.message.reply_text(f"✅ Filter '{filter_to_delete}' deleted successfully!")
        else:
            await update.message.reply_text(f"❌ Filter '{filter_to_delete}' not found.")
    else:
        await update.message.reply_text("❌ Please provide a filter to delete.")

# Delete all filters
async def delete_all_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete all filters."""
    if not is_admin(update.message.from_user.id):
        await update.message.reply_text("❌ You do not have permission to delete all filters.")
        return

    filters.clear()
    await update.message.reply_text("✅ All filters have been cleared.")

# Manual filter action: Detect filters in incoming messages
async def check_for_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the incoming message contains any of the filters."""
    message_text = update.message.text.lower()

    # Check if any of the active filters are in the message
    for filter_word in filters:
        if filter_word in message_text:
            await update.message.delete()  # Optionally delete the message
            await update.message.reply_text(f"❌ Your message contained a forbidden word/phrase: '{filter_word}'. It has been deleted.")
            break
