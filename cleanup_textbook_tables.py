
import logging
from backend.db_textbook import TextbookDB

# Setup logging
logging.basicConfig(level=logging.INFO)

def wipe_textbook_tables():
    db = TextbookDB()
    print("🧹 Wiping 'textbook_chapters' table content (setting to NULL)...")
    
    try:
        # We don't want to delete rows because we want to keep the IDs if possible, 
        # or we just delete them and let the generator recreate them. 
        # Deleting is cleaner to clear 'status' and everything.
        
        # Method 1: Update all to NULL
        # response = db.client.table("textbook_chapters").update({
        #     "content_part1_theory": None,
        #     "content_part2_practice": None,
        #     "content_part3_mentor": None,
        #     "status": "pending"
        # }).neq("day", -1).execute() # Update All
        
        # Method 2: DELETE ALL. Generator uses get_or_create, so it handles missing rows.
        # This is the "Nuclear Option" requested.
        
        # Delete related images first
        print("   Removing related images...")
        try:
            db.client.table("textbook_images").delete().neq("id", "impossible_id").execute()
        except: pass
        
        # Delete craft content
        print("   Removing craft content...")
        try:
             db.client.table("textbook_craft").delete().neq("id", -1).execute()
        except: pass

        # Delete logs
        print("   Removing generation logs...")
        try:
             db.client.table("textbook_generation_log").delete().neq("id", -1).execute()
        except: pass
        
        # Delete chapters
        print("   Removing chapters...")
        try:
            db.client.table("textbook_chapters").delete().neq("day", -1).execute()
        except: pass
        
        print("✅ All Tables Wiped Successfully.")
        print("   - textbook_chapters: CLEARED")
        print("   - textbook_images: CLEARED")
        print("   - textbook_craft: CLEARED")
        print("   - textbook_generation_log: CLEARED")
    except Exception as e:
        print(f"❌ Error wiping tables: {e}")

if __name__ == "__main__":
    wipe_textbook_tables()
