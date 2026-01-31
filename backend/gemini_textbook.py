
import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load params
load_dotenv()

class GeminiTextbook:
    """
    AI Content Generator for PythonBook.
    Handles prompt loading and Gemini API calls.
    """
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logging.error("❌ GEMINI_API_KEY not found.")
            raise ValueError("GEMINI_API_KEY is required.")
            
        genai.configure(api_key=api_key)
        
        # Use Gemini 1.5 Pro or Flash for long context
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def _load_prompt(self, template_name: str) -> str:
        """Load a prompt template from prompts/ directory."""
        try:
            # Locate prompts dir relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            prompt_path = os.path.join(base_dir, "prompts", template_name)
            
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error loading prompt {template_name}: {e}")
            raise

    def generate_part1_theory(self, day: int, topic: str, lesson_content: str) -> str:
        """Generate Part 1: Theory."""
        template = self._load_prompt("part1_theory.md")
        
        # Simple string replacement (Jinja2 is overkill for this)
        prompt = template.replace("{{day}}", str(day)) \
                        .replace("{{topic}}", topic) \
                        .replace("{{lesson_content}}", lesson_content)
                        
        return self._call_gemini(prompt)

    def generate_part2_practice(self, day: int, topic: str, quiz_data: dict, boss_battle: dict) -> str:
        """Generate Part 2: Practice."""
        template = self._load_prompt("part2_practice.md")
        
        # Format quiz questions nicely
        quiz_str = "No quiz data available."
        if quiz_data and 'questions' in quiz_data:
            import json
            # If it's a string, load it. If list/dict, dump it nicely.
            q_obj = quiz_data['questions']
            if isinstance(q_obj, str):
                try: q_obj = json.loads(q_obj)
                except: pass
            quiz_str = json.dumps(q_obj, indent=2)
            
        # Format boss battle
        boss_str = "No boss battle availble."
        if boss_battle:
            boss_str = str(boss_battle.get('content') or boss_battle.get('challenge', ''))

        prompt = template.replace("{{day}}", str(day)) \
                        .replace("{{topic}}", topic) \
                        .replace("{{quiz_questions}}", quiz_str) \
                        .replace("{{boss_challenge}}", boss_str)
                        
        return self._call_gemini(prompt)

    def generate_part3_mentor(self, day: int, topic: str, nuggets: list) -> str:
        """Generate Part 3: Mentor."""
        template = self._load_prompt("part3_mentor.md")
        
        # Format nuggets
        nuggets_str = "No specific tips available."
        if nuggets:
            items = []
            for n in nuggets:
                content = n.get('content', '')
                type_ = n.get('type', 'Tip')
                items.append(f"[{type_}] {content}")
            nuggets_str = "\n".join(items)

        prompt = template.replace("{{day}}", str(day)) \
                        .replace("{{topic}}", topic) \
                        .replace("{{nuggets}}", nuggets_str)
                        
        return self._call_gemini(prompt)
    
    def generate_weekly_summary(self, week: int, topics_list: list) -> str:
        """Generate Weekly Summary."""
        template = self._load_prompt("weekly_summary.md")
        
        start_day = (week - 1) * 7 + 1
        end_day = week * 7
        
        topics_str = "\n".join([f"- Day {t['day']}: {t['topic']}" for t in topics_list])
        
        prompt = template.replace("{{week}}", str(week)) \
                        .replace("{{start_day}}", str(start_day)) \
                        .replace("{{end_day}}", str(end_day)) \
                        .replace("{{topics}}", topics_str) \
                        .replace("{{key_concepts}}", "See individual days.")
                        
        return self._call_gemini(prompt)

    def _call_gemini(self, prompt: str) -> str:
        """Call the API with retries."""
        try:
            response = self.model.generate_content(prompt)
            # Basic validation
            if not response.text:
                raise ValueError("Empty response from Gemini")
            return response.text
        except Exception as e:
            logging.error(f"Gemini API Error: {e}")
            # In production, add retry logic here
            raise
