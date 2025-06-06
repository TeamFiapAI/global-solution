from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import os
import io
import zipfile
from sistema.services.service_chart import gerar_e_salvar_graficos

router = APIRouter()

@router.get("/graficos/gerar")
def gerar_graficos():
    try:
        gerar_e_salvar_graficos()
        return {"status": "ok", "mensagem": "Gráficos salvos em /assets com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/download-todos")
def baixar_graficos_zip():
    gerar_e_salvar_graficos()

    img_dir = os.path.join(os.path.dirname(__file__), "../../../assets")
    nomes_arquivos = [
        "correlacao.png",
        "precipitacao_anual.png",
        "importancia_variaveis.png"
    ]

    # Cria um buffer de memória para armazenar o zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for nome in nomes_arquivos:
            caminho_completo = os.path.join(img_dir, nome)
            zip_file.write(caminho_completo, arcname=nome)

    zip_buffer.seek(0)

    return StreamingResponse(zip_buffer, media_type="application/x-zip-compressed", headers={
        "Content-Disposition": "attachment; filename=grafico_risco.zip"
    })
