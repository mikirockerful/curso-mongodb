from pymongo import MongoClient

client = MongoClient("mongodb://localhost")
db = client.pokemon

# MODIFICAR ESTA CONSULTA
cursor = db.pokemon.find()

for elemento in cursor:
    original_name = elemento["name"]

    # ASIGNAR A ESTE CAMPO EL NOMBRE ORIGINAL AL REVES
    elemento["name"] =

    # ESCRIBIR LA CONSULTA QUE REEMPLAZA EL DOCUMENTO QUE TENIA EL NOMBRE ORIGINAL POR EL NUEVO
    db.pokemon.replace_one()
