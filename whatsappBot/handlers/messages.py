def process_message(message):
    message = message.lower()

    if "oi" in message:
        return "Olá! Como posso te ajudar?"
    elif "preço" in message:
        return "Temos planos a partir de R$99."
    elif "contato" in message:
        return "Você pode falar com um atendente humano."
    else:
        return "Desculpa, não entendi. Pode reformular?"
