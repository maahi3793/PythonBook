import os
import sys
from supabase import create_client
from dotenv import load_dotenv

# Load Environment
# Try loading from PyNexus .env first for Service Key
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PyNexus", ".env")
load_dotenv(env_path)
# Fallback to local .env
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

if not url or not key:
    print("❌ Critical: Missing SUPABASE_SERVICE_KEY in environment.")
    print("   Please ensure PyNexus/.env has the Service Key.")
    sys.exit(1)

client = create_client(url, key)

def generate_report():
    print("\n" + "="*60)
    print(f"PY DAILY EXERCISE REPORT - {os.getenv('COMPUTERNAME', 'Unknown PC')}")
    print("="*60)
    print(f"{'Day':<6} | {'Easy':<8} | {'Medium':<8} | {'Hard':<8} | {'Boss':<8} | {'Total':<8} | {'Status'}")
    print("-" * 75)

    try:
        # Fetch all exercises
        all_rows = []
        start = 0
        while True:
            res = client.table("exercises").select("day_number, difficulty").range(start, start+999).execute()
            if not res.data:
                break
            all_rows.extend(res.data)
            start += 1000

        # Process Data
        stats = {}
        for row in all_rows:
            day = row.get('day_number', 0)
            diff = row.get('difficulty', 'Unknown')
            if day not in stats:
                stats[day] = {"Easy": 0, "Medium": 0, "Hard": 0, "Scenario": 0, "Total": 0}
            
            if diff in stats[day]:
                stats[day][diff] += 1
            elif diff.lower() == 'boss': 
                stats[day]['Scenario'] += 1
            else: 
                pass 
            
            stats[day]['Total'] += 1

        # Print Table
        scan_range = sorted(list(set(stats.keys()) | {1, 2, 3}))
        
        for day in scan_range:
            d_stats = stats.get(day, {"Easy": 0, "Medium": 0, "Hard": 0, "Scenario": 0, "Total": 0})
            t = d_stats['Total']
            
            if t >= 35: status = "Healthy"
            elif t == 0: status = "Empty"
            else: status = "Partial"

            print(f"{day:<6} | {d_stats['Easy']:<8} | {d_stats['Medium']:<8} | {d_stats['Hard']:<8} | {d_stats['Scenario']:<8} | {t:<8} | {status}")

    except Exception as e:
        print(f"Reporting Failed: {e}")

    print("="*60 + "\n")

if __name__ == "__main__":
    generate_report()
