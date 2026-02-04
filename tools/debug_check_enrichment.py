import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def check():
    db = TextbookDB()
    try:
        # Count NOT NULL test_code
        res = db.client.table("exercises").select("*", count="exact").neq("test_code", "null").execute()
        print(f"✅ Enriched Exercises (test_code present): {res.count}")
        
        # Count Pending
        res_pending = db.client.table("exercises").select("*", count="exact").is_("test_code", "null").execute()
        print(f"⏳ Pending Exercises: {res_pending.count}")

    except Exception as e:
        print(f"Error checking table: {e}")

if __name__ == "__main__":
    check()
