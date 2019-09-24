from mongoengine import *
import random

class Coche(Document):
    marca = StringField(required = True)
    modelo = StringField(required = True)
    año_fabricacion = IntField(required = True)
    matricula = StringField(required = True)
    meta = { "collection": "coches"}

connect(host="mongodb://localhost/vehiculos")

mi_coche = Coche(marca = "Renault",
    modelo = "Megane",
    año_fabricacion = random.randrange(1990,2019),
    matricula = str(random.randrange(0000,9999))+"-ABC" )

mi_coche.save()
