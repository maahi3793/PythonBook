import os
from supabase import create_client
from dotenv import load_dotenv

# Load Env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PyNexus", ".env")
load_dotenv(env_path)
load_dotenv() 

client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

print("--- VERIFICATION ---")
for day in [1, 2, 3]:
    res = client.table('exercises').select('id', count='exact').eq('day_number', day).execute()
    print(f"Day {day}: {len(res.data)} exercises")
print("--------------------")
