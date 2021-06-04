### Desafio Coronavírus

### Limpando Plots, Console and Ambiente
rm(list = ls())
dev.off(dev.list()["RStudioGD"])
cat("\014")

### Lendo aquivos csv
caso_full <- read.csv("~/Desktop/Unifor-MBA-DScience/R/00-Aulas/desafio/caso_full.csv")
obito_cartorio <- read.csv("~/Desktop/Unifor-MBA-DScience/R/00-Aulas/desafio/obito_cartorio.csv")

### Selecionando observações
s_caso_full <- caso_full[which(caso_full$state == 'CE'), ]
s_obito_cartorio <- obito_cartorio[which(obito_cartorio$state == 'CE'), ]

### Retirando linhas com falta de observações
sum(complete.cases(s_caso_full))
s_caso_full <- s_caso_full[complete.cases(s_caso_full), ]

### Juntando seleções
j_casos <- merge(x = s_caso_full, y = s_obito_cartorio, by = "date", all.x = TRUE)

### Hora de criar gráficos
### Use a sua criatividade!!!
