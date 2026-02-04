import os
import sys
import logging
import time
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load Env
load_dotenv()

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Config Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def enrich_exercises():
    """
    Fetches exercises with NULL test_code.
    Generates Tests + Solution using Gemini.
    Updates DB.
    """
    print("--- Starting Enrichment Script v3.6 (Clean) ---", flush=True)
    db = TextbookDB()
    client = db.client
    
    # 1. Fetch Pending
    try:
        # Supabase filtering for NULL is .is_('column', 'null')
        res = client.table("exercises").select("*").is_("test_code", "null").limit(1000).execute()
        pending = res.data
        if not pending:
            print("No pending exercises found.", flush=True)
            return
        print(f"Found {len(pending)} pending exercises.", flush=True)
    except Exception as e:
        print(f"Fetch Failed: {e}", flush=True)
        return

    model = genai.GenerativeModel('gemini-flash-latest') # Verified Working Model

    for ex in pending:
        eid = ex['id']
        title = ex['title']
        desc = ex['description']
        
        print(f"🧠 Enriching: {title}...", flush=True)
        
        prompt = f"""
        You are a Python Education Engine.
        Task: Generate executable metadata for a coding exercise.
        
        Exercise Title: {title}
        Description:
        {desc}
        
        Requirements:
        1. starter_code: The 'main.py' file given to students. Should have imports and function stubs.
        2. solution_code: The working solution.
        3. test_code: A 'test_main.py' file using 'pytest'. It must import 'main' and test the functions.
        
        Output JSON ONLY:
        {{
            "starter_code": "...",
            "solution_code": "...",
            "test_code": "..."
        }}
        """
        
        try:
            resp = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            data = json.loads(resp.text)
            
            # Update DB
            client.table("exercises").update({
                "starter_code": data.get('starter_code'),
                "solution_code": data.get('solution_code'),
                "test_code": data.get('test_code')
            }).eq("id", eid).execute()
            
            # Using logger for success to keep it clean, but print shows progress
            print(f"✅ Enriched {eid}", flush=True) 
            
            # Rate Limit Protection
            time.sleep(5) 
            
        except Exception as e:
            print(f"❌ Failed {eid}: {e}", flush=True)
            time.sleep(5) # Backoff

if __name__ == "__main__":
    enrich_exercises()
