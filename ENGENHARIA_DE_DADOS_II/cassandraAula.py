from cassandra.cluster import Cluster

cluster = Cluster(['bigdata-1'],port=9042)
session = cluster.connect()
rows = session.execute('SELECT * FROM bigdata.images')
for row in rows:
    print(row.tags)