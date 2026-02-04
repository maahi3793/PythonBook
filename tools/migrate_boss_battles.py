import os
import sys
from typing import List, Dict
import logging

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def migrate_boss_battles():
    """
    Reads from 'boss_battles' table.
    Writes to 'exercises' table.
    """
    db = TextbookDB()
    client = db.client
    
    logger.info("--- Starting Boss Battle Migration ---")
    
    # 1. Fetch all battles
    try:
        res = client.table("boss_battles").select("*").execute()
        battles = res.data
        if not battles:
            logger.info("No battles found to migrate.")
            return
            
        logger.info(f"Found {len(battles)} battles.")
        
    except Exception as e:
        logger.error(f"Failed to fetch battles: {e}")
        return

    # 2. Transform and Insert
    count = 0
    skipped = 0
    
    for b in battles:
        day = b.get('day')
        title = b.get('title')
        topic = b.get('topic', 'Unknown Topic') # Fallback if missing
        
        # Combine Scenario + Requirements + Hints for description
        scenario = b.get('scenario', '')
        requirements = "\n".join([f"- {r}" for r in b.get('requirements', [])])
        hints = "\n".join([f"> Hint: {h}" for h in b.get('hints', [])])
        
        description = f"""
## Scenario
{scenario}

## Requirements
{requirements}

## Hints
{hints}
        """
        
        try:
            # Explicit check
            # logger.info(f"Checking existence of Day {day} - {title}")
            # check = client.table("exercises").select("id").eq("day_number", day).eq("title", title).execute()
            # if check.data:
            #    skipped += 1
            #    logger.info(f"Skipping duplicate: {title}")
            #    continue
            pass
        except Exception as e:
            logger.warning(f"Check failed: {e}")

        payload = {
            "day_number": day,
            "filename": f"boss_day_{day}.py", 
            "title": title,
            "description": description.strip(),
            "source": "boss_battle",
            "difficulty": "Hard",
            # "topic": topic, # COMMENTED OUT TO TEST IF COLUMN IS MISSING
            "xp_reward": 100
        }
        
        # Add topic safely if column exists (we can't check easily without triggering error)
        # Let's try inserting WITHOUT topic first to see if that works.
        # If the user says table is empty, likely NO rows got in.
        
        # RE-ENABLE TOPIC BUT PRINT ERROR
        payload['topic'] = topic

        try:
            client.table("exercises").insert(payload).execute()
            count += 1
            logger.info(f"✅ Migrated Day {day}: {title}")
        except Exception as e:
            logger.error(f"❌ Failed Day {day}: {e}")
            # RAISE to see full trace
            # raise e 
            pass # Keep it running to see other errors? No, lets see one.
            print(f"CRITICAL ERROR: {e}") 


    logger.info(f"--- Migration Complete ---")
    logger.info(f"Inserted: {count}")
    logger.info(f"Skipped: {skipped}")

if __name__ == "__main__":
    migrate_boss_battles()
