import os
import sys
from supabase import create_client
from dotenv import load_dotenv

# Load Env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PyNexus", ".env")
load_dotenv(env_path)
load_dotenv() 

client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

DEFAULT_CODE = """# 🐍 Python Mission
# Read the instructions in the 'Briefing' tab.
# Write your solution below.

def solve():
    # Your code here
    pass

if __name__ == "__main__":
    solve()
"""

print("🔧 Fixing Missing Starter Code...")

# 1. Fetch rows with null/empty starter_code
# Note: Supabase 'is' filter for null, 'eq' for empty string
res = client.table("exercises").select("id, title").is_("starter_code", "null").execute()
null_rows = res.data

res_empty = client.table("exercises").select("id, title").eq("starter_code", "").execute()
empty_rows = res_empty.data

to_fix = null_rows + empty_rows
print(f"🧐 Found {len(to_fix)} exercises with missing starter code.")

count = 0
for row in to_fix:
    try:
        client.table("exercises").update({"starter_code": DEFAULT_CODE}).eq("id", row['id']).execute()
        count += 1
        if count % 10 == 0:
            print(f"   Fixed {count}...")
    except Exception as e:
        print(f"   ❌ Failed to fix {row['title']}: {e}")

print(f"✅ patched {count} exercises.")
