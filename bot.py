import websocket
import json
import requests
import time
import statistics

# TELEGRAM (SEUS DADOS)
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


def probabilidade_subida():

    if len(historico) < 20:
        return 0

    ultimos = historico[-20:]

    baixos = len([x for x in ultimos if x < 2])
    medios = len([x for x in ultimos if 2 <= x <= 5])
    altos = len([x for x in ultimos if x > 5])

    score = 0

    if baixos > 10:
        score += 40

    if altos < 2:
        score += 30

    if medios < 5:
        score += 20

    return score


def detectar_repeticao():

    if len(historico) < 10:
        return False

    ultimos = historico[-10:]

    baixos = [x for x in ultimos if x < 2]

    if len(baixos) >= 6:
        return True

    return False


def detectar_timing():

    if len(historico) < 5:
        return False

    ultimos = historico[-5:]

    media = statistics.mean(ultimos)

    if media < 2:
        return True

    return False


def detectar_explosao():

    if len(historico) < 6:
        return False

    ultimos = historico[-6:]

    if ultimos[-1] < 1.5 and ultimos[-2] < 1.5 and ultimos[-3] < 1.5:
        return True

    return False


def analisar():

    global ultimo_sinal

    agora = time.time()

    if agora - ultimo_sinal < 180:
        return

    prob = probabilidade_subida()

    repeticao = detectar_repeticao()
    timing = detectar_timing()
    explosao = detectar_explosao()

    if prob > 60 and repeticao:

        enviar_sinal(
            "🚀 SINAL FORTE AVIATOR\n"
            f"📊 Probabilidade: {prob}%\n"
            "🎯 Entrada próxima rodada\n"
            "💰 Saída 2.20x"
        )

        ultimo_sinal = agora
        return


    if explosao:

        enviar_sinal(
            "🔥 POSSÍVEL EXPLOSÃO\n"
            "🚀 Entrada agressiva\n"
            "💰 Saída 3.00x"
        )

        ultimo_sinal = agora
        return


    if timing:

        enviar_sinal(
            "📉 TIMING DETECTADO\n"
            "🎯 Entrada segura\n"
            "💰 Saída 2.00x"
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
