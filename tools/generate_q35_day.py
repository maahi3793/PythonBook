import sys
import os
import argparse
import logging

# Add logic path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.generator import TextbookGenerator
from backend.curriculum import TOPICS

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Generate 35 Exercises (Q35) for a specific day.")
    parser.add_argument("day", type=int, help="Day number to generate (e.g. 5)")
    args = parser.parse_args()
    
    day = args.day
    topic = TOPICS.get(day, f"Day {day}")
    
    print(f"--- Starting Q35 Generation for Day {day}: {topic} ---")
    
    gen = TextbookGenerator()
    res = gen.generate_daily_q35(day, topic)
    
    if res['success']:
        print("✅ SUCCESS!")
        print(res['message'])
    else:
        print("❌ FAILED!")
        print(res['message'])

if __name__ == "__main__":
    main()
