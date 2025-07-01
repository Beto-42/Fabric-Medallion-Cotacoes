# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "45ce5419-0223-4095-a853-f078b1287519",
# META       "default_lakehouse_name": "Lakehouse_Silver",
# META       "default_lakehouse_workspace_id": "a6b4e00b-73ec-4e35-8473-9788aa78062e",
# META       "known_lakehouses": [
# META         {
# META           "id": "45ce5419-0223-4095-a853-f078b1287519"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Leitura dos arquivos Parquet na pasta Novos
df = spark.read.parquet("Files/Cotacoes/Novos/*.parquet")

df.createOrReplaceTempView("df")

df = spark.sql("""
    SELECT 
        cotacaoCompra AS Cotacao,
        CAST(dataHoraCotacao AS DATE) AS Data,
        moeda AS Moeda
    FROM
        df
    ORDER BY Data ASC
""").dropDuplicates(["Moeda", "Data"])

display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC -- Cria uma tabela no lake se não existir
# MAGIC CREATE TABLE IF NOT EXISTS cotacoes (
# MAGIC     Cotacao DOUBLE,
# MAGIC     Data DATE,
# MAGIC     Moeda STRING
# MAGIC )
# MAGIC USING DELTA
# MAGIC PARTITIONED BY (Moeda)

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Executa o merge na tabela cotacoes

df.createOrReplaceTempView('df_novos')

spark.sql("""
    MERGE INTO cotacoes AS e
    USING (
        SELECT
            Cotacao,
            Data,
            Moeda
        FROM
            df_novos    

    ) as n
    ON e.Moeda = n.Moeda
        AND e.Data = n.Data
    WHEN NOT MATCHED THEN
        INSERT (Cotacao, Data, Moeda)
        VALUES (n.Cotacao, n.Data, n.Moeda)                                                                                                                                                
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC -- Contagem de linhas
# MAGIC SELECT COUNT(*) FROM cotacoes

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Movimentação dos arquivos parquet da pasta Novos para Carregados

from notebookutils import mssparkutils

origem = f"abfss://Medallion@onelake.dfs.fabric.microsoft.com/Lakehouse_Bronze.Lakehouse/Files/Cotacoes/Novos"  
destino = f"abfss://Medallion@onelake.dfs.fabric.microsoft.com/Lakehouse_Bronze.Lakehouse/Files/Cotacoes/Carregados/" 

if not mssparkutils.fs.exists(destino):
    mssparkutils.fs.mkdirs(destino)

arquivos = mssparkutils.fs.ls(origem)

for arquivo in arquivos:
    caminho_origem = arquivo.path
    nome_arquivo = arquivo.name
    caminho_destino = f"{destino}{nome_arquivo}"
    
    mssparkutils.fs.mv(caminho_origem, caminho_destino)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
