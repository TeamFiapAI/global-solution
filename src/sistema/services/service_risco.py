from sistema.prediction.model import prever_vazao
from sistema.interfaces.telegram_bot import notificar_todos

def processar_previsao(dados: dict) -> dict:
    resultado = prever_vazao(dados)

    if resultado["nivel_de_risco"] == "Crítico":
        mensagem = (
            f"🚨 ALERTA DE ENCHENTE\n"
            f"Vazão prevista: {resultado['vazao_prevista']} m³/s\n"
            f"Risco: CRÍTICO"
        )
        notificar_todos(mensagem)

    return resultado
