from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sistema.services.service_risco import processar_previsao
from sistema.interfaces.telegram_bot import enviar_alerta_para_todos
from sistema.repository.oracle import salvar_alerta_telegram, salvar_dados_wokwi, salvar_predicao

router = APIRouter()

class SensorData(BaseModel):
    chuva_mm: float
    umidade: float
    pressao: float

class DadosPrevisao(BaseModel):
    PRECIPITACAO_TOTAL_DIARIO_mm: float
    TEMPERATURA_MEDIA_DIARIA_C: float
    UMIDADE_RELATIVA_DO_AR_MEDIA_DIARIA_pct: float    

class PrevisaoRequest(BaseModel):
    precipitacao_mm: float
    temperatura_maxima_c: float
    temperatura_minima_c: float
    temperatura_media_c: float
    temperatura_compensada_c: float
    umidade_media_pct: float
    umidade_minima_pct: float
    evaporacao_mm: float
    insolacao_horas: float
    vento_velocidade_ms: float
    pressao_hpa: float
    umidade_solo_pct: float

def prever_enchente(chuva_mm, umidade, pressao) -> str:
    if chuva_mm > 70 and umidade > 80 and pressao < 1000:
        return "EVACUAR"
    elif chuva_mm > 40:
        return "ALERTA"
    else:
        return "SEGURO"
    
@router.post("/teste-telegram")
async def teste_envio_alerta(msg: str = "🚨 Alerta de enchente: Teste funcionando!"):
    try:
        await notificar_todos(msg)
        return {"status": "sucesso", "mensagem_enviada": msg}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}  
    
async def notificar_todos(mensagem: str):
    await enviar_alerta_para_todos(mensagem)  # essa função precisa ser async também    

@router.post("/receber_wokwi")
def receber_string(payload: str = Body(..., media_type="text/plain")):
    try:
        valores = [float(v.strip()) for v in payload.split(";")]

        if len(valores) != 10:
            raise ValueError("Esperado 10 valores: dist_atual, dist_anterior, temp, umidade, vento, insolação, evaporação, chuva, pressão, umidade_solo.")

        # Desempacota todos os valores recebidos
        distancia_atual, distancia_anterior, temp, umid, vento, insol, evap, chuva, pressao, umidade_solo = valores

        # 1. Salvar dados crus recebidos
        dados_id = salvar_dados_wokwi(
            distancia_atual_cm=distancia_atual,
            distancia_anterior_cm=distancia_anterior,
            temperatura=temp,
            umidade=umid,
            vento_velocidade_ms=vento,
            insolacao_h=insol,
            evaporacao_piche_mm=evap,
            precipitacao_mm=chuva,
            data_recebimento=datetime.utcnow()
        )

        # 2. Monta a estrutura de previsão
        previsao = PrevisaoRequest(
            precipitacao_mm=chuva,
            temperatura_maxima_c=temp,
            temperatura_minima_c=temp,
            temperatura_media_c=temp,
            temperatura_compensada_c=temp,
            umidade_media_pct=umid,
            umidade_minima_pct=umid,
            evaporacao_mm=evap,
            insolacao_horas=insol,
            vento_velocidade_ms=vento,
            pressao_hpa=pressao,
            umidade_solo_pct=umidade_solo
        )

        entrada = request_to_model_input(previsao)
        resultado = processar_previsao(entrada)
        vazao = resultado["vazao_prevista"]
        risco = resultado["nivel_de_risco"]

        # 3. Salva predição
        predicao_id = salvar_predicao(dados_id, vazao, risco)

        return {
            "status": "ok",
            "dados_id": dados_id,
            "vazao": vazao,
            "risco": risco
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/")
def receber_dados(sensor: SensorData):
    status = prever_enchente(sensor.chuva_mm, sensor.umidade, sensor.pressao)
    return {
        "status": status,
        "dados_recebidos": sensor.dict()
    }

@router.post("/prever-vazao")
def prever(dados: PrevisaoRequest):
    try:
        entrada = request_to_model_input(dados)
        return processar_previsao(entrada)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def request_to_model_input(req: PrevisaoRequest) -> dict:
    return {
        "precipitacao_mm": req.precipitacao_mm,
        "temp_max_c": req.temperatura_maxima_c,
        "temp_min_c": req.temperatura_minima_c,
        "temp_media_c": req.temperatura_media_c,
        "temp_compensada_c": req.temperatura_compensada_c,
        "umidade_media_pct": req.umidade_media_pct,
        "umidade_min_pct": req.umidade_minima_pct,
        "evaporacao_mm": req.evaporacao_mm,
        "insolacao_h": req.insolacao_horas,
        "vento_vel_media_ms": req.vento_velocidade_ms,
        "pressao_hpa": req.pressao_hpa,
        "umidade_solo_pct": req.umidade_solo_pct
    }

