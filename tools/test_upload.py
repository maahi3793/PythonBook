import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def main():
    print("🚀 Testing Upload to 'textbook-images'...")
    try:
        db = TextbookDB()
        
        file_name = "test_upload.txt"
        file_content = b"This is a test upload from the python script."
        
        print(f"   Attempting to upload '{file_name}'...")
        
        res = db.client.storage.from_("textbook-images").upload(
            path=file_name,
            file=file_content,
            file_options={"content-type": "text/plain", "upsert": "true"}
        )
        print(f"   ✅ Upload Result: {res}")
        
        # Get URL
        url = db.client.storage.from_("textbook-images").get_public_url(file_name)
        print(f"   ✅ Public URL: {url}")
        
    except Exception as e:
        print(f"   ❌ Upload Test Failed: {e}")

if __name__ == "__main__":
    main()
