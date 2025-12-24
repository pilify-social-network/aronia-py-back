from database.db import fs
import motor.motor_asyncio
import bson
import io
import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

class MediaService:
    async def save_media(self, content: bytes, filename: str, media_type: str) -> str:
        """
        Saves media content to Cloudinary and returns the secure URL.
        """
        print(f"DEBUG: Cloudinary saving {filename}...")
        try:
            # Determine resource type
            resource_type = "video" if "video" in media_type else "image"
            
            # Upload to Cloudinary using a BytesIO stream
            upload_result = cloudinary.uploader.upload(
                content,
                resource_type=resource_type,
                folder="aronia_posts",
                public_id=filename.split('.')[0] if '.' in filename else filename
            )
            
            secure_url = upload_result.get("secure_url")
            print(f"DEBUG: Cloudinary save successful. URL: {secure_url}")
            return secure_url
        except Exception as e:
            print(f"DEBUG: Cloudinary save error: {str(e)}")
            raise e

    async def get_media(self, media_id: str):
        """
        Retrieves media content and media_type from GridFS.
        """
        try:
            obj_id = bson.ObjectId(media_id)
            grid_out = await fs.open_download_stream(obj_id)
            content = await grid_out.read()
            media_type = grid_out.metadata.get("contentType", "application/octet-stream")
            return content, media_type
        except Exception as e:
            print(f"Error retrieving media {media_id}: {e}")
            return None, None

media_service = MediaService()
