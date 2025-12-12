import sidrapy
from bcb import sgs

print("--- INICIANDO COLETA ---")

# 1. PIB (IBGE)
print("1. Coletando PIB...")
try:
    pib_br = sidrapy.get_table(table_code="5938", territorial_level="6", ibge_territorial_code="all", variable="37", period="last 4")
    pib_br.columns = pib_br.iloc[0]
    pib_br = pib_br.iloc[1:].reset_index(drop=True)
    pib_br = pib_br.rename(columns={"Município (Código)": "cod_ibge", "Município": "municipio", "Ano": "ano", "Valor": "pib_valor"})
    df_pib = pib_br[['cod_ibge', 'municipio', 'ano', 'pib_valor']]
    df_pib.to_csv("dados_pib_bruto.csv", index=False)
    print(f"   -> PIB salvo: {len(df_pib)} linhas.")
except Exception as e:
    print(f"   -> Erro IBGE: {e}")

# 2. MACRO (BCB)
print("2. Coletando Dólar e IPCA...")
try:
    df_macro = sgs.get({'ipca': 433, 'dolar': 1}, start='2019-01-01')
    df_macro = df_macro.reset_index()
    df_macro.to_csv("dados_macro_bruto.csv", index=False)
    print(f"   -> Macro salvo: {len(df_macro)} linhas.")
except Exception as e:
    print(f"   -> Erro BCB: {e}")