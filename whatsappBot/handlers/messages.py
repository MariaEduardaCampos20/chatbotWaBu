def process_message(message):
    message = message.lower()

    if "oi" in message:
        return "Olá! Como posso te ajudar?"
    elif "Pedido" in message:
        return "Faça seu pedido aqui: https://instadelivery.com.br/joaoalemaobar."
    elif "cardapio" in message:
        return ""
    else:
        return "Desculpa, não entendi. Pode reformular?"
