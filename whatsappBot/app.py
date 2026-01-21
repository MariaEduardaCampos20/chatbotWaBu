from flask import Flask, request
import requests
from groq import Groq

app = Flask(__name__)

# 🔑 CHAVES
TOKEN = "SEU_TOKEN_WHATSAPP"
PHONE_ID = "SEU_PHONE_NUMBER_ID"
GROQ_API_KEY = "SUA_GROQ_API_KEY"

client = Groq(api_key=GROQ_API_KEY)

# 🔁 VERIFICAÇÃO DO WEBHOOK (Meta)
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == "nexa123":
        return request.args.get("hub.challenge")
    return "Erro de verificação", 403

# 📩 RECEBE MENSAGEM
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        texto = msg["text"]["body"]
        numero = msg["from"]
    except:
        return "ok"

    # 🤖 IA
    resposta = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Você é a Nexa, uma IA de atendimento profissional."},
            {"role": "user", "content": texto}
        ]
    )

    resposta_texto = resposta.choices[0].message.content

    # 📤 ENVIA PARA WHATSAPP
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "text": {"body": resposta_texto}
    }

    requests.post(url, headers=headers, json=payload)

    return "ok"

if __name__ == "__main__":
    app.run(port=5000)
