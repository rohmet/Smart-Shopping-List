import os
import json
from dotenv import load_dotenv
import requests
import re

# Load API key dari file .env
load_dotenv()
API_KEY = os.getenv("HF_API_KEY")

# Pastikan API Key ada
if not API_KEY:
    raise ValueError("HF_API_KEY tidak ditemukan. Pastikan ada di file .env Anda.")

# Menggunakan endpoint dari skrip Anda yang berhasil
API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}"}

def query(payload):
    """Mengirim request ke Hugging Face Chat Completions API."""
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return {"error": f"Request gagal. Status: {response.status_code}", "raw": response.text}
    return response.json()

def extract_json(text: str) -> str:
    """Mengekstrak string JSON dari teks yang lebih besar."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return ""

def shopping_category_recommendation(teks_belanjaan: str) -> dict:
    """
    Mengirim permintaan ke Chat Completions API untuk mengkategorikan belanjaan.
    """
    
    prompt = f"""
    Anda adalah asisten yang bertugas mengkategorikan daftar belanja.
    Kategorikan daftar belanja berikut ke dalam format JSON.
    Jawaban HARUS berupa JSON yang valid dan tidak boleh ada teks penjelasan lain di luar blok JSON.
    Daftar Belanja: "{teks_belanjaan}"

    Contoh format output yang diinginkan:
    {{
      "Buah & Sayur": ["apel", "pisang", "bayam"],
      "Produk Susu": ["susu UHT", "keju"],
      "Minuman": ["kopi bubuk", "teh celup"],
      "Kebutuhan Dapur": ["gula pasir", "minyak goreng"]
    }}
    """
    
    payload = {
        # DIUBAH: Menambahkan kembali tag provider ':featherless-ai'
        "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.1,
    }
    
    result = query(payload)
    
    if "error" in result:
        return result

    try:
        generated_text = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return {"error": "Struktur respons API tidak sesuai harapan.", "raw": result}

    json_str = extract_json(generated_text)
    
    if not json_str:
        return {"error": "Tidak ada JSON yang ditemukan di respons model", "raw": generated_text}

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        data = {"error": "Output dari model bukan JSON yang valid", "raw_json_string": json_str}
        
    return data
