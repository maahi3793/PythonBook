import sys
import os
import argparse

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB
from backend.generator import TextbookGenerator

def main():
    print("🔧 Fixing Schedule Bug...")
    db = TextbookDB()
    gen = TextbookGenerator()
    
    # 1. Delete Day 2 if exists
    print("   Checking Day 2...")
    try:
        res = db.client.table("textbook_chapters").select("*").eq("day", 2).execute()
        if res.data:
            print("   ⚠️ Found Day 2. Deleting...")
            db.client.table("textbook_chapters").delete().eq("day", 2).execute()
            print("   ✅ Day 2 Deleted.")
        else:
            print("   ✅ Day 2 Clean.")
    except Exception as e:
        print(f"   ❌ Error checking Day 2: {e}")

    # 2. Check Day 1 Status
    print("   Checking Day 1...")
    day1 = None
    try:
        res = db.client.table("textbook_chapters").select("*").eq("day", 1).execute()
        if not res.data:
            print("   ❌ Day 1 Missing! (Unexpected)")
            return
        day1 = res.data[0]
        print(f"   Day 1 Status: Part1={day1.get('content_part1_theory') is not None}")
    except Exception as e:
        print(f"   ❌ Error checking Day 1: {e}")
        return

    # 3. Generate Missing Parts for Day 1
    if day1:
        print("   🚀 Generating Day 1 Part 2 (Practice)...")
        try:
            res = gen.generate_day(1, 'part2')
            print(f"   Result: {res['message']}")
        except Exception as e:
            print(f"   ❌ Error Generating Part 2: {e}")

        print("   🚀 Generating Day 1 Part 3 (Mentor)...")
        try:
            res = gen.generate_day(1, 'part3')
            print(f"   Result: {res['message']}")
        except Exception as e:
            print(f"   ❌ Error Generating Part 3: {e}")
    
    print("✅ Fix Script Finished.")

if __name__ == "__main__":
    main()
