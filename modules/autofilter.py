import os
from telegram import Update, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from config import USE_CAPTION_FILTER, CUSTOM_FILE_CAPTION
from utils.database import search_files, add_file, get_file_by_id, update_file, delete_file, files_collection
from utils.helpers import generate_caption


# Function to handle auto-filtering of messages
async def auto_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Automatically filter messages."""
    try:
        message_text = update.message.text.lower()  # Get the incoming message text

        # Apply caption filter if enabled, otherwise filter by filename
        if USE_CAPTION_FILTER:
            filtered_files = search_files({"caption": {"$regex": message_text, "$options": "i"}})
        else:
            filtered_files = search_files({"filename": {"$regex": message_text, "$options": "i"}})

        # If there are files found, send them to the user
        if filtered_files:
            for file in filtered_files:
                file_caption = CUSTOM_FILE_CAPTION.format(
                    filename=file.get("filename"),
                    filesize=file.get("filesize"),
                    duration=file.get("duration")
                ) if CUSTOM_FILE_CAPTION else generate_caption(file)

                # Send the file to the user
                await update.message.reply_document(
                    document=file.get("file_id"),
                    caption=file_caption,
                )
        else:
            await update.message.reply_text("No files found matching your query.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error filtering message: {str(e)}")


# Function to handle file sending
async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a specific file based on the query."""
    try:
        query_data = update.callback_query.data  # Get the query data

        # Get file by ID from the database
        file = get_file_by_id(query_data)
        if file:
            file_caption = CUSTOM_FILE_CAPTION.format(
                filename=file.get("filename"),
                filesize=file.get("filesize"),
                duration=file.get("duration")
            ) if CUSTOM_FILE_CAPTION else generate_caption(file)

            # Send the file to the user
            await update.callback_query.message.reply_document(
                document=file.get("file_id"),
                caption=file_caption
            )
        else:
            await update.callback_query.message.reply_text("File not found.")

    except Exception as e:
        await update.callback_query.message.reply_text(f"❌ Error sending file: {str(e)}")


# Function to add a new file (manual filter)
async def add_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a new file to the filter database."""
    try:
        file_id = update.message.document.file_id  # Get file ID from the message
        file_name = update.message.document.file_name  # Get file name from the message
        file_size = update.message.document.file_size  # Get file size
        duration = None  # Duration can be handled if needed for videos/audio

        # Prepare file data for database insertion
        file_data = {
            "file_id": file_id,
            "filename": file_name,
            "filesize": file_size,
            "duration": duration
        }

        # Add the file to the database
        inserted_id = add_file(file_data)
        if inserted_id:
            await update.message.reply_text(f"File {file_name} added to the database successfully!")
        else:
            await update.message.reply_text("❌ Error adding file to the database.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error adding file: {str(e)}")


# Function to delete a filter (delete a specific file)
async def delete_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a specific file from the filter database."""
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Usage: /delete_filter <file_id>")
            return

        file_id = context.args[0]  # Get file ID from arguments
        deleted_count = delete_file(file_id)  # Delete the file from the database
        if deleted_count > 0:
            await update.message.reply_text(f"File with ID {file_id} deleted successfully!")
        else:
            await update.message.reply_text(f"❌ Error deleting file with ID {file_id}. File may not exist.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error deleting filter: {str(e)}")


# Function to delete all filters (clear all files from the filter)
async def delete_all_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete all filters (clear all files)."""
    try:
        files_deleted = files_collection.delete_many({})  # Delete all files from the collection
        if files_deleted.deleted_count > 0:
            await update.message.reply_text(f"✅ All files deleted successfully!")
        else:
            await update.message.reply_text(f"❌ No files to delete.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error deleting all filters: {str(e)}")


# Function to check if a filter exists (file lookup)
async def check_for_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if a filter exists (check if file exists in the database)."""
    try:
        message_text = update.message.text.lower()  # Get the incoming message text

        # Search for a file matching the query
        files = search_files({"filename": {"$regex": message_text, "$options": "i"}})

        # If files are found, show the first file as the result
        if files:
            file = files[0]  # Assuming the first result is the desired one
            file_caption = CUSTOM_FILE_CAPTION.format(
                filename=file.get("filename"),
                filesize=file.get("filesize"),
                duration=file.get("duration")
            ) if CUSTOM_FILE_CAPTION else generate_caption(file)

            await update.message.reply_text(
                f"Filter found: {file.get('filename')}\n{file_caption}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Send File", callback_data=str(file["_id"]))
                ]])
            )
        else:
            await update.message.reply_text("No matching filter found.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error checking filter: {str(e)}")


# Function to generate a caption for a file (can be customized)
def generate_caption(file):
    """Generate a default caption for a file."""
    return f"📁 {file.get('filename')} \n💾 Size: {file.get('filesize')} bytes"


# Register Handlers in main.py
def register_handlers(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_filter))  # Auto filter
    application.add_handler(MessageHandler(filters.DOCUMENT, add_file_handler))  # Add file manually
    application.add_handler(CommandHandler("delete_filter", delete_filter))  # Delete a filter
    application.add_handler(CommandHandler("delete_all_filters", delete_all_filters))  # Delete all filters
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_for_filter))  # Check for filter
