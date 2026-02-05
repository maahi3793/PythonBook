import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.generator import TextbookGenerator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backfill_day_robust(day):
    generator = TextbookGenerator()
    
    # 4 Batches
    batches = [
        ("Easy", 10),
        ("Medium", 10),
        ("Hard", 10),
        ("Scenario", 5)
    ]
    
    logging.info(f"🛡️ Starting ROBUST Backfill for Day {day}")
    
    for diff, required_count in batches:
        # 1. Check if already done
        try:
            res = generator.db.client.table("exercises") \
                .select("id", count="exact") \
                .eq("day_number", day) \
                .eq("difficulty", diff) \
                .execute()
            
            existing_count = res.count
            logging.info(f"   📊 Day {day} {diff}: Found {existing_count}/{required_count}")
            
            if existing_count >= required_count:
                logging.info(f"   ✅ Batch {diff} already complete. Skipping.")
                continue
                
        except Exception as e:
            logging.error(f"   ❌ DB Check Failed: {e}")
            sys.exit(1)

        # 2. Needs Generation
        retry_count = 0
        max_retries = 1
        
        while retry_count <= max_retries:
            try:
                logging.info(f"   🚀 Generating {diff} (Attempt {retry_count+1})...")
                
                # We interpret "generate slowly" as "Batch by Batch" with waits.
                # We use the existing logic which does 1 API call per batch.
                
                # Fetch Topic
                from backend.curriculum import TOPICS
                topic = TOPICS.get(day, f"Day {day}")
                
                result = generator.generate_daily_q35(day, topic, target_batch=diff)
                
                if result['success']:
                    logging.info(f"   ✅ Batch {diff} Generated. Verifying Data...")
                    
                    # VERIFICATION STEP
                    # Check if actual code content was saved
                    verify = generator.db.client.table("exercises") \
                        .select("*") \
                        .eq("day_number", day) \
                        .eq("difficulty", diff) \
                        .execute()
                        
                    valid_rows = 0
                    for v in verify.data:
                        if v.get('starter_code') and len(v.get('starter_code')) > 10:
                            valid_rows += 1
                            
                    if valid_rows < count:
                        logging.error(f"   ❌ VERIFICATION FAILED: Found {valid_rows}/{count} valid rows.")
                        raise Exception("Generated rows but content was empty/missing.")
                    
                    logging.info(f"   🛡️ Verified {valid_rows}/{count} rows have content.")
                    
                    # Robust Wait
                    logging.info("   ⏳ Waiting 30s before next batch...")
                    time.sleep(30) 
                    break
                else:
                    raise Exception(result['message'])
                    
            except Exception as e:
                logging.error(f"   ⚠️ Batch {diff} Failed: {e}")
                
                if "quota" in str(e).lower() or "429" in str(e):
                    logging.warning("   🛑 Quota Hit! Waiting 60 seconds...")
                    time.sleep(60)
                else:
                    logging.warning("   ⚠️ Error occurred. Waiting 10 seconds...")
                    time.sleep(10)
                
                retry_count += 1
                
                if retry_count > max_retries:
                    logging.critical(f"   ❌ CRITICAL: Failed {diff} after retries. Terminating.")
                    logging.critical("   Please run the script again later to resume.")
                    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default: Run Days 1, 2, 3
        days_to_run = [1, 2, 3]
    else:
        days_to_run = [int(sys.argv[1])]
    
    for d in days_to_run:
        backfill_day_robust(d)
        time.sleep(5) # Buffer between days
