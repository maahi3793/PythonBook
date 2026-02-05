import sys
import os
import json
from supabase import create_client
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

def audit_full_table():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    client = create_client(url, key)
    
    # Fetch ALL rows (limit to 1000 to be safe, user said 147)
    res = client.table("exercises").select("*").execute()
    
    rows = res.data
    total = len(rows)
    
    with open("audit_report.txt", "w", encoding="utf-8") as f:
        f.write(f"📉 Starting Deep Audit of {total} rows...\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'ID':<38} | {'Day':<3} | {'Source':<10} | {'Status'}\n")
        f.write("-" * 60 + "\n")
        
        missing_starter = 0
        missing_solution = 0
        missing_test = 0
        legacy_empty = 0
        q35_empty = 0
        
        for r in rows:
            issues = []
            if not r.get('starter_code'): issues.append("No Starter")
            if not r.get('solution_code'): issues.append("No Solution")
            if not r.get('test_code'): issues.append("No Test")
            
            status = "✅ OK" if not issues else f"❌ {', '.join(issues)}"
            source = r.get('source', 'unknown')[:10]
            
            # Track specific stats
            if issues:
                if 'starter_code' in issues: missing_starter += 1
                if 'solution_code' in issues: missing_solution += 1
                if 'test_code' in issues: missing_test += 1
                
                # Check real Q35 (source=textbook, filename starts with day)
                # Legacy might also be 'textbook' but usually has null source or different ID format
                # Let's count properly
                if source == 'textbook':
                    q35_empty += 1
                else:
                    legacy_empty += 1
            
            # Write row
            f.write(f"{r['id']:<38} | {r.get('day_number', '?'):<3} | {source:<10} | {status}\n")

        f.write("-" * 60 + "\n")
        f.write("📊 SUMMARY\n")
        f.write(f"Total Rows: {total}\n")
        f.write(f"Rows with Issues: {legacy_empty + q35_empty}\n")
        f.write(f"  - Legacy/Unknown Source: {legacy_empty}\n")
        f.write(f"  - Textbook (Q35) Source: {q35_empty}\n")
        f.write(f"Total Missing Starter: {missing_starter}\n")
        f.write(f"Total Missing Solution: {missing_solution}\n")
        f.write("-" * 60 + "\n")
        
    print("Audit written to audit_report.txt")

if __name__ == "__main__":
    audit_full_table()
