import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

CONTENT = """# Quiz Day (Review) - Part 3: The Interview

### Interview Q1: Interpretation vs. Compilation
**Context:** Day 1 (Hello World)
**Question:** Python is an interpreted language. What happens when you run `python script.py`? Does it compile anything?
**Model Answer:** Yes, it compiles to Bytecode (`.pyc`). The Python Interpreter (CPython) then executes this bytecode. It is not compiled to Machine Code like C++. This allows Python to be cross-platform but generally slower than compiled languages.

### Interview Q2: Variable Assignment
**Context:** Day 2 (Variables)
**Question:** In Python, if you do `a = 10` and `b = 10`, do `a` and `b` point to the same memory address?
**Model Answer:** Typically, yes. Python caches small integers (usually -5 to 256) as singleton objects for performance. So `id(a)` will equal `id(b)`. For larger numbers or other types, this might not be true. This demonstrates that Python variables are *references* (indexes) to objects, not fixed memory buckets.

### Interview Q3: Dynamic Typing
**Context:** Day 2 (Variables)
**Question:** Python is dynamically typed. What is the downside of this?
**Model Answer:** Type errors (like adding a string to an integer) are only caught at *runtime*, meaning the program might crash while running. In statically typed languages (like Java), these referrors are caught during compilation before the program ever runs.
"""

def manual_insert():
    db = TextbookDB()
    print("--- MANUAL INSERT DAY 3 PART 3 ---")
    db.update_chapter_part(3, 'content_part3_mentor', CONTENT)
    db.log_generation(3, 'part3', 'manual_override')
    print("Day 3 Part 3 Updated.")
    
if __name__ == "__main__":
    manual_insert()
