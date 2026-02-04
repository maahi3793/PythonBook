import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def inspect():
    db = TextbookDB()
    print("--- Fetching Day 3 (Assessment) ---")
    data = db.client.table("textbook_chapters").select("*").eq("day", 3).execute()
    
    if data.data:
        row = data.data[0]
        # Check all parts
        p1 = row.get('content_part1_theory', '')
        p2 = row.get('content_part2_practice', '')
        
        print(f"Part 1 Length: {len(p1)}")
        print(f"Part 2 Length: {len(p2)}")
        
        print("\n--- Snippet Part 1 ---")
        print(p1[:500])
        print("\n--- Snippet Part 2 ---")
        print(p2[:500])
    
    # Also Check Day 4 (Normal)
    print("\n--- Fetching Day 4 (Normal) ---")
    data4 = db.client.table("textbook_chapters").select("*").eq("day", 4).execute()
    if data4.data:
        row = data4.data[0]
        p2 = row.get('content_part2_practice', '')
        print("\n--- Day 4 Part 2 Snippet ---")
        print(p2[:500])

if __name__ == "__main__":
    inspect()
