import websocket
import json
import base64
import requests
import time

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


def detectar_ciclo():
    if len(historico) < 20:
        return False

    ultimos = historico[-20:]

    baixos = [x for x in ultimos if x < 2]
    medios = [x for x in ultimos if 2 <= x <= 5]
    altos = [x for x in ultimos if x > 5]

    # ciclo clássico aviator
    if len(baixos) > 10 and len(altos) < 3:
        return True

    return False


def detectar_sequencia():
    if len(historico) < 8:
        return False

    ultimos = historico[-8:]

    baixos = [x for x in ultimos if x < 2]

    if len(baixos) >= 5:
        return True

    return False


def detectar_explosao():
    if len(historico) < 5:
        return False

    ultimos = historico[-5:]

    # Alto depois de sequência baixa
    if ultimos[-5] > 10 and all(x < 2 for x in ultimos[-4:]):
        return True

    return False


def analisar():
    global ultimo_sinal

    agora = time.time()

    # evita spam
    if agora - ultimo_sinal < 240:
        return

    if detectar_ciclo():
        enviar_sinal(
            "🚀 CICLO DETECTADO\n"
            "📊 Probabilidade alta\n"
            "🎯 Entrada próxima rodada\n"
            "💰 Saída 2.20x"
        )

        ultimo_sinal = agora
        return

    if detectar_sequencia():
        enviar_sinal(
            "📉 SEQUÊNCIA BAIXA\n"
            "🎯 Entrada próxima rodada\n"
            "💰 Saída 2.00x"
        )

        ultimo_sinal = agora
        return

    if detectar_explosao():
        enviar_sinal(
            "🔥 POSSÍVEL EXPLOSÃO\n"
            "🚀 Entrada agressiva\n"
            "💰 Saída 3.00x"
        )

        ultimo_sinal = agora
        return


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
