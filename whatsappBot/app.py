from flask import Flask, request
import requests
from groq import Groq
import os
from dotenv import load_dotenv

# ================================
# 🔧 CONFIGURAÇÃO INICIAL
# ================================
load_dotenv()
app = Flask(__name__)

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

if not all([TOKEN, PHONE_ID, GROQ_API_KEY, VERIFY_TOKEN]):
    print("❌ ERRO: Variáveis de ambiente faltando!")
    exit(1)

print("✅ Variáveis carregadas com sucesso!")

client = Groq(api_key=GROQ_API_KEY)

# ================================
# 🤖 FUNÇÃO QUE FALA COM O GROQ
# ================================
def gerar_resposta_groq(texto_usuario):
    try:
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é a Nexa, uma IA profissional, educada e prestativa."},
                {"role": "user", "content": texto_usuario}
            ]
        )
        return resposta.choices[0].message.content
    except Exception as e:
        print(f"❌ Erro no Groq: {e}")
        return "Tive um problema ao responder."

# ================================
# 🧪 TESTE INICIAL DO GROQ
# ================================
print("🔄 Testando Groq...")
try:
    print("Resposta teste:", gerar_resposta_groq("Olá, o que é a Nexa?"), "\n")
    print("✅ Groq OK!\n")
except Exception as e:
    print(f"❌ Erro no Groq: {e}")
    exit(1)

# ================================
# 💻 MODO CHAT NO TERMINAL
# ================================
def chat_terminal():
    print("\n🤖 Modo Terminal Ativado! Digite 'sair' para encerrar.\n")
    while True:
        user_input = input("Você: ")

        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Encerrando chat...")
            break

        resposta = gerar_resposta_groq(user_input)
        print("Wabu:", resposta)

# ================================
# 🌐 WEBHOOK WHATSAPP
# ================================
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        print("✅ Webhook verificado!")
        return challenge

    print("❌ Token inválido")
    return "Erro de verificação", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📨 Webhook recebido:", data)

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        texto = msg["text"]["body"]
        numero = msg["from"]
        print(f"💬 {numero}: {texto}")

        resposta_texto = gerar_resposta_groq(texto)

        url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {"body": resposta_texto}
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("✅ Mensagem enviada!")
        else:
            print("❌ Erro ao enviar:", response.text)

    except Exception as e:
        print(f"❌ Erro no webhook: {e}")

    return "ok", 200

# ================================
# 🚀 ESCOLHA DO MODO DE EXECUÇÃO
# ================================
if __name__ == "__main__":
    print("Escolha o modo de execução:")
    print("1 - Servidor WhatsApp (Flask)")
    print("2 - Chat direto no Terminal")

    modo = input("Digite 1 ou 2: ")

    if modo == "1":
        print("\n🚀 Iniciando servidor Flask...")
        print(f"📱 Phone ID: {PHONE_ID}")
        print(f"🔐 Verify Token: {VERIFY_TOKEN}")
        print("=" * 50)
        app.run(port=5000, debug=True)
    else:
        chat_terminal()

