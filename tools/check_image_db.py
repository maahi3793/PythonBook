import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def check_image(image_id):
    db = TextbookDB()
    try:
        res = db.client.table("textbook_images").select("*").eq("id", image_id).execute()
        if res.data:
            print(f"✅ Found Image Record: {res.data[0]}")
        else:
            print(f"❌ Image Record NOT FOUND: {image_id}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_image("IMG_CH01_02")
