from flask import Flask, request
import requests
from groq import Groq
import os
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

app = Flask(__name__)

# 🔑 CHAVES
TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# Valida variáveis
if not all([TOKEN, PHONE_ID, GROQ_API_KEY, VERIFY_TOKEN]):
    print("❌ ERRO: Variáveis de ambiente faltando!")
    exit(1)

print("✅ Variáveis carregadas com sucesso!")

# Inicializa Groq
client = Groq(api_key=GROQ_API_KEY)

# ✨ ADICIONE ESTE BLOCO AQUI - Bypass do aviso do Ngrok
@app.before_request
def before_request():
    # Adiciona header para bypass do aviso do ngrok
    pass

@app.after_request
def after_request(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response
# ✨ FIM DO BLOCO NOVO

# Teste inicial
print("🔄 Testando Groq...")
try:
    chat = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Você é um assistente educado e profissional da Nexa."},
            {"role": "user", "content": "Olá, o que é a Nexa?"}
        ],
        model="llama-3.3-70b-versatile"
    )
    print("✅ Groq OK!")
    print(f"Resposta teste: {chat.choices[0].message.content}\n")
except Exception as e:
    print(f"❌ Erro no Groq: {e}")
    exit(1)

# 🔁 VERIFICAÇÃO DO WEBHOOK (Meta)
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if token == VERIFY_TOKEN:
        print(f"✅ Webhook verificado!")
        return challenge
    
    print(f"❌ Token inválido recebido: {token}")
    return "Erro de verificação", 403

# 📩 RECEBE MENSAGEM
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(f"📨 Webhook recebido: {data}")

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        texto = msg["text"]["body"]
        numero = msg["from"]
        
        print(f"💬 Mensagem de {numero}: {texto}")
        
    except KeyError as e:
        print(f"⚠️ Mensagem sem texto ou formato inesperado: {e}")
        return "ok"
    except Exception as e:
        print(f"❌ Erro ao processar webhook: {e}")
        return "ok"

    # 🤖 Gera resposta com IA
    try:
        print("🤖 Gerando resposta com IA...")
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é a Nexa, uma IA de atendimento profissional e educada."},
                {"role": "user", "content": texto}
            ]
        )
        
        resposta_texto = resposta.choices[0].message.content
        print(f"🤖 IA respondeu: {resposta_texto}")
        
    except Exception as e:
        print(f"❌ Erro na IA: {e}")
        resposta_texto = "Desculpe, estou com dificuldades no momento. Tente novamente."

    # 📤 ENVIA PARA WHATSAPP
    try:
        url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {
                "body": resposta_texto
            }
        }



        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Mensagem enviada com sucesso!")
        else:
            print(f"❌ Erro ao enviar mensagem: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao enviar para WhatsApp: {e}")

    return "ok"

if __name__ == "__main__":
    print("\n🚀 Iniciando servidor Flask...")
    print(f"📱 Phone ID: {PHONE_ID}")
    print(f"🔐 Verify Token: {VERIFY_TOKEN}")
    print("=" * 50)
    app.run(port=5000, debug=True)