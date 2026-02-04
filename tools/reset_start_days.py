import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def wipe_start():
    db = TextbookDB()
    print("--- WIPING DAYS 1, 2, 3 ---")
    
    # 1. Delete Images
    res = db.client.table("textbook_images").delete().in_("chapter_day", [1, 2, 3]).execute()
    print(f"Deleted Images: {res}")
    
    # 2. Delete Chapters
    res = db.client.table("textbook_chapters").delete().in_("day", [1, 2, 3]).execute()
    print(f"Deleted Chapters: {res}")
    
    # 3. Delete Logs? Optional.
    
if __name__ == "__main__":
    wipe_start()
