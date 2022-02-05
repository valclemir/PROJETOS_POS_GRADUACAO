#!/usr/bin/env python
# coding: utf-8

from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt

#cliente = MongoClient('mongodb://192.168.100.113:27017')
cliente = MongoClient('mongodb://192.168.1.65:27017')
filter={
    'location': 'Brazil'
}

resultado = cliente['bigdata']['covid'].find(
  filter=filter
)    

# salvando consulta banco 
df_inicial = pd.DataFrame(resultado)

print (df_inicial)

col = ['location','population','people_fully_vaccinated','date']

print (col)

df_inicial = df_inicial[col]

## tratando valores em branco e zerados
df_inicial['people_fully_vaccinated'].replace('', np.nan, inplace=True)
df_inicial['people_fully_vaccinated'].replace('0.0', np.nan, inplace=True)
df_inicial.dropna(subset=['people_fully_vaccinated'], inplace=True)


#data base
data_base = pd.to_datetime(df_inicial['date'].min())
#vetor de dias
df_inicial = df_inicial.assign(dias = pd.to_datetime(df_inicial['date']) - data_base)
df_inicial = df_inicial.assign(vacinados = pd.to_numeric(df_inicial['people_fully_vaccinated']))

# primeiro dia de ocorrencia de imunização completa
print('A primeira imunização completa no Brasil ocorreu em:',data_base)

# gerando a coluna com dias de vacinação
df_inicial = df_inicial.assign(dias = pd.to_datetime(df_inicial['date']) - data_base)
df_inicial = df_inicial.assign(vacinados = pd.to_numeric(df_inicial['people_fully_vaccinated']))

# convertendo tipos de dados
df_inicial['dias'] = df_inicial['dias'] / np.timedelta64(1, 'D')
df_inicial['dias'] = df_inicial['dias'].astype(int)
df_inicial['vacinados'] = df_inicial['vacinados'].astype(int)


## Utilizando regressão linear para previsão dos dados.
lin_reg=LinearRegression()
x = pd.DataFrame(df_inicial['dias'])
y = pd.DataFrame(df_inicial['vacinados'])

# transformando colunas do dataframe em array numpy
x = x.iloc[:, 0].values.reshape(-1, 1)  
y = y.iloc[:, 0].values.reshape(-1, 1) 

# calculando o score do modelo utilizado
reg = LinearRegression().fit(x,y) # treinando modelo com os dados historicos
print('O valor de score do modelo é = ',reg.score(x,y)) # verificando o score do modelo

y_pred = reg.predict(x) 
"""
# verificando RMSE
rmse = sqrt(mean_squared_error(y, y_pred))
print ('RMSE = ',rmse)

mse = mean_squared_error(y, y_pred)
print('MSE = ', mse)
"""

# visualizando dados reais x previsões (scatter plot)
plt.scatter(x, y)
plt.plot(x, y_pred, color='red')
plt.title('Regressão linear - Real x Previsto')
plt.ylabel('Número de vacinados')
plt.xlabel('Dias de vacinação')
plt.show()



## dados reais + predições 
dias_previsao = 0
taxa_vacinados = 0
populacao = pd.to_numeric(df_inicial['population'].max())
df_final = pd.DataFrame()
dias_max = pd.to_numeric(df_inicial['dias'].max())

while taxa_vacinados < 100:
    quantidade_vacinados = round(reg.predict([[dias_previsao]])[0][0])
    taxa_vacinados = (quantidade_vacinados / populacao)*100
    if dias_previsao in df_inicial['dias'].values:
        dias_vacina = df_inicial['dias'][df_inicial.dias == dias_previsao].values[0]
        perc_vacinados = pd.to_numeric(df_inicial['vacinados']).astype(int)[df_inicial.dias == dias_previsao].values[0] / pd.to_numeric(df_inicial['population']).astype(int)[df_inicial.dias == dias_previsao].values[0]
        qtd_vacinados = pd.to_numeric(df_inicial['vacinados']).astype(int)[df_inicial.dias == dias_previsao].values[0]   
        
        df_final = df_final.append({'dias_vacina':dias_vacina,
                                      'perc_vacinados':round(perc_vacinados,2)*100,
                                      'perc_vacinados_proj':round(taxa_vacinados,2),
                                      'qtd_vacinados':qtd_vacinados,
                                      'qtd_vacinados_proj':quantidade_vacinados},ignore_index = True)


    else:
        df_final = df_final.append({'dias_vacina':dias_previsao,
                                      'perc_vacinados_proj':round(taxa_vacinados,2),                                      
                                      'qtd_vacinados_proj':quantidade_vacinados},ignore_index = True)        
    dias_previsao += 1            




dia_43 = df_final['dias_vacina'][df_final['perc_vacinados_proj']>=43].astype(int).min()

print('No dia', dia_43, ',expectativa de atingir 43% vacinados.')



dia_60 = df_final['dias_vacina'][df_final['perc_vacinados_proj']>=60].astype(int).min()
print('No dia', dia_60, ',expectativa de atingir 60% vacinados.')



dia_100= df_final['dias_vacina'][df_final['perc_vacinados_proj']>=100].values[0].astype(int)
print('No dia', dia_100, ',expectativa de atingir 100% vacinados.')



# Visualizando resumo dos dados reais x previstos
plt.plot(df_final['dias_vacina'],df_final['perc_vacinados'],color='red', linestyle='solid',linewidth=4,label='Real')
plt.plot(df_final['dias_vacina'],df_final['perc_vacinados_proj'],color='blue', linestyle='dashdot',lw=2,label='Previsto')

plt.legend(fontsize=10)
plt.xlabel('Dias',fontsize=10)
plt.ylabel('Percentual de vacinados',fontsize=10)
plt.show()

