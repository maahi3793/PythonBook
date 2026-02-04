import os
import sys
import re
import logging

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db_textbook import TextbookDB
from backend.curriculum import TOPICS

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_exercises():
    """
    Reads from 'textbook_chapters'.
    Parses Markdown.
    Writes to 'exercises'.
    """
    db = TextbookDB()
    client = db.client
    
    logger.info("--- Starting Textbook Parsing ---")
    
    # 1. Fetch all chapters
    try:
        res = client.table("textbook_chapters").select("*").execute()
        chapters = res.data
    except Exception as e:
        logger.error(f"Failed to fetch chapters: {e}")
        return

    count = 0
    
    for ch in chapters:
        day = ch.get('day')
        topic = TOPICS.get(day, "Python Topic")
        
        # Determine strictness based on day type
        is_assessment = (day % 3 == 0) # Assumption or check topic string
        
        # Content Sources
        sources = []
        if ch.get('content_part2_practice'):
            sources.append(('part2', ch.get('content_part2_practice')))
        if is_assessment and ch.get('content_part1_theory'):
            sources.append(('part1_assessment', ch.get('content_part1_theory')))

        for src_name, content in sources:
            # Regex Strategy
            # Match headers composed of "Exercise", "Challenge", "Question"
            # Capture the Title and the Body until the next Header (##)
            
            # Pattern:
            # (###? .*) -> Header
            # ((?:.|\n)*?) -> Body (Lazy match)
            # (?=^#|\Z) -> Positive Lookahead for next header or End of String
            
            pattern = re.compile(r"^(#{2,4}\s+(?:Exercise|Challenge|Question|Problem).*?)\n((?:.|\n)*?)(?=^#{2,4}|\Z)", re.MULTILINE)
            
            matches = pattern.findall(content)
            
            if not matches:
                # Try fallback for numbered lists if headers missing (Common in older gens)
                # e.g. "**1. task name**"
                fallback_pattern = re.compile(r"(\*\*\d+\..*?\*\*)\n((?:.|\n)*?)(?=\*\*\d+\.|\Z)", re.MULTILINE)
                matches = fallback_pattern.findall(content)

            for i, (header, body) in enumerate(matches):
                # Clean Title
                title = header.strip().replace('#', '').strip()
                if "**" in title: title = title.replace('**', '').strip()
                
                # Check Dedupe
                try:
                    check = client.table("exercises").select("id").eq("day_number", day).eq("title", title).execute()
                    if check.data:
                        continue
                except: pass

                difficulty = "Hard" if is_assessment and "part2" in src_name else "Medium"
                if "part1" in src_name: difficulty = "Easy"

                payload = {
                    "day_number": day,
                    "filename": f"day_{day}_ex_{i}.py",
                    "title": title,
                    "description": body.strip(),
                    "source": "textbook",
                    "difficulty": difficulty,
                    "topic": topic,
                    "xp_reward": 20 if difficulty == "Easy" else 50
                }
                
                try:
                    client.table("exercises").insert(payload).execute()
                    count += 1
                    logger.info(f"✅ Extracted Day {day}: {title}")
                except Exception as e:
                    logger.error(f"❌ Insert Failed Day {day}: {e}")

    logger.info(f"--- Extraction Complete ---")
    logger.info(f"New Exercises: {count}")

if __name__ == "__main__":
    extract_exercises()
