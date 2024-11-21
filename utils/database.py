import pymongo
from config import DATABASE_URL, DATABASE_NAME
from bson.objectid import ObjectId
from pymongo import DESCENDING
import logging

# Setup MongoDB connection using the provided URL from the .env file
client = pymongo.MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]  # Specify the database name (defined in .env)

# Assuming you have collections like 'files', 'users', 'messages', and 'filters'
files_collection = db.get_collection("files")
users_collection = db.get_collection("users")
messages_collection = db.get_collection("messages")
filters_collection = db.get_collection("filters")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to search files based on a query
def search_files(query):
    """Search for files in the 'files' collection."""
    try:
        files = files_collection.find(query)
        logger.info(f"Found {files.count()} files for the query: {query}")
        return list(files)  # Return files as a list
    except Exception as e:
        logger.error(f"Error searching files: {e}")
        return []

# Function to add a file to the 'files' collection
def add_file(file_data):
    """Add a new file to the 'files' collection."""
    try:
        result = files_collection.insert_one(file_data)
        logger.info(f"Added file with ID {result.inserted_id}")
        return result.inserted_id  # Return the ID of the newly inserted file
    except Exception as e:
        logger.error(f"Error adding file: {e}")
        return None

# Function to get user count from the 'users' collection
def get_user_count():
    """Get the total number of users."""
    try:
        user_count = users_collection.count_documents({})
        logger.info(f"Total user count: {user_count}")
        return user_count
    except Exception as e:
        logger.error(f"Error getting user count: {e}")
        return 0

# Function to get all users with pagination
def get_all_users(page=1, page_size=10):
    """Fetch all users from the 'users' collection with pagination."""
    try:
        users = users_collection.find().skip((page - 1) * page_size).limit(page_size)
        logger.info(f"Fetched {len(users)} users on page {page}")
        return list(users)  # Return users as a list
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return []

# Function to get message count from the 'messages' collection
def get_message_count():
    """Get the total number of messages in the 'messages' collection."""
    try:
        message_count = messages_collection.count_documents({})
        logger.info(f"Total message count: {message_count}")
        return message_count
    except Exception as e:
        logger.error(f"Error getting message count: {e}")
        return 0

# Function to get all filters from the 'filters' collection
def get_all_filters():
    """Fetch all filters from the 'filters' collection."""
    try:
        filters = filters_collection.find()
        logger.info(f"Fetched {len(filters)} filters.")
        return list(filters)  # Return all filters as a list
    except Exception as e:
        logger.error(f"Error fetching filters: {e}")
        return []

# Function to get a file by its ID
def get_file_by_id(file_id):
    """Fetch a file by its ID from the 'files' collection."""
    try:
        file = files_collection.find_one({"_id": ObjectId(file_id)})
        if file:
            logger.info(f"Found file with ID {file_id}")
        else:
            logger.warning(f"No file found with ID {file_id}")
        return file
    except Exception as e:
        logger.error(f"Error fetching file by ID: {e}")
        return None

# Function to update a file's information
def update_file(file_id, update_data):
    """Update file information based on file ID."""
    try:
        result = files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {"$set": update_data}
        )
        if result.modified_count > 0:
            logger.info(f"Updated file with ID {file_id}")
        else:
            logger.warning(f"No changes made to file with ID {file_id}")
        return result.modified_count  # Return the number of modified documents
    except Exception as e:
        logger.error(f"Error updating file: {e}")
        return 0

# Function to delete a file from the 'files' collection
def delete_file(file_id):
    """Delete a file from the 'files' collection."""
    try:
        result = files_collection.delete_one({"_id": ObjectId(file_id)})
        if result.deleted_count > 0:
            logger.info(f"Deleted file with ID {file_id}")
        else:
            logger.warning(f"No file found to delete with ID {file_id}")
        return result.deleted_count  # Return the number of deleted files
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return 0

# Optionally, you can add a function to check the connection to MongoDB
def check_connection():
    """Check if the connection to MongoDB is successful."""
    try:
        # Attempt to list the databases as a connection test
        client.list_database_names()
        logger.info("Successfully connected to MongoDB!")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")

# Create indexes for optimization
def create_indexes():
    """Create indexes to optimize searches."""
    try:
        # Create indexes on frequently queried fields
        files_collection.create_index([("file_name", DESCENDING)])
        users_collection.create_index([("user_id", DESCENDING)])
        logger.info("Indexes created successfully.")
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
