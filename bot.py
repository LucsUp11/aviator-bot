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

    if len(historico) < 6:
        return

    agora = time.time()

    # Evita spam (1 sinal a cada 3 minutos)
    if agora - ultimo_sinal < 180:
        return

    ultimos = historico[-6:]

    baixos = [x for x in ultimos if x < 2]
    altos = [x for x in ultimos if x > 5]

    # 4 baixos seguidos
    if len(baixos) >= 4:
        enviar_sinal(
            "🚀 SINAL AVIATOR\n"
            "📉 Sequência de baixos\n"
            "🎯 Saída 2.00x"
        )
        ultimo_sinal = agora
        return

    # Alto seguido de queda
    if ultimos[-3] > 8 and ultimos[-1] < 2:
        enviar_sinal(
            "🔥 POSSÍVEL RECUPERAÇÃO\n"
            "📊 Alto seguido de queda\n"
            "🎯 Saída 2.50x"
        )
        ultimo_sinal = agora
        return


while True:

    # SIMULAÇÃO (vamos trocar pelo websocket depois)
    novo = round(1 + (10 * (time.time() % 1)), 2)

    historico.append(novo)

    print("Novo:", novo)

    analisar()

    time.sleep(10)
