import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def check():
    db = TextbookDB()
    try:
        res = db.client.table("exercises").select("*", count="exact").execute()
        print(f"Total Rows in 'exercises': {len(res.data)}")
        if res.data:
            print("First Row Sample:", res.data[0])
    except Exception as e:
        print(f"Error checking table: {e}")

if __name__ == "__main__":
    check()
