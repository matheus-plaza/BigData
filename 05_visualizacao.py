import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("--- 5. GERANDO 10 VISUALIZAÇÕES (FINAL) ---")

# Cria a pasta de saída
os.makedirs("graficos", exist_ok=True)

# Configurações visuais
sns.set_theme(style="whitegrid") # Fundo branco com linhas suaves
plt.rcParams.update({'figure.max_open_warning': 0}) # Evita avisos de memória

print(">> Lendo dataset de 1 milhão...")
df = pd.read_csv("dados_final_1m.csv")
df['data_transacao'] = pd.to_datetime(df['data_transacao'])

# Criar colunas auxiliares para os gráficos
df['ano_mes'] = df['data_transacao'].dt.to_period('M').astype(str)
df['UF'] = df['municipio'].apply(lambda x: x[-2:]) # Extrai a sigla do estado
df['dia_semana'] = df['data_transacao'].dt.day_name()

# -----------------------------------------------------------
# GRÁFICO 1: Evolução Temporal (Linha)
# Mostra se as vendas subiram ou desceram ao longo dos anos
# -----------------------------------------------------------
print("1. Gerando: Evolução Temporal...")
vendas_mes = df.groupby('ano_mes')['valor_transacao'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=vendas_mes, x='ano_mes', y='valor_transacao', color='#1f77b4', linewidth=2.5)
plt.xticks(rotation=45)
plt.title("1. Evolução do Faturamento Total (2019-2025)", fontsize=14, fontweight='bold')
plt.xlabel("Mês/Ano")
plt.ylabel("Total Vendido (R$)")
plt.tight_layout()
plt.savefig("graficos/01_evolucao_vendas.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 2: Top 10 Cidades (Barras Horizontais)
# Mostra quais cidades movimentam mais dinheiro
# -----------------------------------------------------------
print("2. Gerando: Top 10 Cidades...")
top_cidades = df.groupby('municipio')['valor_transacao'].sum().sort_values(ascending=False).head(10).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=top_cidades, y='municipio', x='valor_transacao', palette='viridis')
plt.title("2. As 10 Cidades com Maior Movimentação Econômica", fontsize=14, fontweight='bold')
plt.xlabel("Total Vendido (R$)")
plt.ylabel("Cidade")
plt.tight_layout()
plt.savefig("graficos/02_top_cidades.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 3: Dispersão (Dólar vs Valor da Compra)
# Mostra se o dólar alto faz as transações ficarem mais caras
# -----------------------------------------------------------
print("3. Gerando: Correlação Dólar...")
# Usamos amostra de 2000 pontos para o gráfico não ficar uma mancha preta
amostra = df.sample(2000)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=amostra, x='dolar', y='valor_transacao', alpha=0.5, color='orange')
# Adiciona linha de tendência
sns.regplot(data=amostra, x='dolar', y='valor_transacao', scatter=False, color='red')
plt.title("3. Impacto da Cotação do Dólar no Valor da Compra", fontsize=14, fontweight='bold')
plt.savefig("graficos/03_dispersao_dolar.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 4: Histograma de Preços
# Mostra qual a faixa de preço mais comum (ticket médio)
# -----------------------------------------------------------
print("4. Gerando: Distribuição de Preços...")
plt.figure(figsize=(10, 6))
sns.histplot(df['valor_transacao'], bins=50, kde=True, color='purple')
plt.title("4. Distribuição dos Valores das Transações (Ticket Médio)", fontsize=14, fontweight='bold')
plt.xlabel("Valor da Transação (R$)")
plt.savefig("graficos/04_histograma_valores.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 5: Share por Estado (Pizza)
# Mostra a fatia de mercado dos 5 maiores estados vs resto
# -----------------------------------------------------------
print("5. Gerando: Pizza Estados...")
vendas_uf = df.groupby('UF')['valor_transacao'].sum().sort_values(ascending=False)
top5 = vendas_uf.head(5)
outros = pd.Series([vendas_uf.iloc[5:].sum()], index=['Outros'])
pizza_data = pd.concat([top5, outros])

plt.figure(figsize=(8, 8))
plt.pie(pizza_data, labels=pizza_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title("5. Concentração Econômica por Estado (Top 5)", fontsize=14, fontweight='bold')
plt.savefig("graficos/05_pizza_estados.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 6: Inflação x Volume de Vendas (Regressão)
# Mostra se a inflação alta diminui a quantidade de compras
# -----------------------------------------------------------
print("6. Gerando: Inflação (IPCA)...")
# Agrupa por mês para ver a média
dados_ipca = df.groupby('ano_mes').agg({'ipca': 'mean', 'valor_transacao': 'count'}).reset_index()

plt.figure(figsize=(10, 6))
sns.regplot(data=dados_ipca, x='ipca', y='valor_transacao', color='green')
plt.title("6. Efeito da Inflação na Quantidade de Vendas", fontsize=14, fontweight='bold')
plt.xlabel("Índice IPCA (%)")
plt.ylabel("Quantidade de Vendas")
plt.savefig("graficos/06_ipca_vendas.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 7: Boxplot por Dia da Semana
# Mostra qual dia da semana tem vendas mais variadas
# -----------------------------------------------------------
print("7. Gerando: Boxplot Dias da Semana...")
ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.figure(figsize=(10, 6))
sns.boxplot(data=df.sample(5000), x='dia_semana', y='valor_transacao', order=ordem_dias, palette="Set2")
plt.title("7. Variação de Vendas por Dia da Semana", fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.savefig("graficos/07_boxplot_semana.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 8: Barras Agrupadas (Vendas por Trimestre)
# Mostra sazonalidade (começo vs fim de ano)
# -----------------------------------------------------------
print("8. Gerando: Sazonalidade Trimestral...")
df['trimestre'] = df['data_transacao'].dt.quarter
vendas_trim = df.groupby('trimestre')['valor_transacao'].mean().reset_index()

plt.figure(figsize=(8, 6))
sns.barplot(data=vendas_trim, x='trimestre', y='valor_transacao', palette='magma')
plt.title("8. Ticket Médio por Trimestre (Sazonalidade)", fontsize=14, fontweight='bold')
plt.xlabel("Trimestre (1=Jan-Mar, 4=Out-Dez)")
plt.savefig("graficos/08_trimestres.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 9: Matriz de Correlação (Heatmap)
# Mostra estatisticamente quem influencia quem
# -----------------------------------------------------------
print("9. Gerando: Mapa de Calor...")
correlacao = df[['valor_transacao', 'dolar', 'ipca']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("9. Matriz de Correlação Econômica", fontsize=14, fontweight='bold')
plt.savefig("graficos/09_heatmap.png")
plt.close()

# -----------------------------------------------------------
# GRÁFICO 10: Curva ABC (Pareto Acumulado)
# Mostra que poucos clientes/transações representam muito dinheiro
# -----------------------------------------------------------
print("10. Gerando: Curva de Pareto...")
df_sorted = df.sort_values('valor_transacao', ascending=False)
df_sorted['acumulado'] = df_sorted['valor_transacao'].cumsum()
total_vendas = df_sorted['valor_transacao'].sum()
df_sorted['porcentagem'] = df_sorted['acumulado'] / total_vendas * 100

# Amostra para o gráfico não pesar
pareto_sample = df_sorted.iloc[::500].reset_index(drop=True)

plt.figure(figsize=(10, 6))
sns.lineplot(data=pareto_sample, x=pareto_sample.index, y='porcentagem', color='darkblue')
plt.axhline(80, color='red', linestyle='--', label='80% da Receita')
plt.title("10. Curva de Pareto (Acumulado)", fontsize=14, fontweight='bold')
plt.ylabel("% Acumulada do Faturamento")
plt.legend()
plt.savefig("graficos/10_pareto.png")
plt.close()

print("\n--- [SUCESSO TOTAL] ---")
print("Projeto Finalizado! Confira a pasta 'graficos' e prepare sua apresentação.")
print("Parabéns por completar o pipeline de Big Data!")