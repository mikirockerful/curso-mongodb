from pymongo import MongoClient

# Completar como corresponda
MONGODB_URI=""

client = MongoClient(MONGODB_URI)
db = client.pokemon
print(db.pokemon.count_documents({"type": "Grass"}))
cursor = db.pokemon.find({"type": "Grass"})
while True:
    try:
        elemento = cursor.next()
    except StopIteration:
        break
    print("Nombre: " + elemento["name"])
cursor.rewind()
for elemento in cursor:
    print("Id: " + str(elemento["_id"]))
