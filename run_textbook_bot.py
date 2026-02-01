
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
    parser.add_argument('--part', type=str, choices=['part1', 'part2', 'part3', 'all'], default='all')
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
                    .select("day") \
                    .order("day", desc=True) \
                    .limit(1) \
                    .execute()
                
                if res.data:
                    last_day = res.data[0]['day']
                    target_day = last_day + 1
                else:
                    target_day = 1 # Start fresh
                logging.info(f"👉 Auto-Detected Next Day: {target_day}")
            except Exception as e:
                logging.error(f"❌ Auto-detection failed: {e}")
                sys.exit(1)
        else:
            try:
                target_day = int(args.day)
            except ValueError:
                logging.error(f"Invalid day: {args.day}")
                sys.exit(1)
        
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
