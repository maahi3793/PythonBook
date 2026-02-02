import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def main():
    print("🔧 Attempting to make 'textbook-images' bucket PUBLIC...")
    try:
        db = TextbookDB()
        
        # Access 'storage' schema to update 'buckets' table
        # Note: 'id' in buckets table is the bucket name
        res = db.client.schema("storage").table("buckets") \
            .update({"public": True}) \
            .eq("id", "textbook-images") \
            .execute()
            
        print(f"✅ Result: {res.data}")
        print("Bucket should now be publicly accessible.")
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        print("You may need to do this manually in Supabase Dashboard > Storage > Settings.")

if __name__ == "__main__":
    main()
