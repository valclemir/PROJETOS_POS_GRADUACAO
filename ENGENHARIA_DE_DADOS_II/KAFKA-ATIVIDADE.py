import json
import random
import threading
import time

from kafka import KafkaConsumer, KafkaProducer


class Producer(threading.Thread):
    IP = '192.168.1.65'
    PORT = '9092'
    def run(self):
        producer = KafkaProducer(bootstrap_servers=self.IP+':'+self.PORT, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        while True:
            data = {}
            id_ = random.randint(0, 1000)

            if data.__contains__(id(id_)):
                message = data.get(id_)
            else:
                streaming = {'idade': random.randint(10, 50), 'altura': random.randint(100, 200),
                            'peso': random.randint(30, 100)}
                message = [id_, streaming]
                data[id_] = message

            producer.send('topic', message)
            # REDUZIDO PARA 2 SEGUNDOS
            time.sleep(random.randint(0, 2)) # 3. Aumente a frequência de geracao das tuplas (Geracao mais rápida)


class Consumer(threading.Thread):
    IP = '192.168.1.65'
    PORT = '9092'

    def run(self):
        stream = KafkaConsumer(bootstrap_servers=self.IP+':'+self.PORT)
        stream.subscribe(['topic'])
        for tuple in stream:
            
            # 5. Filtre e imprima apenas por tuplas que possuem valores de IMC acima de 35 (IMC = peso / alture ** 2

            # 4. Filtre e imprima apenas por tuplas que possuem valores de peso maiores que 80
            peso = json.loads(tuple.value.decode('utf-8'))[1]['peso']
            altura = json.loads(tuple.value.decode('utf-8'))[1]['altura']
            imc = peso / altura ** 2

            conteudo = json.loads(tuple.value.decode('utf-8'))[1]
            print({"CONTEUDO TUPLA": conteudo})


            if peso > 80:
               print("\nRESPOSTA QUESTAO 4: PESO "+str(peso)+"\n")

            if imc > 35:
                print("\nRESPOSTA QUESTAO 5: IMC " +str(imc)+"\n")



if __name__ == '__main__':
    threads = [
        Producer(),
        # 2. Gere dados de quatro producers simultaneos
        # R. Descomentar os Proceducer abaixo
        Producer(),
        Producer(),
        Producer(),
        Consumer()
    ]

    for t in threads:
        t.start()