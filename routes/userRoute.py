from fastapi import APIRouter, Body, UploadFile, File, Form, HTTPException, Response
import os
from fastapi.encoders import jsonable_encoder
from typing import Optional

from database.db import (
    user_collection,
)
from models.userModel import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)
from services.image_service import image_service
import time

router = APIRouter()

@router.post("/sync", response_description="Sync user data from Firebase to MongoDB")
async def sync_user_data(
    uid: str = Form(...),
    name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    onboardingComplete: bool = Form(False),
    photoURL: Optional[str] = Form(None), # Add this
    image: Optional[UploadFile] = File(None)
):
    # Prepare user data
    user_data = {
        "uid": uid,
        "name": name,
        "username": username,
        "email": email,
        "phone": phone,
        "bio": bio,
        "onboardingComplete": onboardingComplete,
        "updatedAt": time.time()
    }

    # Handle image upload
    if image:
        try:
            content = await image.read()
            # Save to MongoDB
            await image_service.save_image(uid, content, image.filename)
            # Use a internal flag to indicate it's in MongoDB
            user_data["photoURL"] = "mongodb" 
        except Exception as e:
            print(f"MongoDB image save failed: {e}")
    elif photoURL:
        # If no new image but photoURL provided, sync it to MongoDB record
        user_data["photoURL"] = photoURL

    # Check if user exists
    existing_user = await user_collection.find_one({"uid": uid})
    
    if existing_user:
        # Update
        await user_collection.update_one({"uid": uid}, {"$set": user_data})
        message = "User data synchronized (updated) successfully"
    else:
        # Create
        user_data["createdAt"] = time.time()
        new_user = await user_collection.insert_one(user_data)
        message = "User data synchronized (created) successfully"

    # Fetch updated user to return
    updated_user = await user_collection.find_one({"uid": uid})
    
    # Transform photoURL to proxy link
    if updated_user and updated_user.get("photoURL"):
        # Return relative proxy path
        updated_user["photoURL"] = f"/user/avatar/{uid}"

    # Remove _id from response
    if updated_user:
        updated_user.pop("_id", None)

    # Invalidate Cache on Update
    try:
        await redis_client.delete(f"user:{uid}")
    except Exception as e:
        print(f"Redis delete error: {e}")
        
    return ResponseModel(updated_user, message)

from database.db import redis_client
import json

@router.get("/{uid}", response_description="Get user data")
async def get_user_data(uid: str):
    # 1. Try Cache
    try:
        cached_user = await redis_client.get(f"user:{uid}")
        if cached_user:
            return ResponseModel(json.loads(cached_user), "User data retrieved from cache")
    except Exception as e:
        print(f"Redis get error: {e}")

    # 2. Fetch from DB
    user = await user_collection.find_one({"uid": uid})
    if user:
        user.pop("_id", None)
        user["photoURL"] = f"/user/avatar/{uid}"
        
        # 3. Save to Cache
        try:
            await redis_client.setex(f"user:{uid}", 3600, json.dumps(user))
        except Exception as e:
            print(f"Redis set error: {e}")
            
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")

@router.get("/avatar/{uid}", response_description="Serve user avatar")
async def get_user_avatar(uid: str):
    user = await user_collection.find_one({"uid": uid})
    if not user or not user.get("photoURL"):
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    # Try fetching from MongoDB first if the photoURL is our internal marker
    if user["photoURL"] == "mongodb":
        image_content = await image_service.get_image(uid)
        if image_content:
            return Response(content=image_content, media_type="image/jpeg")
    
    raise HTTPException(status_code=404, detail="Image content not found")
    
    raise HTTPException(status_code=404, detail="Image content not found")
