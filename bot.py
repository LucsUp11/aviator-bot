import requests
import time

TOKEN = "8781088670:AAEsHrAu6y7z2VNfyWU-NZeAwjLpTywfB7A"
CHAT_ID = "1545696519"

while True:
    mensagem = "🚀 SINAL AVIATOR DETECTADO\n💰 Entrar agora\n🎯 Saída 2.00x"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mensagem
    })

    print("Sinal enviado...")

    time.sleep(60)
