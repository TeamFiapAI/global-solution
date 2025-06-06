import cx_Oracle
import json
import os

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.json")
CAMINHO_SCRIPT_DDL = os.path.join(BASE_DIR, "scripts", "script.sql")
CAMINHO_SCRIPT_DROP = os.path.join(BASE_DIR, "scripts", "dropTables.sql")
CAMINHO_SCRIPT_INSERT = os.path.join(BASE_DIR, "scripts", "insert.sql")

print(f"Base dir: {BASE_DIR}")


# Carrega a configuração
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

ORACLE_USER = config["ORACLE_USER"]
ORACLE_PASSWORD = config["ORACLE_PASSWORD"]
ORACLE_DSN = config["ORACLE_DSN"]

def conectar():
    try:
        return cx_Oracle.connect(ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN)
    except cx_Oracle.Error as error:
        print(f"Erro ao conectar ao Oracle: {error}")
        raise

def dropar_tabelas():
    print("\n=== Verificando necessidade de dropar tabelas ===")

    if not os.path.exists(CAMINHO_SCRIPT_DROP):
        print(f"Script de criação de tabelas não encontrado em '{CAMINHO_SCRIPT_DROP}'.")
        return

    with open(CAMINHO_SCRIPT_DROP, "r", encoding="utf-8") as f:
        ddl = f.read()

    comandos = [cmd.strip() for cmd in ddl.split(";") if cmd.strip()]

    conn = None
    try:
        conn = conectar()
        with conn.cursor() as cursor:
            for comando in comandos:
                try:
                    cursor.execute(comando)
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    if error.code == 942:  # ORA-00942: table or view does not exist
                        print("Tabela não existe. Ignorando exclusão.")
                        continue
                    else:
                        print(f"\nErro ao executar comando:\n{comando}\n→ {error.message}")
                        raise
            conn.commit()
            print("Script DDL executado (ou comandos ignorados onde já existiam).")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro durante a execução do DDL: {e}")
    finally:
        if conn:
            conn.close()

def executar_ddl():
    print("\n=== Verificando base de dados ===")

    if not os.path.exists(CAMINHO_SCRIPT_DDL):
        print(f"Script de criação de tabelas não encontrado em '{CAMINHO_SCRIPT_DDL}'.")
        return

    with open(CAMINHO_SCRIPT_DDL, "r", encoding="utf-8") as f:
        ddl = f.read()

    comandos = [cmd.strip() for cmd in ddl.split(";") if cmd.strip()]

    conn = None
    try:
        conn = conectar()
        with conn.cursor() as cursor:
            for comando in comandos:
                try:
                    cursor.execute(comando)
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    if error.code == 955:  # ORA-00955: object name is already used by an existing object
                        print("Objeto já existe. Ignorando criação.")
                        continue
                    elif error.code == 2275: # ORA-02275: such a constraint already exists on table
                        print("FK já existente. Ignorando.")
                        continue
                    else:
                        print(f"\nErro ao executar comando:\n{comando}\n→ {error.message}")
                        raise
            conn.commit()
            print("Script DDL executado (ou comandos ignorados onde já existiam).")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro durante a execução do DDL: {e}")
    finally:
        if conn:
            conn.close()

def executar_insert():
    print("\n=== Verificando necessidade de inserir dados ===")

    if not os.path.exists(CAMINHO_SCRIPT_INSERT):
        print(f"Script de inserção de dados não encontrado em '{CAMINHO_SCRIPT_INSERT}'.")
        return

    with open(CAMINHO_SCRIPT_INSERT, "r", encoding="utf-8") as f:
        inserts = f.read()

    comandos_insert = [cmd.strip() for cmd in inserts.split(";") if cmd.strip()]

    conn = None
    try:
        conn = conectar()
        with conn.cursor() as cursor:
            for comando in comandos_insert:
                try:
                    cursor.execute(comando)
                    print(f"Comando INSERT executado com sucesso:\n{comando}")
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    print(f"\nErro ao executar comando INSERT:\n{comando}\n→ {error.message}")
                    continue
            conn.commit()
            print("Script de inserção de dados executado.")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erro durante a execução dos inserts: {e}")
    finally:
        if conn:
            conn.close()

def buscar_todos(tabela=None, colunas="*", ordem_por=None, sql_query=None):
    conn = None
    registros = []
    try:
        conn = conectar()
        with conn.cursor() as cursor:
            if sql_query:
                cursor.execute(sql_query)
            elif tabela:
                sql = f"SELECT {colunas} FROM {tabela}"
                if ordem_por:
                    sql += f" ORDER BY {ordem_por}"
                cursor.execute(sql)
            else:
                print("Erro: É necessário fornecer o nome da tabela ou uma consulta SQL.")
                return []
            col_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            for row in rows:
                reg = []
                for i, col in enumerate(row):
                    if isinstance(col, cx_Oracle.LOB):
                        reg.append(col.read())
                    else:
                        reg.append(col)
                registros.append(tuple(reg))
    except cx_Oracle.Error as e:
        error, = e.args
        print(f"Erro ao buscar dados: {error.message}")
    finally:
        if conn:
            conn.close()
    return registros