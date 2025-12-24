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

def test_upload():
    print("Testing Cloudinary upload...")
    # Create a small dummy image content
    dummy_content = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    
    import io
    try:
        result = cloudinary.uploader.upload(
            io.BytesIO(dummy_content),
            resource_type="image",
            folder="test_folder",
            public_id="test_dummy"
        )
        print(f"Upload successful! URL: {result.get('secure_url')}")
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False

if __name__ == "__main__":
    test_upload()
