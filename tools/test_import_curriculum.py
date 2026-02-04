import sys
import os

# Add PyDailyEmail to path (assuming we are in PythonBook)
current = os.path.dirname(os.path.abspath(__file__)) # tools/
root = os.path.dirname(current) # PythonBook
sister = os.path.join(os.path.dirname(root), "PyDailyEmail")

sys.path.append(sister)

try:
    from backend.curriculum import TOPICS
    print(f"Success! Day 1 Topic: {TOPICS.get(1)}")
except ImportError as e:
    print(f"Failed to import: {e}")
except Exception as e:
    print(f"Other error: {e}")
