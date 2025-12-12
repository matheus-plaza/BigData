import pandas as pd
from pymongo import MongoClient
from minio import Minio
import os

print("--- 4. ARMAZENAMENTO (POPULANDO BANCOS) ---")

# 1. Ler dados
df = pd.read_csv("dados_final_1m.csv")

# ---------------------------------------------------------
# A. NoSQL (MongoDB)
# ---------------------------------------------------------
print(">> 1. Enviando para MongoDB (NoSQL)...")
try:
    client = MongoClient("mongodb://admin:password123@localhost:27017/")
    db = client["economia_db"]
    col = db["transacoes"]
    col.drop()  # Limpa se existir

    # Envia lote de 5.000 (só para demonstrar, pois 1M demora)
    dados_json = df.head(5000).to_dict("records")
    col.insert_many(dados_json)
    print(f"   [SUCESSO] {len(dados_json)} documentos inseridos no Mongo.")
except Exception as e:
    print(f"   [ERRO] Mongo: {e}")

# ---------------------------------------------------------
# B. Data Lake (MinIO)
# ---------------------------------------------------------
print(">> 2. Enviando para Data Lake (MinIO)...")
try:
    client_minio = Minio("localhost:9000", access_key="admin", secret_key="password123", secure=False)
    if not client_minio.bucket_exists("datalake"):
        client_minio.make_bucket("datalake")

    df.to_csv("temp.csv", index=False)
    client_minio.fput_object("datalake", "raw/dados_brutos.csv", "temp.csv")
    os.remove("temp.csv")
    print("   [SUCESSO] CSV enviado para o Data Lake.")
except Exception as e:
    print(f"   [ERRO] MinIO: {e}")

# ---------------------------------------------------------
# C. Hadoop (Arquivo Parquet)
# ---------------------------------------------------------
print(">> 3. Gerando Arquivo Hadoop (Parquet)...")
try:
    df.to_parquet("dados_hadoop.parquet", index=False)
    print("   [SUCESSO] Arquivo .parquet gerado na pasta do projeto.")
except Exception as e:
    print(f"   [ERRO] Parquet: {e}")