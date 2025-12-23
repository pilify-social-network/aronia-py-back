import os
from mega import Mega
from dotenv import load_dotenv
import tempfile

load_dotenv()

class MegaService:
    def __init__(self):
        self.email = os.getenv("MEGA_EMAIL")
        self.password = os.getenv("MEGA_PASSWORD")
        self.mega = Mega()
        self.m = None

    def login(self):
        if not self.m:
            if not self.email or not self.password:
                raise Exception("Mega credentials not found in environment variables")
            self.m = self.mega.login(self.email, self.password)
        return self.m

    async def upload_image(self, file_content: bytes, filename: str):
        self.login()
        
        # Create a temporary file to upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        try:
            file = self.m.upload(tmp_path)
            link = self.m.get_upload_link(file)
            return link
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    async def download_image(self, url: str):
        self.login()
        try:
            # Download file using the URL
            file_handle = self.m.find_by_link(url)
            if not file_handle:
                return None
            
            # Download to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                self.m.download(file_handle, dest_path=os.path.dirname(tmp.name), dest_filename=os.path.basename(tmp.name))
                tmp_path = tmp.name
            
            try:
                with open(tmp_path, 'rb') as f:
                    content = f.read()
                return content
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except Exception as e:
            print(f"Mega download failed: {e}")
            return None

mega_service = MegaService()
