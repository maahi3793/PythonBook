import os
import sys
from supabase import create_client
from dotenv import load_dotenv
from collections import Counter

# Load Env
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

if not url or not key:
    print("❌ Error: Missing Supabase Credentials")
    sys.exit(1)

client = create_client(url, key)

print("🔍 querying Day 2 Exercises...")
res = client.table("exercises").select("*").eq("day_number", 2).execute()

data = res.data
print(f"✅ Total Rows: {len(data)}")

counts = Counter([r['difficulty'] for r in data])
print("📊 Difficulty Breakdown:")
for diff, count in counts.items():
    print(f"   - {diff}: {count}")

if len(data) < 35:
    print("\n⚠️ WARNING: Missing Exercises! Expected 35.")
else:
    print("\n✅ DATA LOOKS GOOD (Quantity-wise). Check UI Filter.")
