from pymongo import MongoClient
c = MongoClient("mongodb://192.168.1.64", 27017)
db = c['bigdata']

col = db['gastos']

for doc in col.find_one():
    print(doc)