
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
        valid_parts = ['part1_theory', 'part2_practice', 'part3_mentor']
        if part not in valid_parts:
            logging.error(f"Invalid part name: {part}")
            return False
            
        try:
            # 1. Ensure record exists
            self.get_or_create_chapter(day)
            
            # 2. Update
            update_data = {
                part: content,
                "status": f"{part.split('_')[0]}_done" # e.g. part1_done
            }
            
            # Special logic: If all parts present, mark complete?
            # For now, just track the latest part done
            
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
            pass # Don't crash on logging failure
