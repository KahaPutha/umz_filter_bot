from telegram import Update
from telegram.ext import ContextTypes
from utils.database import get_all_users, get_all_chats
from config import ADMINS

# Check if the user is an admin
def is_admin(user_id: int) -> bool:
    """Check if the user is an admin based on the user ID."""
    return str(user_id) in ADMINS

# Broadcast a message to all users and groups
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast a message to all users and groups."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    # Ensure the user provides a message to broadcast
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    message = " ".join(context.args)  # Combine all arguments into a single message

    # Fetch users and chats from the database
    try:
        users = await get_all_users()
        chats = await get_all_chats()
    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching users or chats: {str(e)}")
        return

    count = 0  # Count successfully sent messages
    failed = 0  # Count failed attempts

    # Send the message to all users
    for user in users:
        try:
            await context.bot.send_message(chat_id=user["user_id"], text=message)
            count += 1
        except Exception as e:
            failed += 1
            print(f"Error sending message to user {user['user_id']}: {str(e)}")  # For debugging

    # Send the message to all groups
    for chat in chats:
        try:
            await context.bot.send_message(chat_id=chat["chat_id"], text=message)
            count += 1
        except Exception as e:
            failed += 1
            print(f"Error sending message to chat {chat['chat_id']}: {str(e)}")  # For debugging

    # Send a summary to the admin
    await update.message.reply_text(
        f"✅ Broadcast completed!\n\n"
        f"📤 Sent: {count}\n❌ Failed: {failed}"
    )
