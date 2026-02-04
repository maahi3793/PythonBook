
"""
PythonBook CLI Entry Point
==========================
Run from command line or GitHub Actions to generate textbook content.

Usage:
    python run_textbook_bot.py --day 1 --part all
"""

import argparse
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.generator import TextbookGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    parser = argparse.ArgumentParser(description='PythonBook Content Generator')
    
    parser.add_argument('--day', type=str, help="Day number (1-179) or 'auto'")
    parser.add_argument('--part', type=str, default='all', 
        help="Content part to generate: part1, part2, part3, all, batch_easy, batch_medium, batch_hard, batch_scenario, batch_all"
    )
    parser.add_argument('--weekly', type=int, help='Generate weekly summary (Placeholder)')
    parser.add_argument('--final', action='store_true', help='Generate final chapter (Placeholder)')
    
    args = parser.parse_args()
    
    generator = TextbookGenerator()
    
    if args.weekly:
        logging.warning("Weekly summary logic not yet moved to generator")
    elif args.final:
        logging.warning("Final chapter logic not yet moved to generator")
    elif args.day:
        target_day = 0
        
        # LOGIC: Auto-detect next day
        if args.day == 'auto':
            logging.info("🤖 Auto-Detecting Day...")
            try:
                # Use generator's DB
                res = generator.db.client.table("textbook_chapters") \
                    .select("day, content_part1_theory") \
                    .order("day", desc=False) \
                    .execute()
                
                rows = res.data
                existing_days = {r['day']: r for r in rows}
                
                # Logic: Find the first day that is EITHER missing OR incomplete
                found_target = None
                max_checked_day = 0
                
                if not rows:
                     found_target = 1
                else:
                    max_day_in_db = rows[-1]['day']
                    for d in range(1, max_day_in_db + 2): 
                        if d not in existing_days:
                            found_target = d
                            logging.info(f"🔍 Gap detected at Day {d}. Filling gap.")
                            break
                        # We skip completeness check for 'auto' simpler logic for now
                        # or we keep it. Use simple "Next Day" logic
                        
                if found_target:
                    target_day = found_target
                else:
                    target_day = 1 
                
                logging.info(f"👉 Auto-Detected Target Day: {target_day}")
            except Exception as e:
                logging.error(f"❌ Auto-detection failed: {e}")
                sys.exit(1)
        else:
            try:
                target_day = int(args.day)
            except ValueError:
                logging.error(f"Invalid day: {args.day}")
                sys.exit(1)
        
        # ROUTING LOGIC
        if args.part.startswith('batch_'):
            # It is a Q35 batch
            from backend.curriculum import TOPICS
            topic = TOPICS.get(target_day, f"Day {target_day}")
            
            batch_map = {
                'batch_easy': 'Easy',
                'batch_medium': 'Medium',
                'batch_hard': 'Hard',
                'batch_scenario': 'Scenario',
                'batch_all': None
            }
            target_batch = batch_map.get(args.part)
            
            logging.info(f"🚀 Triggering Q35: Day {target_day}, Topic: {topic}, Batch: {target_batch}")
            result = generator.generate_daily_q35(target_day, topic, target_batch)
            
        else:
            # Standard Textbook Parts
            result = generator.generate_day(target_day, args.part)

        if result['success']:
            logging.info(f"✅ Success: {result['message']}")
        else:
            logging.error(f"❌ Failed: {result['message']}")
            sys.exit(1)
    else:
        logging.error("Please specify --day")

if __name__ == "__main__":
    main()
