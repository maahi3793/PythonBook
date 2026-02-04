import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def reset():
    db = TextbookDB()
    print("--- RESETTING TEXTBOOK ---")
    
    # Check what we have
    res = db.client.table("textbook_chapters").select("day").execute()
    days = sorted([r['day'] for r in res.data])
    print(f"Existing Days: {days}")
    
    if len(days) == 0:
        print("Empty DB!")
        return

    # Delete everything > Day 1
    to_delete = [d for d in days if d > 1]
    
    if not to_delete:
        print("Nothing to delete (Only Day 1 exists).")
        return
        
    print(f"Deleting Days: {to_delete}...")
    
    for d in to_delete:
        db.client.table("textbook_chapters").delete().eq("day", d).execute()
        print(f"Deleted Day {d}")
        
    print("✅ Reset Complete. Database now contains only Day 1 (or nothing lower).")
    print("Next Auto-Run will target Day 2.")

if __name__ == "__main__":
    reset()
