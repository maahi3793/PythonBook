import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def inspect_failure():
    db = TextbookDB()
    print("--- TEXTBOOK CHAPTERS DUMP ---")
    
    # Fetch ALL chapters
    res = db.client.table("textbook_chapters").select("*").order("day").execute()
    
    if not res.data:
        print("No chapters found.")
        return
        
    for ch in res.data:
        d = ch['day']
        t = ch.get('title', 'No Title')
        p1 = bool(ch.get('content_part1_theory'))
        p2 = bool(ch.get('content_part2_practice'))
        p3 = bool(ch.get('content_part3_mentor'))
        print(f"Day {d}: {t} | P1={p1} | P2={p2} | P3={p3} | ID={ch.get('id')}")

if __name__ == "__main__":
    inspect_failure()
