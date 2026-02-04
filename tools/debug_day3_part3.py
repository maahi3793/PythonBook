import sys
import os
import logging

# Setup Logging to console
logging.basicConfig(level=logging.INFO)

# Add Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.generator import TextbookGenerator

def test_gen():
    print("Initializing Generator...")
    gen = TextbookGenerator()
    
    day = 3
    part = 'part3'
    
    print(f"Generating Day {day} Part {part}...")
    try:
        res = gen.generate_day(day, part)
        print(f"Result: {res}")
    except Exception as e:
        print(f"CRASH: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gen()
