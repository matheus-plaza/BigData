import pandas as pd
import numpy as np
from datetime import timedelta

print("--- PROCESSAMENTO E GERAÇÃO DE 1 MILHÃO ---")

# 1. Carregar
df_pib = pd.read_csv("dados_pib_bruto.csv")
df_macro = pd.read_csv("dados_macro_bruto.csv")

# 2. Preparar Pesos (PIB)
df_pib['pib_valor'] = pd.to_numeric(df_pib['pib_valor'], errors='coerce')
df_pib = df_pib.dropna(subset=['pib_valor'])
df_pesos = df_pib[df_pib['ano'] == df_pib['ano'].max()].copy()
df_pesos['probabilidade'] = df_pesos['pib_valor'] / df_pesos['pib_valor'].sum()

# 3. Preparar Datas (Corrigimos Finais de Semana)
print("   -> Ajustando calendário...")
df_macro['Date'] = pd.to_datetime(df_macro['Date'])
df_macro = df_macro.set_index('Date')
full_range = pd.date_range(start=df_macro.index.min(), end=df_macro.index.max())
df_macro = df_macro.reindex(full_range).ffill().bfill().reset_index().rename(columns={'index': 'Date'})

# 4. Gerar Sintéticos
NUM = 1_000_000
print(f"   -> Gerando {NUM} registros...")

cidades = np.random.choice(df_pesos['cod_ibge'], size=NUM, p=df_pesos['probabilidade'])

# Datas aleatórias
dias_total = (df_macro['Date'].max() - df_macro['Date'].min()).days
dias_rand = np.random.randint(0, dias_total, NUM)
datas = [df_macro['Date'].min() + timedelta(days=int(d)) for d in dias_rand]

df_big = pd.DataFrame({'cod_ibge': cidades, 'data_transacao': datas})

# 5. Enriquecer
print("   -> Cruzando dados...")
df_big = df_big.merge(df_pesos[['cod_ibge', 'municipio']], on='cod_ibge', how='left')
df_big['data_transacao'] = pd.to_datetime(df_big['data_transacao'])
df_big = df_big.merge(df_macro, left_on='data_transacao', right_on='Date', how='left')

# Valor Transação
base = np.random.uniform(10, 5000, NUM)
df_big['valor_transacao'] = (base * (1 + (df_big['dolar'].fillna(5) / 100))).round(2)

# Salvar
df_big.drop(columns=['Date']).to_csv("dados_final_1m.csv", index=False)
print("--- SUCESSO: 'dados_final_1m.csv' CRIADO ---")