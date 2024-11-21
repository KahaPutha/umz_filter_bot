from telegram import Update
from telegram.ext import ContextTypes
from config import ADMINS
from utils.database import get_user_count, get_all_users  # Import database functions for stats


# Check if the user is an admin
def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMINS


# Command: Ban User
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /ban_user <user_id>")
        return

    user_id = context.args[0]

    # Logic to ban the user (could be saving to a 'banned_users' collection or flagging in the database)
    try:
        # Placeholder for actual banning logic (this will vary based on your implementation)
        # For example: ban_user_in_db(user_id)
        await update.message.reply_text(f"✅ User {user_id} has been banned.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error banning user: {e}")


# Command: Unban User
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /unban_user <user_id>")
        return

    user_id = context.args[0]

    # Logic to unban the user (e.g., removing the user from a 'banned_users' collection)
    try:
        # Placeholder for actual unbanning logic
        # For example: unban_user_in_db(user_id)
        await update.message.reply_text(f"✅ User {user_id} has been unbanned.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error unbanning user: {e}")


# Command: Get Bot Stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    # Fetch stats using the database functions
    try:
        users_count = get_user_count()  # Get the total number of users
        # Example for active chats count, this may vary depending on your implementation
        chats_count = 45  # Placeholder for active chats count
        await update.message.reply_text(
            f"📊 **Bot Stats:**\n- Total Users: {users_count}\n- Total Chats: {chats_count}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching stats: {e}")


# Command: Leave a Chat
async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /leave <chat_id>")
        return

    chat_id = context.args[0]
    try:
        await context.bot.leave_chat(chat_id)
        await update.message.reply_text(f"✅ Left chat {chat_id} successfully.")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to leave chat {chat_id}: {e}")
