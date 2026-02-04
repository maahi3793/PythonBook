import os
import sys
import re

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def repair_images():
    print("--- Starting Image DB Repair ---")
    db = TextbookDB()
    
    # 1. Fetch all chapters
    print("Fetching chapters...")
    chapters = db.client.table("textbook_chapters").select("*").execute().data
    
    found_placeholders = set()
    
    # 2. Scan Content for Placeholders
    regex = r'<!-- IMAGE_PLACEHOLDER:\s*(.*?)\s*-->'
    
    for ch in chapters:
        day = ch['day']
        print(f"Scanning Day {day}...")
        
        parts = [ch.get('content_part1_theory'), ch.get('content_part2_practice'), ch.get('content_part3_mentor')]
        
        for p in parts:
            if p:
                matches = re.findall(regex, p)
                for m in matches:
                    img_id = m.strip()
                    found_placeholders.add((img_id, day))

    print(f"Found {len(found_placeholders)} placeholders in markdown content.")
    
    # 3. Check against DB
    print("Checking DB for existing records...")
    # Fetch all existing IDs (inefficient for huge datasets but fine here)
    res = db.client.table("textbook_images").select("id").execute()
    existing_ids = {r['id'] for r in res.data}
    
    missing_count = 0
    for img_id, day in found_placeholders:
        if img_id not in existing_ids:
            print(f"⚠️ Missing Record: {img_id} (Day {day})")
            
            # 4. Insert Missing Record
            try:
                db.client.table("textbook_images").insert({
                    "id": img_id,
                    "chapter_day": day,
                    "description": "Auto-detected by repair tool (Missing AI Prompt)",
                    "status": "pending"
                }).execute()
                print(f"✅ Created record for {img_id}")
                missing_count += 1
            except Exception as e:
                print(f"❌ Failed to insert {img_id}: {e}")
                
    if missing_count == 0:
        print("✅ No missing image records found. DB is in sync.")
    else:
        print(f"🎉 Repaired {missing_count} missing image records.")

if __name__ == "__main__":
    repair_images()
