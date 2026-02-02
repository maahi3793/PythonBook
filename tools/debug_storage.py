import sys
import os
import requests

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def main():
    print("🕵️ Debugging Supabase Storage: 'textbook-images'")
    db = TextbookDB()
    bucket = "textbook-images"
    
    # 1. List Files
    print("\n[1] Listing Files in Bucket...")
    try:
        files = db.client.storage.from_(bucket).list()
        if not files:
            print("   ⚠️ Bucket appears empty or list failed.")
        else:
            print(f"   found {len(files)} files.")
            for f in files[:5]: # Show first 5
                print(f"   - {f['name']} ({f['metadata']['mimetype']} - {f['metadata']['size']} bytes)")
    except Exception as e:
        print(f"   ❌ List Failed: {e}")
        return

    # 2. Test Public Access (using first file)
    if files:
        test_file = files[0]['name']
        print(f"\n[2] Testing Public URL for: {test_file}")
        
        public_url = db.client.storage.from_(bucket).get_public_url(test_file)
        print(f"   URL: {public_url}")
        
        # Test HTTP codes
        try:
            resp = requests.head(public_url)
            print(f"   HTTP Status: {resp.status_code}")
            if resp.status_code == 200:
                print("   ✅ Access OK.")
            elif resp.status_code == 404:
                print("   ❌ 404 Not Found.")
            elif resp.status_code == 403:
                print("   ❌ 403 Forbidden (Permissions).")
            else:
                print(f"   ❌ Status {resp.status_code}")
        except Exception as e:
            print(f"   Request Error: {e}")

if __name__ == "__main__":
    main()
