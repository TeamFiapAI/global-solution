import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sistema.prediction.model import get_df_limpo, get_modelo

def gerar_e_salvar_graficos():
    df = get_df_limpo()
    modelo = get_modelo()

    if df is None or modelo is None:
        raise RuntimeError("Modelo ou dados ainda não carregados.")

    img_path = os.path.join(os.path.dirname(__file__), "../../../assets")
    os.makedirs(img_path, exist_ok=True)

    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Gráfico 1: Matriz de Correlação
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
    plt.title("Matriz de Correlação")
    plt.tight_layout()
    plt.savefig(os.path.join(img_path, "correlacao.png"))
    plt.close()

    # Gráfico 2: Precipitação Anual
    plt.figure(figsize=(14, 4))
    df.set_index("data")["precipitacao_mm"].resample("Y").sum().plot()
    plt.title("Precipitação Anual Acumulada")
    plt.ylabel("mm")
    plt.xlabel("Ano")
    plt.grid()
    plt.tight_layout()
    plt.savefig(os.path.join(img_path, "precipitacao_anual.png"))
    plt.close()

    # Gráfico 3: Importância das Variáveis
    importancias = modelo.feature_importances_
    X = df.drop(columns=["data", "vazao"])
    df_imp = pd.DataFrame({"Variável": X.columns, "Importância": importancias})
    df_imp = df_imp.sort_values(by="Importância", ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x="Importância", y="Variável", data=df_imp, palette="viridis")
    plt.title("Importância das Variáveis")
    plt.tight_layout()
    plt.savefig(os.path.join(img_path, "importancia_variaveis.png"))
    plt.close()
