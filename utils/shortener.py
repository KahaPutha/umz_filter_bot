# utils/shortner.py
import pyshorteners
from config import SHORT_API, SHORT_URL

# Initialize the URL shortener object
shortener = pyshorteners.Shortener(api_key=SHORT_API)

# Function to shorten a URL using TinyURL
def shorten_url(url):
    try:
        # Using TinyURL to shorten the URL
        short_url = shortener.tinyurl.short(url)
        return short_url
    except Exception as e:
        return f"Error shortening URL: {str(e)}"

# Function to use a custom URL shortener (if different from TinyURL)
def custom_shorten_url(url):
    """
    This function allows you to implement custom URL shortening logic
    if you prefer using a service other than TinyURL.
    For example, you can integrate Bitly or other URL shortening services.
    """
    pass
