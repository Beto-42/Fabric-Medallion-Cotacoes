# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "bf702687-1640-4847-bcff-f34de4f1e9e8",
# META       "default_lakehouse_name": "Lakehouse_Bronze",
# META       "default_lakehouse_workspace_id": "a6b4e00b-73ec-4e35-8473-9788aa78062e",
# META       "known_lakehouses": [
# META         {
# META           "id": "bf702687-1640-4847-bcff-f34de4f1e9e8"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import requests

url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=json&$select=simbolo,nomeFormatado"

response = requests.get(url)

dados = response.json()['value']

df = spark.createDataFrame(dados)



df = df.selectExpr(
    "nomeFormatado AS MoedaNome",
    "simbolo AS Moeda"
)

# display(df)

df.write.mode('overwrite').saveAsTable('dim_moeda')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from dim_moeda

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
