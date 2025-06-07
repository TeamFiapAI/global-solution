from fastapi import APIRouter, HTTPException
from sistema.repository.oracle import dropar_tabelas, executar_ddl, executar_insert

router = APIRouter(prefix="/manutencao", tags=["Manutenção"])

@router.post("/recriar-tabelas")
def recriar_base():
    try:
        dropar_tabelas()
        executar_ddl()
        return {"status": "ok", "mensagem": "Tabelas recriadas com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/popular-tabelas")
def popular_base():
    try:
        executar_insert()
        return {"status": "ok", "mensagem": "Tabelas populadas com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-completo")
def resetar_completo():
    try:
        dropar_tabelas()
        executar_ddl()
        executar_insert()
        return {"status": "ok", "mensagem": "Reset completo da base realizado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
