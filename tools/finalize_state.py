import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def finalize_state():
    db = TextbookDB()
    
    # 1. Wipe 4 and 5
    print("--- WIPING DAYS 4, 5 ---")
    db.client.table("textbook_chapters").delete().in_("day", [4, 5]).execute()
    db.client.table("textbook_images").delete().in_("chapter_day", [4, 5]).execute()
    print("Days 4 & 5 Wiped.")
    
if __name__ == "__main__":
    finalize_state()
