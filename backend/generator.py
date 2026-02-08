
import logging
from backend.db_textbook import TextbookDB
from backend.gemini_textbook import GeminiTextbook
from backend.image_extractor import ImageExtractor
from PyDailyEmail.backend.curriculum import TOPICS # Single Source of Truth

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
        
        topic_from_curriculum = TOPICS.get(day, "")
        is_quiz_curriculum = "Quiz" in topic_from_curriculum
        
        # ==========================
        # 🚨 ASSESSMENT DAY ROUTING
        # ==========================
        if is_quiz_curriculum:
            # Instead of Skipping, we generate Assessment
            logging.info(f"🛡️ Day {day} is ASSESSMENT DAY. Generating Assessment Content...")
            return self._generate_assessment_day(day, part, topic_from_curriculum)

        # ==========================
        # PART 1: THEORY
        # ==========================
        if part in ['all', 'part1']:
            # Skip if already generated
            if self.db.has_part_content(day, 'part1'):
                logging.info(f"⏭️ Skipping Part 1 for Day {day} (already generated)")
                results.append("Part 1 ⏭️ (skipped)")
            else:
                try:
                    logging.info(f"📘 Generating Day {day} Part 1...")
                    lesson = self.db.get_pydaily_lesson(day)
                    if not lesson:
                        lesson_content = "Topic data not available."
                        # FALLBACK: Use Curriculum Topic
                        topic = TOPICS.get(day, f"Day {day}")
                        logging.info(f"ℹ️ DB Lesson Missing. Fallback to Curriculum Topic: {topic}")
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
            # Skip if already generated
            if self.db.has_part_content(day, 'part2'):
                logging.info(f"⏭️ Skipping Part 2 for Day {day} (already generated)")
                results.append("Part 2 ⏭️ (skipped)")
            else:
                try:
                    logging.info(f"🧪 Generating Day {day} Part 2...")
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
            # Skip if already generated
            if self.db.has_part_content(day, 'part3'):
                logging.info(f"⏭️ Skipping Part 3 for Day {day} (already generated)")
                results.append("Part 3 ⏭️ (skipped)")
            else:
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

    def _generate_assessment_day(self, day: int, part: str, topic: str):
        """Helper to generate Assessment Content (3 Parts)."""
        results = []
        
        # Build Context (Previous 2 Days)
        # e.g. Day 3 -> Context: Day 1, Day 2
        context_days = [d for d in range(day - 2, day) if d > 0]
        context_lines = []
        for d in context_days:
            t = TOPICS.get(d, "Unknown Concept")
            context_lines.append(f"Day {d}: {t}")
        
        context_str = "\n".join(context_lines) if context_lines else "General Python Basics"
        logging.info(f"🧠 Assessment Context for Day {day}:\n{context_str}")
        
        # PART 1: Warmup
        if part in ['all', 'part1']:
            try:
                logging.info(f"🛡️ Generating Day {day} Assessment Part 1 (Warmup)...")
                content = self.gemini.generate_assessment_part1(day, topic, context_str)
                self.db.update_chapter_part(day, 'content_part1_theory', content)
                self.db.log_generation(day, 'part1', 'completed')
                results.append("Assessment P1 ✅")
            except Exception as e:
                logging.error(f"Assessment P1 Failed: {e}")
                results.append(f"Assessment P1 ❌")

        # PART 2: Gauntlet
        if part in ['all', 'part2']:
            try:
                logging.info(f"🛡️ Generating Day {day} Assessment Part 2 (Gauntlet)...")
                content = self.gemini.generate_assessment_part2(day, topic, context_str)
                self.db.update_chapter_part(day, 'content_part2_practice', content)
                self.db.log_generation(day, 'part2', 'completed')
                results.append("Assessment P2 ✅")
            except Exception as e:
                logging.error(f"Assessment P2 Failed: {e}")
                results.append(f"Assessment P2 ❌")

        # PART 3: Interview
        if part in ['all', 'part3']:
            try:
                logging.info(f"🛡️ Generating Day {day} Assessment Part 3 (Interview)...")
                content = self.gemini.generate_assessment_part3(day, topic, context_str)
                self.db.update_chapter_part(day, 'content_part3_mentor', content)
                self.db.log_generation(day, 'part3', 'completed')
                results.append("Assessment P3 ✅")
            except Exception as e:
                logging.error(f"Assessment P3 Failed: {e}")
                results.append(f"Assessment P3 ❌")

        success = not any('❌' in r for r in results)
        return {'success': success, 'message': ", ".join(results)}

    def generate_daily_q35(self, day: int, topic: str, target_batch: str = None) -> dict:
        """
        Generate 35 Exercises (or a specific batch):
        - 10 Easy (10xp)
        - 10 Medium (20xp)
        - 10 Hard (50xp)
        - 5 Scenario (100xp)
        
        target_batch: 'Easy', 'Medium', 'Hard', 'Scenario', or None (All)
        """
        import json
        import time 
        results = []
        all_batches = [
            ("Easy", 10, 10),
            ("Medium", 10, 20),
            ("Hard", 10, 50),
            ("Scenario", 5, 100)
        ]
        
        # Filter if target_batch is set
        if target_batch:
            # Case-insensitive match
            batches = [b for b in all_batches if b[0].lower() == target_batch.lower()]
            if not batches:
                return {'success': False, 'message': f"Invalid batch type: {target_batch}"}
            logging.info(f"🚀 Starting Q35 Generation for Day {day}: {topic} (Batch: {target_batch})")
        else:
            batches = all_batches
            logging.info(f"🚀 Starting Q35 Generation for Day {day}: {topic} (All Batches)")
        
        for diff, count, xp in batches:
            # Skip if exercises already exist for this day+difficulty
            if self.db.has_exercises(day, diff):
                logging.info(f"   ⏭️ Skipping {diff} batch (already exists)")
                results.append(f"{diff} ⏭️ (skipped)")
                continue
                
            try:
                logging.info(f"   Generating Batch: {count} {diff}...")
                json_str = self.gemini.generate_exercise_batch(topic, diff, count, xp)
                
                # Clean JSON (Gemini sometimes adds ```json ... ```)
                clean_json_str = json_str.strip()
                if clean_json_str.startswith("```json"):
                    clean_json_str = clean_json_str[7:]
                if clean_json_str.endswith("```"):
                    clean_json_str = clean_json_str[:-3]
                
                exercises = json.loads(clean_json_str)
                
                # Check formatting
                if not isinstance(exercises, list):
                    raise ValueError("Output is not a list")
                
                # Save to DB
                saved_count = 0
                for ex in exercises:
                    # Enrich with metadata
                    ex['day_number'] = day
                    ex['source'] = 'textbook'
                    ex['topic'] = topic
                    ex['difficulty'] = diff
                    ex['xp_reward'] = xp
                    # Ensure minimal fields (fallback)
                    if 'starter_code' not in ex: ex['starter_code'] = '# Write code here'
                    if 'test_code' not in ex: ex['test_code'] = '# No test provided'

                    try:
                        slug = ex['title'].lower().replace(" ", "_")
                        slug = "".join(c for c in slug if c.isalnum() or c == "_")
                        ex['filename'] = f"day{day}_{slug}.py"
                        
                        self.db.client.table("exercises").insert(ex).execute()
                        saved_count += 1
                    except Exception as db_e:
                        logging.error(f"Failed to save exercise {ex.get('title')}: {db_e}")
                
                results.append(f"{diff}: {saved_count}/{count} ✅")
                
                # Only sleep if running multiple batches (i.e., target_batch is None)
                if not target_batch:
                    time.sleep(10)
                
            except Exception as e:
                logging.error(f"Batch {diff} Failed: {e}")
                results.append(f"{diff} ❌")
        
        return {'success': True, 'message': ", ".join(results)}
