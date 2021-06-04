# Setando o diretorio de trabalho
setwd("C:/Users/valclemir/Documents/Azure-estudos/POS_GRADUACAO/PROJETOS_POS_GRADUACAO/INTRODUCAO_ESTATISTICA")

# Install packages
#install.packages("Hmisc")
#install.packages("plotly")
#install.packages("kableExtra")




vetor_pacotes = c(
  #"plyr",
  "readr",
  "ggplot2",
  "ggplot",
  "plotly",
  "e1071",
  "dplyr",
  "Hmisc",
  "DescTools",
  "esquisse",
  "gridExtra",
  "e1071",
  "devtools",
  "testthat",
  "Hmisc",
  "kableExtra",
  "data.table"
  
)

lapply(vetor_pacotes, require, character.only = TRUE)


#library(plyr)
#library(dplyr)



# importando dados 
enade2017 = read.csv2("MICRODADOS_ENADE_2017.txt") 

# Selecionando colunas 
colunas_filtradas = enade2017[, c('NT_OBJ_FG', 'CO_GRUPO', 'CO_REGIAO_CURSO', 'QE_I02', 'CO_TURNO_GRADUACAO')]

# Selecionando o tipo de curso 
# 701 -> Curso de matematica 
dados_mat = colunas_filtradas[colunas_filtradas$CO_GRUPO == 701, ]


# QE_I02

# A = Branca.
# B = Preta.
# C = Amarela.
# D = Parda.
# E = Indígena.
# F = Não quero declarar.


dados_mat$QE_I02[ which(dados_mat$QE_I02 == 'A') ] = 'Branca'
dados_mat$QE_I02[ which(dados_mat$QE_I02 == 'B') ] = 'Preta'
dados_mat$QE_I02[ which(dados_mat$QE_I02 == 'C') ] = 'Amarela'
dados_mat$QE_I02[ which(dados_mat$QE_I02 == 'D') ] = 'Parda'
dados_mat$QE_I02[ which(dados_mat$QE_I02 == 'E') ] = 'Indígena'
dados_mat$QE_I02[ which(dados_mat$QE_I02 == 'F') ] = 'Não quero declarar'
dados_mat$QE_I02[ which(dados_mat$QE_I02 == "")] = "Não quero declarar"




# CO_TURNO_GRADUACAO 

# 1 = Matutino
# 2 = Vespertino
# 3 = Integral
# 4 = Noturno

dados_mat$CO_TURNO_GRADUACAO[ which(dados_mat$CO_TURNO_GRADUACAO == '1') ] = 'Matutino'
dados_mat$CO_TURNO_GRADUACAO[ which(dados_mat$CO_TURNO_GRADUACAO == '2') ] = 'Vespertino'
dados_mat$CO_TURNO_GRADUACAO[ which(dados_mat$CO_TURNO_GRADUACAO == '3') ] = 'Integral'
dados_mat$CO_TURNO_GRADUACAO[ which(dados_mat$CO_TURNO_GRADUACAO == '4') ] = 'Noturno'



# CO_REGIAO_CURSO

# 1 = Norte
# 2 = Nordeste
# 3 = Sudeste
# 4 = Sul
# 5 = Centro-Oeste

dados_mat$CO_REGIAO_CURSO[ which(dados_mat$CO_REGIAO_CURSO == '1') ] = 'Norte'
dados_mat$CO_REGIAO_CURSO[ which(dados_mat$CO_REGIAO_CURSO == '2') ] = 'Nordeste'
dados_mat$CO_REGIAO_CURSO[ which(dados_mat$CO_REGIAO_CURSO == '3') ] = 'Sudeste'
dados_mat$CO_REGIAO_CURSO[ which(dados_mat$CO_REGIAO_CURSO == '4') ] = 'Sul'
dados_mat$CO_REGIAO_CURSO[ which(dados_mat$CO_REGIAO_CURSO == '5') ] = 'Centro-Oeste'



# Analise descritiva dos dados. 
Hmisc::describe(dados_mat) 

# Olhando para análise descritiva dos dados, podemos observar que a coluna QE_I02 possui dados faltantes e
# portanto, iremos elimina-los.

dados_mat = na.omit(dados_mat)

# Verificando se ainda existe dados faltantes na coluna
sum(is.na(dados_mat$QE_I02))

# Visualizando novamente a descrição dos dados 
Hmisc::describe(dados_mat) 

# podemos ver que os dados missings não existem mais


# Falando um pouco sobre cada variável: 

# Variável CO_REGIAO_CURSO
# Olhando para a variável CO_REGIAO_CURSO, a região que mais possui alunos que cursam bacharel em matemática
# é o nordeste com 15%, seguido do sul com 12%.

# Variável QE_I02.
# Essa variável diz respeito a cor do aluno, se é Branco, Indígena, Não quero declarar, Parda ou Preta
# Comparando as cores Branca, Parda e Preta. Podemos observar que a cor Branca se destaca, seguida da parda
# Já a cor preta, fica abaixo, com uma proporção de 0.089 ou 8%. Isso pode-se dar, pelo fato do negro não ter
# muitas oportunidades, pois são mais pobres e menos assistidos. 

# CO_TURNO_GRADUACAO 
# Diz respeito dos turnos



dados = dados_mat$NT_OBJ_FG

#Media
media <- function(dados){
  return (sum(dados) / length(dados))
}

#media(dados)



# Mediana 
mediana <- function(dados) {
  # No R, a contagem do elemento, começa no  1
  numero_central = round(length(dados[order(dados)]) / 2) + 1
  return ((dados[order(dados)][numero_central] + dados[order(dados)][numero_central - 2]) / 2)
  
}
#mediana(dados)



# Moda
moda <- function(dados) {
  dados_comparar <- unique(dados)
  return(dados_comparar[which.max(tabulate(match(dados, dados_comparar)))])
  
}

#moda(dados)


cv <- function (dados){
  tamanho = length(dados)
  lista_desvio = numeric(tamanho)
  lista_varianca = numeric(tamanho)
  j = 1 
  
  media = media(dados)
  
  #calcula o desvio 
  for (i in dados){
    lista_desvio[j] = abs(media - i)
    j = j + 1
  }
  
  #Calcula a varianca
  j = 1
  for (i in lista_desvio){
    lista_varianca[j] = i ** 2
    j = j + 1 
  }
  varianca = round(sum(lista_varianca) / length(lista_varianca), 2)
  
  # Calcula desvio padrao
  desvio_padrao = sqrt(varianca)
  
  return(desvio_padrao)
  
  
}

#cv(dados)



#Coeficientes de Pearson
#Primeiro Coeficiente de Assimetria de Pearson:
#  AS = (media - mediana) / desvio padrao


#Segundo Coeficiente de Assimetria de Pearson:
#  AS = 3 * (media - mediana) / desvio padrao 



assimetria <- function (dados){
  CoeficienteAssimetria = (media(dados) - mediana(dados)) / cv(dados)
  return(CoeficienteAssimetria)
}

#assimetria(dados)

# Distribuicao Assimetrica negativa, pois o resultado da subtracao da media e moda é negativa.
media(dados) - moda(dados)


# frequencia relativa
freq_rel <- function (dados){
  lista = c() 
  j = 1 
  
  for (i in unique(dados)){
    lista[j] = length(dados[which(dados == i)]) / length(dados) #Frequencia relativa
    j = j + 1
    
  }
  return (lista)
}

freq_rel(dados) * 100



# CURTOSE 
curtose = kurtosis(dados)



# salvando resultado em um dataframe
qt = c(length(dados))
me = c(media(dados))
mo = c(moda(dados))
med = c(mediana(dados))
ass = c(assimetria(dados))
curt = c(kurtosis(dados))

df = data.frame(quantidade=qt, media=me, moda=mo, mediana=med, assimetria=ass, curtose = curt)


kable_material_dark(kbl(df, digits = 2))



# Estatisticas resumo 
summary(dados)


g_hist=ggplot(dados_mat,aes(x=NT_OBJ_FG)) + 
  geom_histogram(color = "black",fill="lightblue",bins =50,aes(y=(..count..)/sum(..count..)))+
  ggtitle("Histograma da nota dos alunos de matemática ")+
  xlab("nota") +
  ylab("Frequência relativa")


g_densidade=ggplot(dados_mat,aes(x=NT_OBJ_FG))+
  geom_density(col=2,size = 1, aes(y = 27 * (..count..)/sum(..count..))) +
  ggtitle("Curva de densidade da nota dos alunos de matemática") +
  xlab("Nota dos alunos de matemática") +
  ylab("Frequência relativa")

g_hist_densidade = ggplot(dados_mat,aes(x=NT_OBJ_FG)) + 
  geom_histogram(color = "black",fill="lightblue",bins =50,aes(y=(..count..)/sum(..count..)))+
  geom_density(col=2,size = 1, aes(y = 27 * (..count..)/sum(..count..))) +
  ggtitle("Histograma e curva de densidade da nota dos alunos de matemática")+
  xlab("Nota dos alunos de matemática") +
  ylab("Frequência relativa")


grid.arrange( g_hist,
              g_densidade,
              g_hist_densidade,
              nrow=3,ncol=1)

# Olhando para os gráficos de histogramas acima, podemos observar que, 15% dos alunos, tem uma nota
# bruta de 50, enquanto que, mais de 20% da turma, tem uma nota bruta de 70.
# Para esses dados, a curtose deu um valor de -0.61 e portanto, uma curtose negativa platicúrtica. Uma curtose negativa,
# indica que a distribuição tem caudas mais leves que a distribuição normal


qt_dados_agrupados_regiao_e_raca = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02), FUN = length)
media_dados_agrupados_regiao_e_raca = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02), FUN = media)
moda_dados_agrupados_regiao_e_raca = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02), FUN = moda)
mediana_dados_agrupados_regiao_e_raca = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02), FUN = median)
cv_dados_agrupados_regiao_e_raca = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02), FUN = cv)



df_regiao_cor = data.frame(qt_dados_agrupados_regiao_e_raca,
                 media_dados_agrupados_regiao_e_raca[3],
                 moda_dados_agrupados_regiao_e_raca[3],
                 mediana_dados_agrupados_regiao_e_raca[3],
                 cv_dados_agrupados_regiao_e_raca[3])

nomes_colunas = c("regiao", "cor", "quantidade", "media", "moda", "mediana", "cv")

#Ajusta nome das colunas
setnames(df_regiao_cor, nomes_colunas)
df_order_by = arrange(df_regiao_cor, desc(media), desc(moda), desc(mediana), desc(cv))

kable_material_dark(kbl(df_order_by, digits = 2)) 


# Na tabela mostrada acima, podemos observar que os alunos do sul e de cor parda, 
# tem uma média e mediana, superior aos outros alunos de outras regiões,
# seria esses dois alunos, outliers? Para isso, vamos plotar um grafico de boxplot, 
# para analisar melhor essa situação.





fig <- plot_ly(type = 'box')
fig <- fig %>% add_boxplot(y = as.list(df_order_by$media), name = "Media", boxpoints = TRUE,
                           marker = list(color = 'rgb(9,56,125)'),
                           line = list(color = 'rgb(9,56,125)'))

fig <- fig %>% add_boxplot(y = as.list(df_order_by$mediana), name = "Mediana", boxpoints = TRUE,
                           marker = list(color = 'rgb(9,56,255)'),
                           line = list(color = 'rgb(9,56,125)'))

fig <- fig %>% add_boxplot(y = as.list(df_order_by$moda), name = "Moda", boxpoints = TRUE,
                           marker = list(color = 'rgb(9,56,255)'),
                           line = list(color = 'rgb(9,56,255)'))

fig 


# Bom, com isso confirma nossa duvida. Os alunos são sim outliers. O que poderia levar esses alunos terem notas tão altas? 
# Será se é por conta dos alunos estudarem mais tempo que outros e por serem muito dedicados, os levam a tirar boas notas?
# Vamos mais fundo nos dados e ver se é esse o motivo.


# Fazendo agrupamento e comparacao por regiao, cor e turno
qt_dados_agrupados_regiao_e_cor_turno = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02, dados_mat$CO_TURNO_GRADUACAO), FUN = length)
media_dados_agrupados_regiao_e_cor_turno = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02, dados_mat$CO_TURNO_GRADUACAO), FUN = media)
moda_dados_agrupados_regiao_e_cor_turno = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02, dados_mat$CO_TURNO_GRADUACAO), FUN = moda)
mediana_dados_agrupados_regiao_e_cor_turno = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02, dados_mat$CO_TURNO_GRADUACAO), FUN = median)
cv_dados_agrupados_regiao_e_cor_turno = aggregate(dados_mat$NT_OBJ_FG, list(dados_mat$CO_REGIAO_CURSO, dados_mat$QE_I02, dados_mat$CO_TURNO_GRADUACAO), FUN = cv)



df_regiao_cor = data.frame(qt_dados_agrupados_regiao_e_cor_turno,
                           media_dados_agrupados_regiao_e_cor_turno[4],
                           moda_dados_agrupados_regiao_e_cor_turno[4],
                           mediana_dados_agrupados_regiao_e_cor_turno[4],
                           cv_dados_agrupados_regiao_e_cor_turno[4])

nomes_colunas = c("regiao", "cor", "turno", "quantidade", "media", "moda", "mediana", "cv")

#Ajusta nome das colunas
setnames(df_regiao_cor, nomes_colunas)
df_order_by = arrange(df_regiao_cor, desc(media), desc(moda), desc(mediana), desc(cv))

kable_material_dark(kbl(df_order_by, digits = 2)) 

# Os alunos do sul e com tempo integral de estudo, de fato, conseguem ter notas mais elevadas. 
# Isso justifica seu alto desempenho, pois são mais dedicados e mais assistidos que outros.

# Gráfico box-plot da Nota por região
grafico_boxplot1 = ggplot(dados_mat, aes(x=QE_I02,y=dados_mat$NT_OBJ_FG,fill=dados_mat$QE_I02)) + 
  geom_boxplot() +
  ggtitle("Gráfico box-plot da nota por turno e região")+
  xlab("Turno") +
  ylab("Notas") +
  facet_grid(~CO_TURNO_GRADUACAO)+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))


ggplotly(grafico_boxplot1)


grafico_boxplot2 = ggplot(dados_mat, aes(x=QE_I02,y=dados_mat$NT_OBJ_FG,fill=dados_mat$QE_I02)) + 
  geom_boxplot() +
  ggtitle("Gráfico box-plot da nota por turno e região")+
  xlab("Turno") +
  ylab("Notas") +
  facet_grid(~CO_REGIAO_CURSO)+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))


ggplotly(grafico_boxplot2)



# Acima, o grafico de boxplot, mostrando que os BOXS(caixas) pra quem estuda em tempo INTEGRAL, são 
# superiores aos outros turnos. O que deixa mais claro que os alunos que estudam em tempo integral,
# tem um melhor desempenho quanto aos outros alunos.


# Grafico histograma das notas por cor
grafico_histograma1 = ggplot(dados_mat, aes(x=NT_OBJ_FG, fill=QE_I02)) + 
  geom_histogram(bins=30)+
  ggtitle("Gráfico histograma da Nota por Cor" )+
  xlab("Notas") +
  ylab("Frequência simples") +
  facet_grid(~QE_I02)

ggplotly(grafico_histograma1)


# Olhando para o histograma acima, é facil observar o quanto a cor branca se
# destaca entre as outras e isso se dar por vários fatores, como: 
# 1. Ter acesso à educação de qualidade
# 2. Ter estrutura familiar estável
# 3. Ter acesso à cuidados de saúde de qualidade
# 4. Ter estudado no ensino fundamental e médio em instituições privadas ou em instituições públicas de referência


# Gráfico histograma da Nota por região

grafico_histograma2 = ggplot(dados_mat, aes(x=NT_OBJ_FG, fill=CO_REGIAO_CURSO)) + 
  geom_histogram(bins=30)+
  ggtitle("Gráfico histograma da Nota por Região" )+
  xlab("Notas") +
  ylab("Frequência simples") +
  facet_grid(~CO_REGIAO_CURSO)

ggplotly(grafico_histograma2)





# Gráfico de pizza, mostrando as proporções de notas por região
grafico_pizza <- plot_ly(dados_mat, labels = ~CO_REGIAO_CURSO, values = ~NT_OBJ_FG, type = 'pie')
grafico_pizza <- grafico_pizza %>% layout(title = 'Proporção, gráfico de pizza',
                      xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
                      yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

grafico_pizza





#Consolidando graficos 
grid.arrange( grafico_histograma1,
              grafico_histograma2,
              grafico_boxplot1,
              grafico_boxplot2,
              nrow=2,ncol=2)



# Gráfico acima, mostra o histograma das notas por região. Nele, podemos observar,
# que a região sudeste ela é superior em relação as demais regiões.
# De acordo com o inep(Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira), os indices de educação, principalmente dos alunos no ensino fundamental e médio,
# localizam-se nos mais baixos patamares. Eles não conseguem transpor o que é solicitado no enunicado
# de uma questão para uma linguagem matematica. Apesar de elevados, os indices na região sudeste, é bem menor 
# comparado a media nacional. Como mostrado no histograma acima.


#REFERENCIAS 
# https://simaigualdaderacial.com.br/site/o-que-e-privilegio-branco-entenda/
# http://inep.gov.br/en/artigo/-/asset_publisher/B4AQV9zFY7Bv/content/desempenho-escolar-de-estudantes-da-regiao-sudeste-e-tema-de-seminario/21206
# https://plotly.com/r/box-plots/
# https://support.minitab.com/pt-br/minitab/20/help-and-how-to/statistics/basic-statistics/supporting-topics/data-concepts/how-skewness-and-kurtosis-affect-your-distribution/#:~:text=Uma%20distribui%C3%A7%C3%A3o%20com%20um%20valor%20de%20curtose%20negativa%20indica%20que,um%20valor%20de%20curtose%20negativo.
