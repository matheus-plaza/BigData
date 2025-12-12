import pandas as pd

print("--- LENDO ARQUIVO PARQUET (HADOOP) ---")

# O Pandas usa a engine 'pyarrow' (que instalamos) para abrir o arquivo
df = pd.read_parquet("dados_hadoop.parquet")

print(f"Total de linhas: {len(df)}")
print("Amostra dos dados:")
print(df.head())