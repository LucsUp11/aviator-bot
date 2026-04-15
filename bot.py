import requests
import time

TOKEN = "SEU_TOKEN_AQUI"
CHAT_ID = "SEU_CHAT_ID"

# Simulação (depois vamos conectar ao websocket real)
historico = []

def enviar_sinal(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mensagem
    })

def analisar():
    global historico
    
    if len(historico) < 5:
        return

    ultimos = historico[-5:]

    baixos = [x for x in ultimos if x < 2]

    # 4 baixos seguidos
    if len(baixos) >= 4:
        enviar_sinal(
            "🚀 POSSÍVEL ENTRADA\n"
            "📊 4 baixos detectados\n"
            "🎯 Saída 2.00x"
        )

    # Alto seguido de baixos
    if ultimos[-5] > 10 and ultimos[-1] < 2:
        enviar_sinal(
            "🔥 PADRÃO DETECTADO\n"
            "📊 Alto seguido de baixos\n"
            "🎯 Saída 2.50x"
        )

while True:
    
    # Simulação (vamos trocar depois)
    novo = round(1 + (10 * (time.time() % 1)), 2)
    
    historico.append(novo)
    
    print("Novo:", novo)

    analisar()

    time.sleep(10)
