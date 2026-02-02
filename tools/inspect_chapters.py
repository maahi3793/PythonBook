import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def main():
    print("🕵️ Inspecting Chapters...")
    db = TextbookDB()
    
    res = db.client.table("textbook_chapters").select("*").order("day").execute()
    
    if not res.data:
        print("No chapters found.")
        return
        
    for ch in res.data:
        print(f"Day {ch['day']}: {ch['title']}")
        print(f"  - Status: {ch['status']}")
        print(f"  - Part 1: {'✅' if ch.get('content_part1_theory') else '❌'}")
        print(f"  - Part 2: {'✅' if ch.get('content_part2_practice') else '❌'}")
        print(f"  - Part 3: {'✅' if ch.get('content_part3_mentor') else '❌'}")

if __name__ == "__main__":
    main()
