
import os
import logging
from supabase import create_client, Client
from dotenv import load_dotenv

# Load params from .env or environment
load_dotenv()

class TextbookDB:
    """
    Database Manager for PythonBook.
    Handles all interactions with Supabase tables.
    """
    
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            logging.error("❌ Missing Supabase credentials. check .env")
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY are required.")
            
        self.client: Client = create_client(url, key)

    # ==========================================================
    # 📖 READ FROM PYDAILY
    # ==========================================================
    
    def get_pydaily_lesson(self, day: int):
        """Fetch lesson content for a specific day."""
        try:
            # Table: daily_content
            # Columns: day, content, topic
            response = self.client.table("daily_content") \
                .select("*") \
                .eq("day", day) \
                .execute()
                
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error fetching lesson for day {day}: {e}")
            return None

    def get_pydaily_quiz(self, day: int):
        """Fetch quiz questions for a specific day."""
        try:
            # Table: quiz_questions
            # Columns: day, questions (json)
            response = self.client.table("quiz_questions") \
                .select("*") \
                .eq("day", day) \
                .execute()
                
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error fetching quiz for day {day}: {e}")
            return None

    def get_pydaily_boss_battle(self, day: int):
        """
        Fetch boss battle. Boss battles are range-based (e.g., Days 1-5).
        So we need to find one where day is within START_DAY and END_DAY.
        Or simplified: PyDaily might store them by specific day if generated daily.
        Assuming 'boss_battles' has a 'day' column if generated daily, 
        OR we query based on the current day matching a boss schedule.
        
        For now, let's try querying by specific 'day' content.
        """
        try:
            # Table: boss_battles
            # Columns: day, content/challenge
            response = self.client.table("boss_battles") \
                .select("*") \
                .eq("day", day) \
                .execute()
                
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logging.error(f"Error fetching boss battle for day {day}: {e}")
            return None

    def get_pydaily_nuggets(self, day: int):
        """Fetch nuggets (feed items) for a specific day to use as Pro Tips."""
        try:
            # Table: feed
            # Columns: day, content, type
            response = self.client.table("feed") \
                .select("*") \
                .eq("day", day) \
                .execute()
            
            # Return all items for that day
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching nuggets for day {day}: {e}")
            return []

    # ==========================================================
    # ✍️ WRITE TO TEXTBOOK
    # ==========================================================

    def get_or_create_chapter(self, day: int):
        """Get existing chapter record or create a placeholder."""
        try:
            # Check if exists
            response = self.client.table("textbook_chapters") \
                .select("*") \
                .eq("day", day) \
                .execute()
                
            if response.data:
                return response.data[0]
            
            # Create new
            new_chapter = {
                "day": day,
                "title": f"Day {day} Content",  # Will be updated by AI later
                "status": "pending"
            }
            res = self.client.table("textbook_chapters").insert(new_chapter).execute()
            return res.data[0] if res.data else None
            
        except Exception as e:
            logging.error(f"Error getting/creating chapter for day {day}: {e}")
            return None

    def update_chapter_part(self, day: int, part: str, content: str):
        """
        Update a specific part of the chapter content.
        part: 'part1_theory', 'part2_practice', 'part3_mentor'
        """
        valid_parts = ['content_part1_theory', 'content_part2_practice', 'content_part3_mentor']
        if part not in valid_parts:
            # Allow legacy/short names too?
            # If passed 'part1_theory', map to 'content_part1_theory'?
            # No, generator sends full name. Stick to whitelist.
            logging.error(f"Invalid part name: {part}")
            return False
            
        try:
            # 1. Ensure record exists
            self.get_or_create_chapter(day)
            
            # 2. Update
            # Derive status: content_part1_theory -> part1_done
            # split('_') -> ['content', 'part1', 'theory'] -> index 1 is part1
            status_prefix = part.split('_')[1] 
            
            update_data = {
                part: content,
                "status": f"{status_prefix}_done" 
            }
            
            self.client.table("textbook_chapters") \
                .update(update_data) \
                .eq("day", day) \
                .execute()
                
            logging.info(f"✅ Updated Day {day} {part}")
            return True
            
        except Exception as e:
            logging.error(f"Error updating chapter day {day}: {e}")
            return False

    def save_image_placeholders(self, day: int, placeholders: list):
        """
        Save extracted image placeholders.
        placeholders: list of dicts {id, description, suggested_urls}
        """
        if not placeholders:
            return
            
        try:
            # Upsert each placeholder
            for p in placeholders:
                data = {
                    "id": p['id'],
                    "chapter_day": day,
                    "description": p['description'],
                    "suggested_urls": p.get('suggested_urls', []),
                    "status": "pending"
                }
                
                self.client.table("textbook_images") \
                    .upsert(data, on_conflict="id") \
                    .execute()
                    
            logging.info(f"🖼️ Saved {len(placeholders)} images for Day {day}")
            
        except Exception as e:
            logging.error(f"Error saving images for day {day}: {e}")

    def is_quiz_day(self, day: int) -> bool:
        """Check if the day is a dedicated Quiz day (e.g. Topic contains 'Quiz')."""
        try:
            lesson = self.get_pydaily_lesson(day)
            if lesson:
                topic = lesson.get('topic', '')
                # Heuristic: If topic explicitly mentions "Quiz" and not just "Quiz App" (like a project)
                # Ideally, we want to skip "Day X: Quiz". 
                # Be careful not to skip "Project: Quiz App". 
                # Let's assume strict "Quiz" word or maybe user has a flag. 
                # For now, simple check: "Quiz" in topic? 
                # Or check if content is empty but quiz exists?
                # User said "days for quizes".
                if "Quiz" in topic and "Project" not in topic: 
                    return True
            return False
            return False
        except Exception:
            return False

    def get_non_quiz_days(self) -> list[int]:
        """
        Fetch all days that are valid for the textbook (excluding Quiz days).
        Returns a sorted list of day numbers.
        """
        try:
            # Fetch all topics to filter locally (faster than 179 queries)
            # Or assume we want days 1-179 and filter.
            response = self.client.table("daily_content").select("day, topic").execute()
            
            valid_days = []
            if response.data:
                for row in response.data:
                    day = row['day']
                    topic = row.get('topic', '')
                    
                    # Same logic as is_quiz_day
                    if "Quiz" in topic and "Project" not in topic:
                        continue # Skip
                    
                    # Also ensure it's within range 1-179 just in case
                    if 1 <= day <= 179:
                        valid_days.append(day)
            
            # Use set to ensure uniqueness if DB has dupes, then sort
            return sorted(list(set(valid_days)))
            
        except Exception as e:
            logging.error(f"Error fetching non-quiz days: {e}")
            # Fallback to all days if query fails
            return list(range(1, 180))

    def log_generation(self, day: int, part: str, status: str, error: str = None):
        """Log the result of a generation run."""
        try:
            self.client.table("textbook_generation_log").insert({
                "day": day,
                "part": part,
                "status": status,
                "error_message": error
            }).execute()
        except Exception:
            pass
            
    def get_all_chapters_metadata(self):
        """Fetch metadata for all chapters (day, title, status) for sidebar."""
        try:
            response = self.client.table("textbook_chapters") \
                .select("day, title, status, part1_at, part2_at, part3_at") \
                .order("day") \
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching chapter metadata: {e}")
            return []

    def get_pending_images(self):
        """Fetch all images that need review/upload."""
        try:
            response = self.client.table("textbook_images") \
                .select("*") \
                .neq("status", "uploaded") \
                .order("chapter_day") \
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching pending images: {e}")
            return []
            
    def update_image_url(self, image_id: str, public_url: str):
        """Update an image with its hosted URL."""
        try:
            self.client.table("textbook_images") \
                .update({
                    "selected_url": public_url,
                    "status": "uploaded"
                }) \
                .eq("id", image_id) \
                .execute()
            return True
        except Exception as e:
            logging.error(f"Error updating image URL: {e}")
            return False
