from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from services.media_service import media_service
import os

router = APIRouter()

@router.post("/upload", response_description="Upload media for a post")
async def upload_media(file: UploadFile = File(...)):
    print(f"DEBUG: Received upload request for {file.filename} ({file.content_type})")
    MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
    
    try:
        content = await file.read()
        print(f"DEBUG: Read {len(content)} bytes")
        
        if file.content_type and "video" in file.content_type and len(content) > MAX_VIDEO_SIZE:
            print("DEBUG: Video too large")
            raise HTTPException(status_code=400, detail="Video too large. Max size is 50MB.")

        media_url = await media_service.save_media(content, file.filename, file.content_type)
        print(f"DEBUG: Media saved at: {media_url}")
        
        return {
            "mediaId": media_url.split('/')[-1], # Placeholder/Ref
            "mediaType": file.content_type,
            "url": media_url
        }
    except Exception as e:
        print(f"DEBUG: Upload error in route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

from database.db import redis_client

@router.get("/media/{media_id}", response_description="Get post media")
async def get_media(media_id: str):
    # 1. Try Cache
    try:
        cached_content = await redis_client.get(f"media:{media_id}")
        cached_type = await redis_client.get(f"media:{media_id}:type")
        
        if cached_content and cached_type:
            return Response(content=cached_content, media_type=cached_type.decode('utf-8'))
    except Exception as e:
        print(f"Redis error: {e}")

    # 2. Fetch from DB
    content, media_type = await media_service.get_media(media_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Media not found")
        
    # 3. Save to Cache (Expiration: 1 hour)
    try:
        await redis_client.setex(f"media:{media_id}", 3600, content)
        await redis_client.setex(f"media:{media_id}:type", 3600, media_type)
    except Exception as e:
        print(f"Redis set error: {e}")

    return Response(content=content, media_type=media_type)
