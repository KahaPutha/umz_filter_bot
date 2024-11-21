import logging
import os
from datetime import datetime

# Configure logging for bot activities (optional: can log to a file or console)
logging.basicConfig(
    level=logging.INFO,  # You can change this to logging.DEBUG for more verbose output
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("logs", "bot_activity.log"))  # Log to file (optional)
    ]
)


# Function to format file sizes (e.g., KB, MB, GB)
def format_size(size_in_bytes):
    """Format bytes into human-readable size (KB, MB, GB)."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 ** 3:
        return f"{size_in_bytes / 1024 ** 2:.2f} MB"
    else:
        return f"{size_in_bytes / 1024 ** 3:.2f} GB"


# Function to log bot activity (could be saved to a file or external service)
def log_activity(message, level="INFO"):
    """Log activity to both console and file."""
    log_message = f"[{level}]: {message}"

    # Log message to console
    if level == "INFO":
        logging.info(log_message)
    elif level == "ERROR":
        logging.error(log_message)
    elif level == "WARNING":
        logging.warning(log_message)

    # Optionally save logs to a file (can be expanded to include log rotation)
    log_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Save log message to a file
    with open(os.path.join(log_dir, "bot_activity.log"), "a") as file:
        file.write(f"{datetime.now()} - {message}\n")


# Function to handle errors gracefully
def handle_error(error_message, critical=False):
    """Handle errors gracefully and log them."""
    if critical:
        log_activity(f"Critical Error: {error_message}", level="ERROR")
        # Additional actions like sending the error message to admins can be added here
    else:
        log_activity(f"Error: {error_message}", level="ERROR")

    # Optionally, you can raise an exception for critical errors or just log them
    if critical:
        raise Exception(error_message)


# Function to calculate the duration between two timestamps
def format_duration(start_time, end_time):
    """Return the duration between two timestamps in a human-readable format."""
    duration = end_time - start_time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours}h {minutes}m {seconds}s"


# Function to validate if a file is an image (or any other specific file type)
def validate_file_type(file_path, allowed_extensions=None):
    """Validate if the file has an allowed extension."""
    if allowed_extensions is None:
        allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in allowed_extensions:
        return True
    else:
        return False


# Function to check if a file exists in the given path (can be used for checking cache files)
def file_exists(file_path):
    """Check if a file exists in the specified path."""
    return os.path.exists(file_path)
