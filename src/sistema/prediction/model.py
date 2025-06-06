import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

modelo = None
scaler = None
colunas_modelo = None

df_limpo = None

def treinar_modelo():
    global modelo, scaler, colunas_modelo, df_limpo

    # Caminho para o CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "../../../assets/history_data.csv")

    # Carrega e renomeia as colunas
    df = pd.read_csv(csv_path, sep=';', encoding='ISO-8859-1')
    df.rename(columns={
        'EVAPORACAO DO PICHE, DIARIA(mm)': 'evaporacao_mm',
        'INSOLACAO TOTAL, DIARIO(h)': 'insolacao_h',
        'PRECIPITACAO TOTAL, DIARIO(mm)': 'precipitacao_mm',
        'TEMPERATURA MAXIMA, DIARIA(Ã\x82Â°C)': 'temp_max_c',
        'TEMPERATURA MEDIA COMPENSADA, DIARIA(Ã\x82Â°C)': 'temp_compensada_c',
        'TEMPERATURA MINIMA, DIARIA(Ã\x82Â°C)': 'temp_min_c',
        'UMIDADE RELATIVA DO AR, MEDIA DIARIA(%)': 'umidade_media_pct',
        'UMIDADE RELATIVA DO AR, MINIMA DIARIA(%)': 'umidade_min_pct',
        'VENTO, VELOCIDADE MEDIA DIARIA(m/s)': 'vento_vel_media_ms',
        'UMIDADE DO SOLO ESTIMADA': 'umidade_solo_pct',
        'MEDIA DIARIA DE VAZÃO': 'vazao',
        'Data Medicao': 'data'
    }, inplace=True)

    # Converter datas
    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")

    # Limpeza e normalização
    colunas_numericas = df.columns.drop("data")
    for col in colunas_numericas:
        df[col] = df[col].astype(str).str.replace('.', '', regex=False)
        df[col] = df[col].str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(inplace=True)
    df_limpo = df.copy()

    # Separar variáveis
    X = df.drop(columns=["data", "vazao"])
    y = df["vazao"]
    colunas_modelo = list(X.columns)

    # Treinamento
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train_scaled, y_train)

    # Log para debug
    print("\n✅ Modelo treinado e pronto para uso!")

import pandas as pd

def prever_vazao(dados: dict) -> dict:
    global modelo, scaler, colunas_modelo

    if not modelo or not scaler or not colunas_modelo:
        raise RuntimeError("O modelo ainda não foi treinado.")

    faltando = [col for col in colunas_modelo if col not in dados]
    if faltando:
        raise ValueError(f"Faltando os seguintes campos na entrada: {faltando}")

    entrada = [dados[col] for col in colunas_modelo]
    entrada_df = pd.DataFrame([entrada], columns=colunas_modelo)

    entrada_esc = scaler.transform(entrada_df)

    vazao = modelo.predict(entrada_esc)[0]

    if vazao < 3000:
        risco = "Baixo"
    elif vazao < 6000:
        risco = "Moderado"
    else:
        risco = "Crítico"

    return {
        "vazao_prevista": round(vazao, 2),
        "nivel_de_risco": risco
    }

def get_modelo():
    return modelo

def get_df_limpo():
    return df_limpo
