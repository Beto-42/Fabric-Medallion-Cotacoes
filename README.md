# Fabric-Medallion-Cotacoes

Criação da estrutura Medallion (ou Medalhão) no Microsoft Fabric em um projeto de ponta a ponta requisitando, tratando e exibindo dados provenientes de uma API pública.
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos 
Configurei o Lakehouse e estruturei com as camadas Bronze, Silver e Gold tanto em arquivos como em tabelas Delta.
Contrui notebooks utilizando PySpark e SparkSql para limpeza, transformação e enriquecimento de dados.
Também configurei um Data Pipeline para orquestrar o fluxo de atualização entre as camadas.
Por fim, montei um modelo semântico em Direct Lake e um relatório do Power BI diretamente do Fabric através do navegador.
