import websocket
import json
import base64
import requests
import time

# TELEGRAM
TOKEN = "8781088670:AAEsHrAu6y7z2VNfyWU-NZeAwjLpTywfB7A"
CHAT_ID = "1545696519"

historico = []
ultimo_sinal = 0


def enviar_sinal(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def analisar():
    global ultimo_sinal
    global historico

    if len(historico) < 8:
        return

    agora = time.time()

    # evita spam
    if agora - ultimo_sinal < 300:
        return

    ultimos = historico[-8:]

    baixos = [x for x in ultimos if x < 2]

    if len(baixos) >= 5:
        enviar_sinal(
            "🚀 SINAL AVIATOR\n"
            "📉 Sequência baixa detectada\n"
            "🎯 Entrada próxima rodada\n"
            "💰 Saída 2.00x"
        )

        ultimo_sinal = agora


def on_message(ws, message):
    global historico

    try:
        if "crash" in message.lower():

            valor = float(
                message.split("crash")[-1]
                .replace('"', "")
                .replace(":", "")
                [:4]
            )

            historico.append(valor)

            print("Novo:", valor)

            analisar()

    except:
        pass


def on_open(ws):
    print("Conectado Betano")


ws = websocket.WebSocketApp(
    "wss://et.sa-east-1.spribegaming.com/api/v1/public/et-player-stomp/853/v4sjmrrx/websocket?currency=BRL&userId=325836026&token=325836026%7C2eb1768f3356499c8b05509b1d55d636&operator=betanobr&sessionToken=7uyvXOSqg7IcPkR7xs6LnxPxGHz6BuHT5FUEl1xpEGvMJ7X9ftE6tIwr0emT6hcY&deviceType=desktop&gameIdentifier=AVIATOR&gameZone=aviator_core_inst5_sa&lang=pt-br",
    on_message=on_message,
    on_open=on_open
)


while True:
    try:
        ws.run_forever()
    except:
        print("Reconectando...")
        time.sleep(5)
