# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f9ae54df-3f45-4243-82f0-d5b19d7cd73c",
# META       "default_lakehouse_name": "Lakehouse_Gold",
# META       "default_lakehouse_workspace_id": "a6b4e00b-73ec-4e35-8473-9788aa78062e",
# META       "known_lakehouses": [
# META         {
# META           "id": "f9ae54df-3f45-4243-82f0-d5b19d7cd73c"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC CREATE OR REPLACE TABLE Lakehouse_Gold.fact_cotacoes
# MAGIC USING DELTA
# MAGIC AS
# MAGIC   
# MAGIC -- Mínimas datas por moeda
# MAGIC WITH base_dados AS (
# MAGIC SELECT
# MAGIC     c.Moeda,
# MAGIC     MIN(c.Data) AS min_data
# MAGIC FROM Lakehouse_Silver.cotacoes c
# MAGIC GROUP BY c.Moeda
# MAGIC ),
# MAGIC 
# MAGIC -- Gera todas as datas do período
# MAGIC datas_periodo AS (
# MAGIC SELECT
# MAGIC     Moeda,
# MAGIC     explode(
# MAGIC         sequence(
# MAGIC             min_data,
# MAGIC             current_date(), --Data atual
# MAGIC             interval 1 day
# MAGIC         )
# MAGIC     ) AS Data
# MAGIC FROM base_dados
# MAGIC ),
# MAGIC 
# MAGIC -- Mescla as cotações atuais com as datas do período
# MAGIC dados_completos AS (
# MAGIC SELECT
# MAGIC     dp.Moeda,
# MAGIC     dp.Data,
# MAGIC     COALESCE(c.Cotacao, NULL) AS Cotacao
# MAGIC FROM datas_periodo dp
# MAGIC LEFT JOIN Lakehouse_Silver.cotacoes c
# MAGIC ON dp.Moeda = c.Moeda 
# MAGIC     AND dp.Data = c.Data
# MAGIC ),
# MAGIC 
# MAGIC -- Preenche as lacunas com a última cotação de cada moeda
# MAGIC fact_cotacoes_final AS (
# MAGIC SELECT
# MAGIC     Moeda,
# MAGIC     Data,
# MAGIC     last_value(Cotacao, true)
# MAGIC     OVER (
# MAGIC         PARTITION BY Moeda
# MAGIC         ORDER BY Data
# MAGIC         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
# MAGIC     ) AS Cotacao
# MAGIC FROM dados_completos
# MAGIC )
# MAGIC 
# MAGIC -- Saída
# MAGIC SELECT * FROM fact_cotacoes_final
# MAGIC ORDER BY Data, Moeda;


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
