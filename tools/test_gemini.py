import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Key loaded: {str(api_key)[:5]}...")
genai.configure(api_key=api_key)

try:
    print("Asking Gemini a question...")
    model = genai.GenerativeModel('gemini-flash-latest')
    resp = model.generate_content("Say hello")
    print(f"Response: {resp.text}")
    print("✅ GEMINI IS WORKING")
except Exception as e:
    print(f"❌ GEMINI FAILED: {e}")
