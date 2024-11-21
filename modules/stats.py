import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import DATABASE_URL
import pymongo
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the DATABASE_NAME from environment variables
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Setup MongoDB connection
client = pymongo.MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]  # Use the DATABASE_NAME from .env

# Assuming you have collections for users, messages, filters, and active chats
users_collection = db.get_collection("users")
messages_collection = db.get_collection("messages")
filters_collection = db.get_collection("filters")
active_chats_collection = db.get_collection("active_chats")  # Track active chats

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to get basic bot stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch bot statistics like user count, active chats, and filter count."""
    try:
        # Get number of users
        user_count = users_collection.count_documents({})

        # Get number of active filters
        filter_count = filters_collection.count_documents({})

        # Get the number of messages processed
        message_count = messages_collection.count_documents({})

        # Get number of active chats (from the active_chats collection)
        active_chats_count = active_chats_collection.count_documents({})

        # Prepare the response message
        stats_message = (
            f"📊 **Bot Stats**\n"
            f"👤 **Total Users**: {user_count}\n"
            f"💬 **Active Chats**: {active_chats_count}\n"
            f"⚙️ **Active Filters**: {filter_count}\n"
            f"📥 **Processed Messages**: {message_count}\n"
        )

        await update.message.reply_text(stats_message)

    except Exception as e:
        # Log the error and send a user-friendly message
        logger.error(f"Error fetching stats: {str(e)}")
        await update.message.reply_text(f"❌ Error fetching stats. Please try again later.")
