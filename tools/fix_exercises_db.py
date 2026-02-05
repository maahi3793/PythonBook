import sys
import os
from supabase import create_client
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

def fix_db():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    client = create_client(url, key)
    
    print("🧹 Starting Cleanup Operation...")

    # 1. Delete Broken Day 3 (All Day 3 rows)
    print("   Deleting Day 3 (Broken Q35)...")
    res = client.table("exercises").delete().eq("day_number", 3).execute()
    print(f"   Deleted {len(res.data) if res.data else '?'} rows from Day 3.")

    # 2. Delete Legacy Junk (Source != 'textbook')
    # Note: Q35 source is 'textbook'.
    print("   Deleting Legacy Junk (Non-Textbook)...")
    res = client.table("exercises").delete().neq("source", "textbook").execute()
    print(f"   Deleted {len(res.data) if res.data else '?'} legacy rows.")

    print("✅ Cleanup Complete. Remaining rows should be Day 1 & 2 Q35.")

if __name__ == "__main__":
    fix_db()
