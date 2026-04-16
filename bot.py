import requests
import time

TOKEN = "8781088670:AAEsHrAu6y7z2VNfyWU-NZeAwjLpTywfB7A"
CHAT_ID = "1545696519"

historico = []
ultimo_sinal = 0

def enviar_sinal(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mensagem
    })

def analisar():
    global historico
    global ultimo_sinal

    if len(historico) < 8:
        return

    agora = time.time()

    # Evita spam (1 sinal a cada 5 minutos)
    if agora - ultimo_sinal < 300:
        return

    ultimos = historico[-8:]

    baixos = [x for x in ultimos if x < 2]
    muito_baixos = [x for x in ultimos if x < 1.5]

    # 5 baixos seguidos (forte)
    if len(baixos[-5:]) == 5:
        enviar_sinal(
            "🚀 SINAL FORTE AVIATOR\n"
            "📉 5 baixos seguidos\n"
            "🎯 Saída 2.00x"
        )
        ultimo_sinal = agora
        return

    # 3 muito baixos seguidos
    if len(muito_baixos[-3:]) == 3:
        enviar_sinal(
            "🔥 POSSÍVEL EXPLOSÃO\n"
            "📊 3 muito baixos seguidos\n"
            "🎯 Saída 2.20x"
        )
        ultimo_sinal = agora
        return

    # Alto forte seguido de queda
    if ultimos[-4] > 10 and ultimos[-1] < 1.5:
        enviar_sinal(
            "⚡ PADRÃO DETECTADO\n"
            "📉 Alto forte seguido queda\n"
            "🎯 Saída 2.50x"
        )
        ultimo_sinal = agora
        return
