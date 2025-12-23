import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import urllib.parse
import sys

load_dotenv()

# Example: mongodb://username:password@localhost:27017
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

client = None
database = None
user_collection = None

try:
    client = AsyncIOMotorClient(MONGO_DETAILS)
    database = client.aronia_db
    user_collection = database.get_collection("users_collection")
    image_collection = database.get_collection("images_collection")
    # Trigger a quick check (optional, but AsyncIOMotorClient is lazy)
except Exception as e:
    print(f"\nERROR: Could not connect to MongoDB: {e}")
    if "escaped" in str(e).lower() or "RFC 3986" in str(e):
        print("\n[!] TIP: Your MongoDB password likely contains special characters (like '@', ':', '#').")
        print("[!] You MUST URL-encode these characters in your .env file.")
        print("[!] Use this to encode your password:")
        print("    python -c \"import urllib.parse; print(urllib.parse.quote_plus('your_password'))\"")
    print("\n")
