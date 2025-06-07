from fastapi import FastAPI
import threading
import uvicorn
import asyncio
from sistema.routers import sensor_router
from sistema.routers.dashboard_router import router as dashboard_router
from sistema.prediction import model
from sistema.interfaces.telegram_bot import iniciar_bot_async
from sistema.routers.maintenance_router import router as maintenance_router

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
app.include_router(maintenance_router, prefix="/manutencao", tags=["Manutenção"])


# Entry point
if __name__ == "__main__":
    uvicorn.run("sistema.main:app", host="0.0.0.0", port=8000, reload=True)
