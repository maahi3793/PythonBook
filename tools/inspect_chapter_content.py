import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def inspect():
    db = TextbookDB()
    rows = db.client.table("textbook_chapters").select("content_part1_theory").eq("day", 1).execute()
    if rows.data:
        print(rows.data[0]['content_part1_theory'][:2000]) # First 2000 chars

if __name__ == "__main__":
    inspect()
