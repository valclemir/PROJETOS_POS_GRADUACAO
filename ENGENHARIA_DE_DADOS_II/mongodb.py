import pandas as pd 
from pymongo import MongoClient


c = MongoClient("mongodb://192.168.1.64")
db = c['bigdata']

covid = db['covid']
filtro = {"location": "Brazil"}
lista = []


for doc in covid.find(filtro):
    dados = {}
    dados['populacao'] = doc['population']
    dados['populacao_total_vacinada'] = doc['people_fully_vaccinated']
    dados['date'] = doc['date']
    lista.append(dados)
df = pd.DataFrame(lista)
df = df.sort_values('date')

people_fully_vaccinated = []
for i in df['populacao_total_vacinada']: 
    if i == '':
        i = 0
    else:
        i = i.split('.')[0]

    people_fully_vaccinated.append(int(i))
df['populacao_total_vacinada'] = people_fully_vaccinated


population = []
for i in df['populacao']: 
    i = i.split('.')[0]

    population.append(int(i))
df['populacao'] = population