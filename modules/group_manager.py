from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from config import ADMINS

# Check if the user is an admin
def is_admin(user_id: int) -> bool:
    """Check if the user is an admin based on user ID."""
    return str(user_id) in ADMINS

# Ban a user from a group
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user from the group."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /ban_user <user_id>")
        return

    user_id = context.args[0]

    try:
        await context.bot.kick_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text(f"✅ User {user_id} has been banned.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error banning user: {str(e)}")

# Unban a user from a group
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a user from the group."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /unban_user <user_id>")
        return

    user_id = context.args[0]

    try:
        await context.bot.unban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text(f"✅ User {user_id} has been unbanned.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error unbanning user: {str(e)}")

# Mute a user in a group
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mute a user in the group."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /mute_user <user_id>")
        return

    user_id = context.args[0]

    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, user_id, can_send_messages=False)
        await update.message.reply_text(f"✅ User {user_id} has been muted.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error muting user: {str(e)}")

# Unmute a user in a group
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unmute a user in the group."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /unmute_user <user_id>")
        return

    user_id = context.args[0]

    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, user_id, can_send_messages=True)
        await update.message.reply_text(f"✅ User {user_id} has been unmuted.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error unmuting user: {str(e)}")

# Promote or demote a user to/from admin
async def promote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Promote a user to admin in the group."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /promote_user <user_id>")
        return

    user_id = context.args[0]

    try:
        await context.bot.promote_chat_member(update.effective_chat.id, user_id, can_change_info=True, can_post_messages=True, can_pin_messages=True)
        await update.message.reply_text(f"✅ User {user_id} has been promoted to admin.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error promoting user: {str(e)}")

# Demote a user from admin
async def demote_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Demote a user from admin in the group."""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this command!")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /demote_user <user_id>")
        return

    user_id = context.args[0]

    try:
        await context.bot.promote_chat_member(update.effective_chat.id, user_id, can_change_info=False, can_post_messages=False, can_pin_messages=False)
        await update.message.reply_text(f"✅ User {user_id} has been demoted from admin.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error demoting user: {str(e)}")

# Check the user's current status (admin/member)
async def check_user_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check the current status of a user in the group."""
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /check_user_status <user_id>")
        return

    user_id = context.args[0]

    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        if member.status == ChatMember.ADMINISTRATOR:
            status = "Admin"
        elif member.status == ChatMember.MEMBER:
            status = "Member"
        else:
            status = "Not a member or banned"
        await update.message.reply_text(f"User {user_id} is a {status}.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error checking status: {str(e)}")
