from telegram import Update
from telegram.ext import ContextTypes
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to download and open an image from a photo message
async def get_image_from_message(update: Update):
    """Helper function to download and open the image from the user's message."""
    if update.message.photo:
        # Get the largest photo from the list
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_bytes = await file.download_as_bytearray()

        try:
            # Open the image using PIL
            image = Image.open(BytesIO(file_bytes))
            return image
        except Exception as e:
            logger.error(f"Error opening image: {e}")
            await update.message.reply_text("❌ Error processing image.")
            return None
    else:
        await update.message.reply_text("❌ No image found. Please send an image to edit.")
        return None

# Function to handle image editing (resize, rotate, etc.)
async def edit_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image = await get_image_from_message(update)
    if not image:
        return

    try:
        # Example: Resize the image to 500x500 pixels
        edited_image = image.resize((500, 500))

        # Optionally add text to the image
        draw = ImageDraw.Draw(edited_image)
        font = ImageFont.load_default()  # Use default font
        text = "Edited by Umz Filter Bot"
        draw.text((10, 10), text, font=font, fill="white")

        # Save the edited image into a byte buffer
        byte_io = BytesIO()
        edited_image.save(byte_io, format="PNG")
        byte_io.seek(0)

        # Send the edited image back to the user
        await update.message.reply_photo(photo=byte_io, caption="Here is your edited image!")
    except Exception as e:
        logger.error(f"Error editing image: {e}")
        await update.message.reply_text(f"❌ Error editing image: {e}")

# Function to resize image
async def resize_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image = await get_image_from_message(update)
    if not image:
        return

    try:
        # Resize the image to 800x800 pixels
        edited_image = image.resize((800, 800))

        # Save the resized image into a byte buffer
        byte_io = BytesIO()
        edited_image.save(byte_io, format="PNG")
        byte_io.seek(0)

        # Send the resized image back to the user
        await update.message.reply_photo(photo=byte_io, caption="Here is your resized image!")
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        await update.message.reply_text(f"❌ Error resizing image: {e}")

# Function to rotate image
async def rotate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image = await get_image_from_message(update)
    if not image:
        return

    try:
        # Rotate the image by 90 degrees
        edited_image = image.rotate(90)

        # Save the rotated image into a byte buffer
        byte_io = BytesIO()
        edited_image.save(byte_io, format="PNG")
        byte_io.seek(0)

        # Send the rotated image back to the user
        await update.message.reply_photo(photo=byte_io, caption="Here is your rotated image!")
    except Exception as e:
        logger.error(f"Error rotating image: {e}")
        await update.message.reply_text(f"❌ Error rotating image: {e}")
