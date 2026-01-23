from dotenv import load_dotenv
import os

load_dotenv()

print("📋 Testando variáveis de ambiente:")
print(f"GROQ_API_KEY: {os.getenv('GROQ_API_KEY')[:20]}..." if os.getenv('GROQ_API_KEY') else "❌ Não encontrada")
print(f"WHATSAPP_TOKEN: {os.getenv('WHATSAPP_TOKEN')[:20]}..." if os.getenv('WHATSAPP_TOKEN') else "❌ Não encontrada")
print(f"PHONE_NUMBER_ID: {os.getenv('PHONE_NUMBER_ID')}")
print(f"VERIFY_TOKEN: {os.getenv('VERIFY_TOKEN')}")