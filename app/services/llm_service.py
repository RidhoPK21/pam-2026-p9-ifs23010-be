import os
from google import genai

def generate_from_llm(prompt: str):
    try:
        # 1. Pindahkan inisialisasi ke dalam fungsi agar PASTI terbaca setelah .env diload
        # SDK google-genai secara otomatis mencari os.environ["GEMINI_API_KEY"],
        # jadi kita tidak perlu menuliskannya secara manual di dalam kurung ().
        client = genai.Client()

        # Menggunakan model Gemini 1.5 Flash
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        
        raw_text = response.text

        # 2. PEMBERSIH MARKDOWN (ANTI-CRASH)
        # Menghapus bungkus ```json dan ``` jika AI menambahkannya
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1)
            raw_text = raw_text.replace("```", "")
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "")
            
        raw_text = raw_text.strip()

        # Mengembalikan Dictionary bersih
        return {
            "response": raw_text
        }
        
    except Exception as e:
        print(f"Error LLM: {str(e)}")
        raise Exception("LLM request failed")