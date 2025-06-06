from fastapi import FastAPI
import threading
import uvicorn
import asyncio
from sistema.routers import sensor_router
from sistema.routers.dashboard_router import router as dashboard_router
from sistema.prediction import model
from sistema.interfaces.telegram_bot import iniciar_bot_async

app = FastAPI(
    title="Global Solution - Previsão de Enchentes",
    description="API para receber dados de sensores e prever risco de enchentes",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    model.treinar_modelo()
    import asyncio
    asyncio.get_event_loop().create_task(iniciar_bot_async())

# Rota com prefixo /dados
app.include_router(sensor_router.router, prefix="/dados", tags=["Sensores"])
app.include_router(dashboard_router, prefix="/graficos", tags=["Gráficos"])

# Menu do terminal
def exibir_menu():
    print("\n=== Centro de Gerenciamento de Emergências ===")
    print("1. Sair")
    print("2. Enviar alerta manual (para inscritos no bot)")

def menu_loop():
    from sistema.interfaces.telegram_bot import notificar_todos
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("Encerrando sistema...")
            break
        elif opcao == "2":
            msg = input("Digite a mensagem de alerta: ")
            notificar_todos(f"🚨 {msg}")
        else:
            print("Opção inválida. Tente novamente.")

# Entry point
if __name__ == "__main__":
    threading.Thread(target=menu_loop, daemon=True).start()

    uvicorn.run("sistema.main:app", host="0.0.0.0", port=8000, reload=True)
