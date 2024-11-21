import logging
import os
from pydub.utils import mediainfo
from telegram import InputMediaPhoto, InputMediaDocument

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_caption(file_name: str, file_path: str):
    """
    Generates a custom caption with the required format.

    Args:
    - file_name (str): Name of the file.
    - file_path (str): Path to the file to calculate its size and duration.

    Returns:
    - str: A formatted caption.
    """

    # Convert file size to a readable format
    def format_size(size: int) -> str:
        if size < 1024:
            return f"{size} Bytes"
        elif size < 1048576:
            return f"{size / 1024:.2f} KB"
        elif size < 1073741824:
            return f"{size / 1048576:.2f} MB"
        else:
            return f"{size / 1073741824:.2f} GB"

    # Get file size
    file_size = os.path.getsize(file_path)

    # Get duration of the file (if it's a video or audio)
    duration = "N/A"  # Default value for files without duration info
    resolution = "N/A"  # Default value for video resolution

    if file_path.lower().endswith(('.mp4', '.mp3', '.mkv', '.avi')):
        try:
            media_info = mediainfo(file_path)
            duration = media_info.get("duration", "N/A")
            duration = f"{int(float(duration)) // 60}m {int(float(duration)) % 60}s"  # Format as minutes and seconds
            if 'width' in media_info and 'height' in media_info:
                resolution = f"{media_info['width']}x{media_info['height']}"  # For videos, get resolution
        except Exception as e:
            logger.error(f"Error fetching media info for {file_name}: {str(e)}")
            duration = "N/A"

    # Format the caption
    caption = (
        f"@Unlimited_Movie_Zone\n\n"
        f"📕 **File Name**: {file_name}\n"
        f"💾 **Size**: {format_size(file_size)}\n"
        f"⏰ **Duration**: {duration}\n"
        f"🎬 **Resolution**: {resolution}\n"
    )

    return caption

def send_file_with_caption(update, context, file_path: str, file_name: str):
    """
    Sends a file with a custom caption using the Telegram API.

    Args:
    - update (telegram.Update): The update object containing information about the incoming message.
    - context (telegram.ext.CallbackContext): The context in which the command is executed.
    - file_path (str): The path of the file to be sent.
    - file_name (str): The name of the file.

    Returns:
    - None
    """
    # Generate the custom caption
    caption = generate_caption(file_name, file_path)

    # Send the file as a photo or document with the custom caption
    with open(file_path, 'rb') as file:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Send as a photo if it's an image
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=file,
                caption=caption
            )
        else:
            # Send as a document if it's a file
            context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file,
                caption=caption
            )
