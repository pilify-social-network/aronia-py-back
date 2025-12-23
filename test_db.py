import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

async def test_connection():
    load_dotenv()
    mongo_details = os.getenv("MONGO_DETAILS")
    print(f"Testing connection to: {mongo_details}")
    
    try:
        client = AsyncIOMotorClient(mongo_details)
        # The client doesn't connect until the first query
        server_info = await client.server_info()
        print("Successfully connected to MongoDB!")
        print(f"Server info: {server_info.get('version')}")
        
        database = client.aronia_db
        user_collection = database.get_collection("users_collection")
        
        count = await user_collection.count_documents({})
        print(f"Users in collection: {count}")
        
    except Exception as e:
        print(f"FAILED to connect to MongoDB: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
