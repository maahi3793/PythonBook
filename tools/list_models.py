import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    with open("available_models.txt", "w") as f:
        print("Found models:", file=f)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}", file=f)
    print("Models written to available_models.txt")
except Exception as e:
    print(f"Error listing models: {e}")

