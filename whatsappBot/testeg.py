from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("🔄 Testando Groq API...")
print(f"API Key: {GROQ_API_KEY[:20]}...")

try:
    client = Groq(api_key=GROQ_API_KEY)
    
    chat = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Responda apenas: OK"}
        ],
        model="llama-3.3-70b-versatile"
    )
    
    print("✅ GROQ FUNCIONANDO!")
    print(f"Resposta: {chat.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ ERRO na Groq: {e}")