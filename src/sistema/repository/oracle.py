import oracledb
import os
import json
from datetime import datetime

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
CONFIG_PATH = os.path.join(BASE_PATH, "config", "config.json")
SCRIPTS_PATH = os.path.join(BASE_PATH, "scripts")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

DB_USER = config["ORACLE_USER"]
DB_PASSWORD = config["ORACLE_PASSWORD"]
DB_DSN = config["ORACLE_DSN"]

CAMINHO_SCRIPT_DROP = os.path.join(SCRIPTS_PATH, "drop.sql")
CAMINHO_SCRIPT_DDL = os.path.join(SCRIPTS_PATH, "ddl.sql")
CAMINHO_SCRIPT_INSERT = os.path.join(SCRIPTS_PATH, "insert.sql")

def get_conn():
    connection = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )
    return connection

from datetime import datetime
from sistema.repository.oracle import get_conn

def salvar_dados_wokwi(
    distancia_atual_cm, distancia_anterior_cm, temperatura,
    umidade, vento_velocidade_ms, insolacao_h,
    evaporacao_piche_mm, precipitacao_mm, data_recebimento
):
    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dados_wokwi (
                    distancia_atual_cm, distancia_anterior_cm, temperatura,
                    umidade, vento_velocidade_ms, insolacao_h,
                    evaporacao_piche_mm, precipitacao_mm, data_recebimento
                ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
            """, [
                distancia_atual_cm, distancia_anterior_cm, temperatura,
                umidade, vento_velocidade_ms, insolacao_h,
                evaporacao_piche_mm, precipitacao_mm, data_recebimento
            ])
            conn.commit()

            # Captura o último ID inserido
            cursor.execute("SELECT MAX(id) FROM dados_wokwi")
            dados_id = cursor.fetchone()[0]
            return dados_id

    except Exception as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Erro ao salvar dados do Wokwi: {e}")
    finally:
        if conn:
            conn.close()

def salvar_predicao(dados_id, vazao_prevista, risco, explicabilidade=None):
    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO predicoes (
                    dados_id, vazao_prevista, risco, explicabilidade, data_predicao
                ) VALUES (:1, :2, :3, :4, :5)
            """, [
                int(dados_id),
                float(vazao_prevista),
                str(risco),
                explicabilidade,
                datetime.utcnow()
            ])
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Erro ao salvar predição: {e}")
    finally:
        if conn:
            conn.close()

def salvar_alerta_telegram(predicao_id, mensagem):
    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO alertas_telegram (
                    predicao_id, mensagem, data_envio
                ) VALUES (:1, :2, :3)
            """, [
                predicao_id, mensagem, datetime.utcnow()
            ])
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Erro ao salvar alerta Telegram: {e}")
    finally:
        if conn:
            conn.close()

def dropar_tabelas():
    print("\n=== Verificando necessidade de dropar tabelas ===")

    if not os.path.exists(CAMINHO_SCRIPT_DROP):
        print(f"Script não encontrado: '{CAMINHO_SCRIPT_DROP}'")
        return

    with open(CAMINHO_SCRIPT_DROP, "r", encoding="utf-8") as f:
        ddl = f.read()

    comandos = [cmd.strip() for cmd in ddl.split(";") if cmd.strip()]

    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            for comando in comandos:
                try:
                    cursor.execute(comando)
                except oracledb.DatabaseError as e:
                    error, = e.args
                    if error.code == 942:  # Tabela não existe
                        print("Tabela inexistente. Ignorando exclusão.")
                    else:
                        print(f"Erro no DROP:\n{comando}\n→ {error.message}")
                        raise
            conn.commit()
            print("Comandos de DROP executados (ou ignorados onde necessário).")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao dropar tabelas: {e}")
    finally:
        if conn:
            conn.close()

def executar_ddl():
    print("\n=== Executando script DDL ===")

    if not os.path.exists(CAMINHO_SCRIPT_DDL):
        print(f"Script não encontrado: '{CAMINHO_SCRIPT_DDL}'")
        return

    with open(CAMINHO_SCRIPT_DDL, "r", encoding="utf-8") as f:
        ddl = f.read()

    comandos = [cmd.strip() for cmd in ddl.split(";") if cmd.strip()]

    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            for comando in comandos:
                try:
                    cursor.execute(comando)
                except oracledb.DatabaseError as e:
                    error, = e.args
                    if error.code in [955, 2275]:  # Objeto existe ou constraint já criada
                        print("Objeto ou constraint já existe. Ignorando.")
                    else:
                        print(f"Erro no DDL:\n{comando}\n→ {error.message}")
                        raise
            conn.commit()
            print("Script DDL executado com sucesso.")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao executar DDL: {e}")
    finally:
        if conn:
            conn.close()

def executar_insert():
    print("\n=== Executando inserts ===")

    if not os.path.exists(CAMINHO_SCRIPT_INSERT):
        print(f"Script não encontrado: '{CAMINHO_SCRIPT_INSERT}'")
        return

    with open(CAMINHO_SCRIPT_INSERT, "r", encoding="utf-8") as f:
        inserts = f.read()

    comandos = [cmd.strip() for cmd in inserts.split(";") if cmd.strip()]

    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            for comando in comandos:
                try:
                    cursor.execute(comando)
                    print(f"✅ INSERT executado:\n{comando}")
                except oracledb.DatabaseError as e:
                    error, = e.args
                    print(f"Erro no INSERT:\n{comando}\n→ {error.message}")
                    continue
            conn.commit()
            print("Todos os INSERTs foram processados.")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro ao executar inserts: {e}")
    finally:
        if conn:
            conn.close()

def buscar_todos(tabela=None, colunas="*", ordem_por=None, sql_query=None):
    registros = []
    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cursor:
            if sql_query:
                cursor.execute(sql_query)
            elif tabela:
                sql = f"SELECT {colunas} FROM {tabela}"
                if ordem_por:
                    sql += f" ORDER BY {ordem_por}"
                cursor.execute(sql)
            else:
                print("Erro: informe tabela ou SQL.")
                return []

            col_names = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                registros.append([
                    col.read() if hasattr(col, "read") else col for col in row
                ])
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Erro ao buscar: {error.message}")
    finally:
        if conn:
            conn.close()
    return registros