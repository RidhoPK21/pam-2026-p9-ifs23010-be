import os
from google import genai

# Inisialisasi Client Gemini yang baru
# Secara otomatis akan membaca GEMINI_API_KEY dari file .env kamu
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_from_llm(prompt: str):
    try:
        # Menggunakan model Gemini 2.5 Flash terbaru
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Mengembalikan dalam format Dictionary seperti yang diminta oleh parser.py
        return {
            "response": response.text
        }
        
    except Exception as e:
        print(f"Error LLM: {str(e)}")
        raise Exception("LLM request failed")