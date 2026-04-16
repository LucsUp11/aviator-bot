import websocket
import json
import requests
import time

TOKEN = "8781088670:AAEsHrAu6y7z2VNfyWU-NZeAwjLpTywfB7A"
CHAT_ID = "1545696519"

WS = "wss://et.sa-east-1.spribegaming.com/api/v1/public/et-player-stomp/600/e4bmvxgi/websocket?currency=BRL&userId=325836026&token=325836026%7Cd4a517297b894cbea718acb14d99487d&operator=betanobr&sessionToken=uWAb6fwqGKSZzGh4f01QGzAgehSUkjnjIutyn3K8BYtgyilhs2tr0EEwDkD3Oihn&deviceType=desktop&gameIdentifier=AVIATOR&gameZone=aviator_core_inst5_sa&lang=pt-br"

historico = []


def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def analisar(valor):
    historico.append(valor)

    if len(historico) < 5:
        return

    ultimos = historico[-5:]
    baixos = [x for x in ultimos if x < 2]

    if len(baixos) >= 4:
        enviar("🚀 POSSÍVEL ENTRADA\n🎯 Saída 2x")

    if ultimos[-5] > 10 and ultimos[-1] < 2:
        enviar("🔥 PADRÃO FORTE\n🎯 Saída 2.5x")


def on_message(ws, message):
    try:
        data = json.loads(message)

        if "crash" in str(data):
            valor = float(data["crash"])
            print("Crash:", valor)
            analisar(valor)

    except:
        pass


def on_error(ws, error):
    print("Erro:", error)


def on_close(ws, close_status_code, close_msg):
    print("Reconectando...")
    time.sleep(5)
    start()


def on_open(ws):
    print("Conectado Aviator 🚀")


def start():
    ws = websocket.WebSocketApp(
        WS,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.on_open = on_open
    ws.run_forever()


start()
