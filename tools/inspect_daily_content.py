import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def inspect():
    db = TextbookDB()
    # Fetch Day 1 or 2
    print("--- Fetching Day 2 Content ---")
    data = db.client.table("daily_content").select("*").eq("day", 2).execute()
    
    if data.data:
        row = data.data[0]
        print(f"TOPIC: {row.get('topic')}")
        print("CONTENT SNIPPET:")
        print(row.get('content')[:1000]) # Print first 1000 chars
        print("..." * 10)
        
        # Check for "Assignment" keyword
        content = row.get('content', '')
        if "Assignment" in content:
            print("✅ Found 'Assignment' keyword.")
            # Find context
            idx = content.find("Assignment")
            print(content[idx:idx+200])
        else:
            print("❌ 'Assignment' keyword not found in Day 2.")
    else:
        print("No data for Day 2.")

if __name__ == "__main__":
    inspect()
