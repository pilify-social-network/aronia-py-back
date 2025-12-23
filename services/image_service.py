from bson.binary import Binary
from database.db import image_collection
import time

class ImageService:
    async def save_image(self, uid: str, content: bytes, filename: str):
        """
        Saves image binary data to MongoDB.
        If an image already exists for the UID, it overwrites it.
        """
        image_data = {
            "uid": uid,
            "filename": filename,
            "content": Binary(content),
            "updatedAt": time.time()
        }
        
        await image_collection.update_one(
            {"uid": uid},
            {"$set": image_data},
            upsert=True
        )
        return True

    async def get_image(self, uid: str):
        """
        Retrieves image binary data from MongoDB.
        """
        image = await image_collection.find_one({"uid": uid})
        if image:
            return image["content"]
        return None

image_service = ImageService()
