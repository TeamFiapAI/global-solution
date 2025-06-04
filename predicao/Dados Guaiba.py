import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# --- 1. Carregamento e limpeza dos dados ---

# Carregar CSV
df = pd.read_csv("Dados_Historicos_Porto_Alegre_Com_Vazao_V2.csv", sep=';', encoding='ISO-8859-1')

# Converter a coluna de data
df["Data Medicao"] = pd.to_datetime(df["Data Medicao"], dayfirst=True, errors="coerce")

# Converter colunas numéricas
colunas_numericas = df.columns.drop("Data Medicao")
for col in colunas_numericas:
    df[col] = df[col].astype(str).str.replace('.', '', regex=False)  # remover separador de milhar
    df[col] = df[col].str.replace(',', '.', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remover linhas com valores ausentes
df_limpo = df.dropna()

# Verificar dados
print(df.info())
print(df.head())

# --- 2. Visualização inicial ---

# Matriz de correlação
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Matriz de Correlação")
plt.show()

# Precipitação ao longo dos anos
plt.figure(figsize=(14, 4))
df.set_index("Data Medicao")["PRECIPITACAO TOTAL, DIARIO(mm)"].resample("Y").sum().plot()
plt.title("Precipitação Anual Acumulada")
plt.ylabel("mm")
plt.xlabel("Ano")
plt.grid()
plt.show()

# --- 3. Separação de variáveis ---

X = df_limpo.drop(columns=["Data Medicao", "MEDIA DIARIA DE VAZÃO"])
y = df_limpo["MEDIA DIARIA DE VAZÃO"]

print("\nVariáveis utilizadas para previsão:")
print(X.columns.tolist())

# --- 4. Treinamento do modelo ---

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train_scaled, y_train)

# Previsão
y_pred = modelo.predict(X_test_scaled)

# Avaliação
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\nDesempenho do modelo:")
print(f"R²: {r2:.4f}")
print(f"RMSE: {rmse:.2f}")

# --- 5. Importância das variáveis ---

importancias = modelo.feature_importances_
colunas = X.columns
importancia_df = pd.DataFrame({'Variável': colunas, 'Importância': importancias})
importancia_df = importancia_df.sort_values(by='Importância', ascending=False)

# Exibir
print("\nImportância das variáveis no modelo Random Forest:")
print(importancia_df)

# Gráfico
plt.figure(figsize=(10, 6))
sns.barplot(x='Importância', y='Variável', data=importancia_df, palette='viridis')
plt.title("Importância das variáveis na previsão da vazão")
plt.tight_layout()
plt.show()

# --- 6. Lógica de alerta com sistema de decisão ---

def classificar_nivel_de_risco(vazao):
    if vazao < 3000:
        return "Baixo"
    elif vazao < 6000:
        return "Moderado"
    else:
        return "Crítico"

niveis_de_risco = [classificar_nivel_de_risco(v) for v in y_pred]

# Alerta geral
if "Crítico" in niveis_de_risco:
    print("\n⚠️ ALERTA MÁXIMO: Condição crítica de vazão prevista!")
elif "Moderado" in niveis_de_risco:
    print("\n⚠️ Atenção: Risco moderado detectado. Monitoramento necessário.")
else:
    print("\n✅ Situação normal. Vazão dentro dos padrões seguros.")

print("\nPrevisões detalhadas:")
for i in range(len(y_pred)):
    print(f"Previsão {i+1}: Vazão = {y_pred[i]:.2f} m³/s → Risco: {niveis_de_risco[i]}")

# --- 7. Terminal Interativo para Previsão Manual ---

print("\n💧 Previsão personalizada de vazão (entrada manual):")
dados_usuario = []
for coluna in X.columns:
    while True:
        try:
            valor = float(input(f"Digite o valor para '{coluna}': "))
            dados_usuario.append(valor)
            break
        except ValueError:
            print("Valor inválido. Por favor, digite um número válido.")

entrada_usuario = scaler.transform([dados_usuario])
vazao_prevista = modelo.predict(entrada_usuario)[0]
risco_usuario = classificar_nivel_de_risco(vazao_prevista)

print("\n🔍 Previsão baseada nos dados inseridos:")
print(f"Vazão prevista: {vazao_prevista:.2f} m³/s")
print(f"🚨 Nível de Risco: {risco_usuario}")

