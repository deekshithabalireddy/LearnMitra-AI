
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the project root .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

# Get MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing. Please check your .env file.")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# Verify database connection
try:
    client.admin.command("ping")
    print("MongoDB Atlas connected successfully!")
except Exception as error:
    print("MongoDB connection failed:", error)
    raise

# Create database and collection
database = client["learnmitra"]
history_collection = database["learning_history"]
