import json
import os
import sys
from supabase import create_client
from dotenv import load_dotenv

# Load Env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PyNexus", ".env")
load_dotenv(env_path)
load_dotenv() # Fallback

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")
client = create_client(url, key)

INPUT_FILE = r"C:\Users\reach\.gemini\antigravity\scratch\relaunchpython\PythonBook\assets\exercises.json"

def ingest():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ File not found: {INPUT_FILE}")
        return

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("❌ Invalid JSON: Expected a list of objects.")
            return

        print(f"📦 Found {len(data)} exercises. Ingesting...")
        
        count = 0
        for item in data:
            # Enforce source tag
            item['source'] = 'manual_external'
            
            # Field Mapping (JSON -> DB)
            if 'description_md' in item:
                item['description'] = item.pop('description_md')
            
            # Slug -> Filename Mapping
            # The DB requires 'filename' as a unique key for many things
            if 'slug' in item and 'filename' not in item:
                 item['filename'] = f"{item.pop('slug')}.py"
            elif 'filename' not in item:
                 # Fallback if neither exists
                 item['filename'] = f"day{item.get('day_number','x')}_{item.get('title','unknown').replace(' ','_')}.py"

            try:
                # Manual Upsert (Delete then Insert) to avoid "ON CONFLICT" error if no unique constraint exists
                fname = item.get('filename')
                if fname:
                    client.table("exercises").delete().eq("filename", fname).execute()
                
                client.table("exercises").insert(item).execute()
                
                count += 1
                if count % 10 == 0:
                    print(f"   Saved {count}...")
            except Exception as e:
                print(f"   ⚠️ Error saving {item.get('title')}: {e}")

        print(f"✅ Successfully ingested {count} exercises.")

    except Exception as e:
        print(f"❌ Crash: {e}")

if __name__ == "__main__":
    ingest()
