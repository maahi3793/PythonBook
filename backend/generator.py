
import logging
from backend.db_textbook import TextbookDB
from backend.gemini_textbook import GeminiTextbook
from backend.image_extractor import ImageExtractor

class TextbookGenerator:
    """
    Core content generation engine.
    Callable from CLI or Web UI.
    """
    
    def __init__(self):
        self.db = TextbookDB()
        self.gemini = GeminiTextbook()
        self.extractor = ImageExtractor()

    def generate_day(self, day: int, part: str) -> dict:
        """
        Generate content for a specific day and part.
        part: 'part1', 'part2', 'part3', 'all'
        Returns: {'success': bool, 'message': str}
        """
        results = []
        
        # Check for Quiz Day and Skip
        if self.db.is_quiz_day(day):
            msg = f"🚫 Day {day} is a designated QUIZ DAY. Skipping."
            logging.warning(msg)
            self.db.log_generation(day, part, 'skipped', 'Quiz Day')
            return {'success': False, 'message': msg}

        # ==========================
        # PART 1: THEORY
        # ==========================
        if part in ['all', 'part1']:
            try:
                logging.info(f"📘 Generating Day {day} Part 1...")
                lesson = self.db.get_pydaily_lesson(day)
                if not lesson:
                    lesson_content = "Topic data not available."
                    topic = f"Python Topic Day {day}"
                else:
                    lesson_content = lesson.get('content', '')
                    topic = lesson.get('topic', f"Day {day}")
                
                content = self.gemini.generate_part1_theory(day, topic, lesson_content)
                self.db.update_chapter_part(day, 'content_part1_theory', content)
                
                images = self.extractor.extract_placeholders(content)
                self.db.save_image_placeholders(day, images)
                
                self.db.log_generation(day, 'part1', 'completed')
                results.append("Part 1 ✅")
            except Exception as e:
                logging.error(f"Part 1 Failed: {e}")
                self.db.log_generation(day, 'part1', 'failed', str(e))
                results.append(f"Part 1 ❌ ({e})")

        # ==========================
        # PART 2: PRACTICE
        # ==========================
        if part in ['all', 'part2']:
            try:
                logging.info(f"🧪 Generating Day {day} Part 2...")
                # Re-fetch topic if needed (could optimize)
                lesson = self.db.get_pydaily_lesson(day)
                topic = lesson.get('topic', f"Day {day}") if lesson else f"Day {day}"

                quiz = self.db.get_pydaily_quiz(day)
                boss = self.db.get_pydaily_boss_battle(day)
                
                content = self.gemini.generate_part2_practice(day, topic, quiz, boss)
                self.db.update_chapter_part(day, 'content_part2_practice', content)
                
                images = self.extractor.extract_placeholders(content)
                self.db.save_image_placeholders(day, images)
                
                self.db.log_generation(day, 'part2', 'completed')
                results.append("Part 2 ✅")
            except Exception as e:
                logging.error(f"Part 2 Failed: {e}")
                self.db.log_generation(day, 'part2', 'failed', str(e))
                results.append(f"Part 2 ❌ ({e})")

        # ==========================
        # PART 3: MENTOR
        # ==========================
        if part in ['all', 'part3']:
            try:
                logging.info(f"🎓 Generating Day {day} Part 3...")
                lesson = self.db.get_pydaily_lesson(day)
                topic = lesson.get('topic', f"Day {day}") if lesson else f"Day {day}"

                nuggets = self.db.get_pydaily_nuggets(day)
                
                content = self.gemini.generate_part3_mentor(day, topic, nuggets)
                self.db.update_chapter_part(day, 'content_part3_mentor', content)
                
                self.db.log_generation(day, 'part3', 'completed')
                results.append("Part 3 ✅")
            except Exception as e:
                logging.error(f"Part 3 Failed: {e}")
                self.db.log_generation(day, 'part3', 'failed', str(e))
                results.append(f"Part 3 ❌ ({e})")

        success = not any('❌' in r for r in results)
        return {'success': success, 'message': ", ".join(results)}
