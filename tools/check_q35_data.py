import sys
import os
import json
from supabase import create_client
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

def check_data():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    client = create_client(url, key)
    
    # Fetch 1 exercise from Day 1
    res = client.table("exercises").select("*").eq("day_number", 1).limit(1).execute()
    
    if res.data:
        ex = res.data[0]
        print(f"Checking Exercise: {ex.get('title')}")
        print(f"Starter Code Length: {len(ex.get('starter_code', ''))}")
        print(f"Test Code Length: {len(ex.get('test_code', ''))}")
        print(f"Solution Code Length: {len(ex.get('solution_code', ''))}")
        
        if ex.get('starter_code') and ex.get('test_code') and ex.get('solution_code'):
             print("✅ COMPLETE: All code fields present.")
        else:
             print("❌ INCOMPLETE: Missing fields.")
    else:
        print("❌ No exercises found for Day 1.")

if __name__ == "__main__":
    check_data()
