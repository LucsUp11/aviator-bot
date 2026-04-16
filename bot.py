import websocket
import requests
import time
import json
import statistics

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

    if len(historico) < 10:
        return

    agora = time.time()

    if agora - ultimo_sinal < 180:
        return

    ultimos = historico[-10:]

    baixos = [x for x in ultimos if x < 2]

    if len(baixos) >= 6:
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

        # Spribe manda JSON dentro do STOMP
        if "multiplier" in message:

            start = message.find("{")
            end = message.rfind("}") + 1

            json_data = message[start:end]

            data = json.loads(json_data)

            if "multiplier" in data:

                valor = float(data["multiplier"])

                historico.append(valor)

                print("Novo:", valor)

                analisar()

    except Exception as e:
        print("Erro:", e)


def on_open(ws):

    print("Conectado Betano")

    # STOMP CONNECT
    ws.send("CONNECT\naccept-version:1.2\n\n\x00")

    time.sleep(1)

    # Subscribe Aviator
    ws.send(
        "SUBSCRIBE\nid:sub-0\ndestination:/topic/aviator\n\n\x00"
    )


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
