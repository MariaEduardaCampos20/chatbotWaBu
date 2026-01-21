from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

resp = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": "Responda apenas: Nexa ativa"}]
)

print(resp.choices[0].message.content)
