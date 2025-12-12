import pandas as pd
import numpy as np
from datetime import timedelta

print("--- 2. PROCESSAMENTO E GERAÇÃO DE DADOS ---")

# 1. Carregar
df_pib = pd.read_csv("dados_pib_bruto.csv")
df_macro = pd.read_csv("dados_macro_bruto.csv")

# 2. Preparar Pesos (PIB)
df_pib['pib_valor'] = pd.to_numeric(df_pib['pib_valor'], errors='coerce')
df_pib = df_pib.dropna(subset=['pib_valor'])

# Pega apenas o ano mais recente para não duplicar cidade no sorteio
df_pesos = df_pib[df_pib['ano'] == df_pib['ano'].max()].copy()
# Cria coluna de probabilidade baseada no total do PIB
df_pesos['probabilidade'] = df_pesos['pib_valor'] / df_pesos['pib_valor'].sum()

# 3. Preparar Datas (Corrigimos Finais de Semana)
print("   -> Ajustando calendário...")
df_macro['Date'] = pd.to_datetime(df_macro['Date'])
df_macro = df_macro.set_index('Date')

# Cria calendario completo de 2019 ate hoje
full_range = pd.date_range(start=df_macro.index.min(), end=df_macro.index.max())

# Reindexa e usa ffill para repetir cotacao de sexta no sabado/domingo
df_macro = df_macro.reindex(full_range).ffill().bfill().reset_index().rename(columns={'index': 'Date'})

# 4. Gera as 1 milhão de linhas
NUM_REGISTROS = 1_000_000
print(f">> Gerando {NUM_REGISTROS} registros...")

# Sorteia cidades usando o peso do PIB
cidades_sorteadas = np.random.choice(
    df_pesos['cod_ibge'],
    size=NUM_REGISTROS,
    p=df_pesos['probabilidade']
)

# Sorteia datas aleatorias dentro do periodo
dias_total = (df_macro['Date'].max() - df_macro['Date'].min()).days
dias_rand = np.random.randint(0, dias_total, NUM_REGISTROS)
datas_geradas = [df_macro['Date'].min() + timedelta(days=int(d)) for d in dias_rand]

# Cria o dataframe principal
df_big = pd.DataFrame({
    'cod_ibge': cidades_sorteadas,
    'data_transacao': datas_geradas
})

# 5. Cruza os dados (Merge) e define preços
print(">> Cruzando tabelas e calculando valores...")

# Traz nome da cidade
df_big = df_big.merge(df_pesos[['cod_ibge', 'municipio']], on='cod_ibge', how='left')

# Traz dolar e ipca da data correspondente
df_big['data_transacao'] = pd.to_datetime(df_big['data_transacao'])
df_big = df_big.merge(df_macro, left_on='data_transacao', right_on='Date', how='left')

# Logica de preço: Produto Importado (Preço em Dolar * Cotação do Dia)
# Gera um preço base em dolar (entre $10 e $1000)
preco_base_dolar = np.random.uniform(5, 1000, NUM_REGISTROS)

# Garante que nao tem nulos no dolar antes de multiplicar
cotacao = df_big['dolar'].fillna(5.0)

# Calcula valor final em reais
df_big['valor_transacao'] = (preco_base_dolar * cotacao).round(2)

# 6. Salva o resultado
print(">> Salvando csv final...")
df_big = df_big.drop(columns=['Date']) # remove coluna duplicada
df_big.to_csv("dados_final_1m.csv", index=False)

print("--- Sucesso! Arquivo gerado. ---")