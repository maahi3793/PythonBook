
"""
PythonBook CLI Entry Point
==========================
Run from command line or GitHub Actions to generate textbook content.

Usage:
    python run_textbook_bot.py --day 1 --part all
    python run_textbook_bot.py --day 1 --part part1
    python run_textbook_bot.py --weekly 1
    python run_textbook_bot.py --final
"""

import argparse
import logging
import sys

# Add project root to path
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db_textbook import TextbookDB
from backend.gemini_textbook import GeminiTextbook
from backend.image_extractor import ImageExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_generation(day: int, part: str):
    """Main generation logic for day content."""
    db = TextbookDB()
    gemini = GeminiTextbook()
    extractor = ImageExtractor()
    
    logging.info(f"🚀 Starting generation for Day {day} - {part}")

    # ==========================
    # PART 1: THEORY
    # ==========================
    if part in ['all', 'part1']:
        logging.info("📘 Generating Part 1: Theory...")
        try:
            lesson = db.get_pydaily_lesson(day)
            if not lesson:
                logging.warning(f"⚠️ No lesson content found for Day {day}")
                lesson_content = "Topic data not available."
                topic = f"Python Topic Day {day}"
            else:
                lesson_content = lesson.get('content', '')
                topic = lesson.get('topic', f"Day {day}")
            
            # Generate
            content = gemini.generate_part1_theory(day, topic, lesson_content)
            
            # Save Content
            db.update_chapter_part(day, 'content_part1_theory', content)
            
            # Extract & Save Images
            images = extractor.extract_placeholders(content)
            db.save_image_placeholders(day, images)
            
            db.log_generation(day, 'part1', 'completed')
            logging.info("✅ Part 1 Complete")
            
        except Exception as e:
            logging.error(f"❌ Part 1 Failed: {e}")
            db.log_generation(day, 'part1', 'failed', str(e))

    # ==========================
    # PART 2: PRACTICE
    # ==========================
    if part in ['all', 'part2']:
        logging.info("🧪 Generating Part 2: Practice...")
        try:
            # Need topic again
            if not locals().get('topic'):
                lesson = db.get_pydaily_lesson(day)
                topic = lesson.get('topic', f"Day {day}") if lesson else f"Day {day}"

            quiz = db.get_pydaily_quiz(day)
            boss = db.get_pydaily_boss_battle(day)
            
            # Generate
            content = gemini.generate_part2_practice(day, topic, quiz, boss)
            
            # Save
            db.update_chapter_part(day, 'content_part2_practice', content)
            
            # Images? (Rare in practice but possible)
            images = extractor.extract_placeholders(content)
            db.save_image_placeholders(day, images)
            
            db.log_generation(day, 'part2', 'completed')
            logging.info("✅ Part 2 Complete")
            
        except Exception as e:
            logging.error(f"❌ Part 2 Failed: {e}")
            db.log_generation(day, 'part2', 'failed', str(e))

    # ==========================
    # PART 3: MENTOR
    # ==========================
    if part in ['all', 'part3']:
        logging.info("🎓 Generating Part 3: Mentor...")
        try:
            # Need topic again
            if not locals().get('topic'):
                lesson = db.get_pydaily_lesson(day)
                topic = lesson.get('topic', f"Day {day}") if lesson else f"Day {day}"

            nuggets = db.get_pydaily_nuggets(day)
            
            # Generate
            content = gemini.generate_part3_mentor(day, topic, nuggets)
            
            # Save
            db.update_chapter_part(day, 'content_part3_mentor', content)
            
            db.log_generation(day, 'part3', 'completed')
            logging.info("✅ Part 3 Complete")
            
        except Exception as e:
            logging.error(f"❌ Part 3 Failed: {e}")
            db.log_generation(day, 'part3', 'failed', str(e))


def run_weekly(week: int):
    """Generate weekly summary."""
    logging.info(f"📅 Generating Weekly Summary for Week {week}...")
    # TODO: Implement full weekly logic (fetching 7 days of topics)
    logging.warning("Weekly summary logic to be fully implemented")

def main():
    parser = argparse.ArgumentParser(description='PythonBook Content Generator')
    
    parser.add_argument('--day', type=int, help='Day number (1-179)')
    parser.add_argument('--part', type=str, choices=['part1', 'part2', 'part3', 'all'], default='all')
    parser.add_argument('--weekly', type=int, help='Generate weekly summary for week N')
    parser.add_argument('--final', action='store_true', help='Generate final chapter')
    
    args = parser.parse_args()
    
    if args.weekly:
        run_weekly(args.weekly)
    elif args.final:
        logging.info("🎓 Generating Final Chapter...")
        logging.warning("Final chapter logic not yet implemented")
    elif args.day:
        run_generation(args.day, args.part)
    elif args.day is None:
        # Auto-detect day logic could go here
        logging.error("Please specify --day or --weekly")

if __name__ == "__main__":
    main()
