import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def inspect():
    db = TextbookDB()
    print("--- TEXTBOOK CHAPTERS ---")
    res = db.client.table("textbook_chapters").select("day, title, content_part1_theory, content_part2_practice, content_part3_mentor").order("day").execute()
    
    for row in res.data:
        d = row['day']
        t = row.get('title', 'No Title')
        has_p1 = bool(row.get('content_part1_theory'))
        has_p2 = bool(row.get('content_part2_practice'))
        has_p3 = bool(row.get('content_part3_mentor'))
        print(f"Day {d}: {t} | P1: {has_p1} | P2: {has_p2} | P3: {has_p3}")

if __name__ == "__main__":
    inspect()
