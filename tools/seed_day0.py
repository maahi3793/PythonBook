
import os
import sys

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB

def seed_day0():
    print("🌱 Seeding Day 0: Preface...")
    db = TextbookDB()
    
    # Content for the Preface
    preface_content = """
# Welcome to PyTextbook 🐍

Welcome to **PyTextbook**, your daily companion for mastering Python. This isn't just a collection of tutorials; it's a structured journey designed to take you from a complete beginner to a confident Python developer in 180 days.

## 🌟 Our Philosophy

We believe that learning to code is like learning a language or an instrument: consistency beats intensity.
*   **Daily Practice:** Small, manageable chunks every day.
*   **Hands-on First:** You won't just read code; you'll write it.
*   **Mentor-Guided:** Every chapter includes insights from a virtual mentor to explain the "why," not just the "how."

## 📚 Structure of the Book

Each "Day" in this book follows a proven three-part structure:

### 1. 📘 Part 1: Theory
We start with the core concepts. What are we learning today? Why does it matter? We use clear analogies and simple examples to build your mental model.

### 2. 🧪 Part 2: Practice
Philosophy is nothing without action. This section provides code snippets, small exercises, and "Try It Yourself" challenges to build your muscle memory.

### 3. 🎓 Part 3: Mentor
Finally, we sit down with a senior developer's perspective. We discuss common pitfalls, best practices, and how to think like a programmer.

## 🗺️ The Roadmap (Syllabus)

This journey is divided into major phases:

*   **Days 1-15:** **The Basics** (Variables, Loops, Logic)
*   **Days 16-30:** **Data Structures** (Lists, Dicts, Sets)
*   **Days 31-50:** **Functions & Modular Code**
*   **Days 51-80:** **Object-Oriented Programming (OOP)**
*   **Days 81-120:** **Web Development & APIs**
*   **Days 121-150:** **Data Science & AI Basics**
*   **Days 151-180:** **Final Capstone Projects**

## 🚀 How to Use This Book

1.  **Start at Day 1.** Don't skip ahead unless you are reviewing.
2.  **Code Along.** Don't just read. Type the code. Break it. Fix it.
3.  **Use the "Practice" Tab.** The only way to learn is to do.
4.  **Stay Consistent.** 30 minutes a day is better than 5 hours on Sunday.

Ready to begin? Select **Day 1** from the menu (Top Right) to start your journey!
"""

    # Data Payload
    day0_data = {
        "day": 0,
        "title": "Preface: Welcome to Python",
        "content_part1_theory": preface_content,
        "content_part2_practice": "*(Review the Theory tab for the Introduction)*", 
        "content_part3_mentor": "*(Review the Theory tab for the Introduction)*",
        "status": "complete"
    }

    try:
        # Upsert into DB
        res = db.client.table("textbook_chapters").upsert(day0_data, on_conflict="day").execute()
        print("✅ Day 0 Seeded Successfully!")
        print(f"Response: {res}")
    except Exception as e:
        print(f"❌ Error seeding Day 0: {e}")

if __name__ == "__main__":
    seed_day0()
