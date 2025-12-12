import findspark
findspark.init()
from pyspark.sql import SparkSession

print("--- SPARK START ---")

# Inicia Spark
spark = SparkSession.builder.master("local[*]").appName("Proj2").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Lê CSV
print("Lendo 1 Milhão de linhas...")
df = spark.read.csv("dados_final_1m.csv", header=True, inferSchema=True)

# Processa
print("Calculando Top Estados...")
df.createOrReplaceTempView("vendas")
resultado = spark.sql("""
    SELECT substring(municipio, -2, 2) as UF, 
           count(*) as Qtd, 
           ROUND(SUM(valor_transacao), 2) as Total
    FROM vendas 
    GROUP BY substring(municipio, -2, 2) 
    ORDER BY Total DESC
""")

resultado.show(10)
print("--- SPARK FIM ---")
spark.stop()
