# Desarrollo con MongoDB

Partimos del caso en el que tenemos la máquina virtual ejecutando una instancia de mongod en standalone en el puerto 27017. Si no hemos completado las prácticas anteriores podemos partir de la instantánea "5 - Estado final" (del entorno correspondiente).

Además, la instancia debería tener cargadas las tres colecciones de pokemon, estudiantes y zips. Podemos comprobando conectándonos a la misma.

#### 1 - Instalamos el intérprete de Python 3

Comprobamos que tenemos acceso a Internet, y ejecutamos:
```bash
yum install -y python3
```

Cuando termine, comprobamos que podemos abrir una consola interactiva de python ejecutando el comando ```python3```. Salimos de la consola con el comando ```quit()```.

#### 2 - Instalamos PyMongo

Desde el bash de Linux (la línea de comandos del sistema operativo), ejecutamos:

```bash
python3 -m pip install pymongo
```

Comprobamos que la instalación ha funcionado abriendo otra consola de Python. Una vez que la hayamos abierto, ejecutamos ```import pymongo```. Si no devuelve nada, es que todo ha ido bien ("no news is good news"). Si no está instalado, devolverá un error de tipo "ModuleNotFoundError".

---

# Ejercicios con PyMongo

#### 1 - Modifica el archivo "pymongo_driver.py" para que se conecte a la base de datos local.

El archivo está en el directorio correspondiente a la práctica 5. Puedes leer el código en esta misma web de GitHub, incluye resaltado de sintaxis y facilita la lectura. El objetivo de este ejercicio es darle un valor a la variable MONGODB_URI, de forma que cuando ejecutemos el script se conecte a la base de datos y lea bien los datos correspondientes.

Para probar el script cuando lo hayamos modificado, nos situamos en el directorio donde está el script y ejecutamos:

```bash
python3 pymongo_driver.py
```

<details>
<summary>Ver solución</summary>
<p>

Cualquiera de estas opciones:

```python
MONGODB_URI="localhost"
MONGODB_URI="127.0.0.1"
MONGODB_URI="127.0.0.1:27017"
MONGODB_URI="localhost:27017"
MONGODB_URI="mongodb://localhost"
MONGODB_URI="mongodb://127.0.0.1"
MONGODB_URI="mongodb://localhost:27017"
MONGODB_URI="mongodb://127.0.0.1:27017"
```

También funcionaría si nos conectamos a una base de datos específica dentro de la instancia, por ejemplo:
```python
MONGODB_URI="mongodb://localhost/students"
```

Esto es porque el ya se posiciona por sí mismo en la base de datos correcta con la línea:
```python
db = client.pokemon
```
Equivalente al ```use pokemon``` de la shell de Mongo.

</p>
</details>  

#### 2 - Escribir un script en Python que revierta el nombre en la base de datos de todos los pokemon de tipo planta ("Grass")
Nos basaremos en "pymongo_plantilla.py", hay que aplicar los tres cambios que se indican en el código.

Como ayuda, una manera de revertir un string en Python es usando lo que se llama el [string slicing](https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/):

```python
palabra = "casa"
palabra_al_reves = palabra[::-1]
print(palabra_al_reves)
```

Imprimirá:

```bash
asac
```

<details>
<summary>Ver solución</summary>
<p>

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost")
db = client.pokemon

# MODIFICAR ESTA CONSULTA
cursor = db.pokemon.find({"type": "Grass"})

for elemento in cursor:
    original_name = elemento["name"]

    # ASIGNAR A ESTE CAMPO EL NOMBRE ORIGINAL AL REVES
    elemento["name"] = original_name[::-1]

    # ESCRIBIR LA CONSULTA QUE REEMPLAZA EL DOCUMENTO QUE TENIA EL NOMBRE ORIGINAL
    db.pokemon.replace_one({"name": original_name},elemento)

```
</p>
</details>  

---

# ODM
Vamos a usar MongoEngine como ODM para esta práctica. Para ello, lo primero es instalarlo:

Desde el bash de Linux (la línea de comandos del sistema operativo), ejecutamos:

```bash
python3 -m pip install mongoengine
```

Comprobamos que la instalación ha funcionado abriendo una consola de python y ejecutando ```import mongoengine```. Si no devuelve nada, es que todo ha ido bien ("no news is good news"). Si no está instalado, devolverá un error de tipo "ModuleNotFoundError".

# Ejercicios con ODM

#### 1. Leer el código del script "mongoengine_sencillo.py". ¿Qué va a ocurrir en la Mongo cuando se ejecute?

<details>
<summary>Ver respuesta</summary>
<p>

Se creará la base de datos "vehiculos" y la colección "coches", y se insertará en ella un Renault Megane con año de año_fabricación y matrícula calculados al azar.

</p>
</details>  

#### 2. Revisando la [documentación de referencia de MongoEngine](http://docs.mongoengine.org/apireference.html#mongoengine.fields.StringField), limitar la longitud de la marca para que no acepte más de 10 caracteres.

<details>
<summary>Ver respuesta</summary>
<p>

```python
marca = StringField(max_length=10, required = True)
```

</p>
</details>  

#### 3. Modificar el script para intentar crear un coche con una marca de más de 10 caracteres, ¿qué ocurre? ¿cómo debería gestionar este problema en una aplicación real?

<details>
<summary>Ver respuesta</summary>
<p>

El script falla con "ValidationError", indicando que el valor es demasiado largo.

Para tratar este problema en una aplicación real, debería añadir control de excepciones a mi aplicación y definir un comportamiento en caso de encontrar este fallo (devolverle algún error amigable al usuario, por ejemplo).

</p>
</details>

#### 4. Modificar el script para añadir un método que imprima por pantalla cuántos años tiene el coche.

Ayuda: Para obtener el año actual en Python, usaremos el módulo ```datetime```. Hay que incluir la importación correspondiente al inicio del script:
```python
import datetime
```
Y sacar el año como número entero cuando lo necesitemos con:
```python
año = datetime.datetime.now().year
```
<details>
<summary>Ver solución</summary>
<p>
```python
from mongoengine import *
import random
import datetime

class Coche(Document):
    marca = StringField(required = True)
    modelo = StringField(required = True)
    año_fabricacion = IntField(required = True)
    matricula = StringField(required = True)
    meta = { "collection": "coches"}

    def imprimir_edad(self):
        print(datetime.datetime.now().year - self.año_fabricacion)

connect(host="mongodb://localhost/vehiculos")

mi_coche = Coche(marca = "Renaultsdfsdfsdfsdfe3rw",
    modelo = "Megane",
    año_fabricacion = random.randrange(1990,2019),
    matricula = str(random.randrange(0000,9999))+"-ABC" )

mi_coche.imprimir_edad()

mi_coche.save()
```
</p>
</details>

#### 5. Ejecutar el script y comprobar si en la Mongo se ha guardado el código del método que acabamos de crear.
<details>
<summary>Ver respuesta</summary>
<p>

En la Mongo no se guarda el método. El motivo es el fundamento de la programación orientada a objetos: la clase ("class") define todas las características comunes a todos los objetos de tipo "Coche", se puede ver como una plantilla. Una de esas características es el método "imprimir_edad", que tienen todos los coches y es igual para todos ellos.

En la base de datos se guardará únicamente aquella información que sea específica de cada coche en concreto. La información de los métodos reside en el código de la aplicación. Lo mismo ocurre con las variables de clase, un tipo de variable que no aparece en estos ejemplos pero que estaría asociada a la plantilla y no a un coche específico.

</p>
</details>

#### 6. En "mongoengine_embed.py" está definido el modelo que hemos utilizado en nuestra colección de ejemplo de estudiantes. Modificar el script para que ahora cada estudiante tenga que tener un array de objetos llamado "emails". Cada objeto de este array contendrá obligatoriamente una dirección de correo en el campo "emailAddress" y un tipo en el campo "type" (personal, profesional, temporal...) Además, se debe pasar a utilizar la colección "students2" dentro de la misma base de datos.

Será necesario recurrir a la [documentación sobre definición de documentos](http://docs.mongoengine.org/guide/defining-documents.html) de MongoEngine para encontrar cómo definir un campo de tipo email.

<details>
<summary>Ver solución</summary>
<p>

```python
from mongoengine import *

class Score(EmbeddedDocument):
    score = FloatField(required = True)
    type = StringField(required = True)

class Email(EmbeddedDocument):
    emailAddress = EmailField(required = True)
    type = StringField(required = True)

class Student(Document):
    name = StringField(required = True)
    age = IntField(required = True)
    nationality = StringField(required = True)
    scores = ListField(EmbeddedDocumentField(Score))
    emails = ListField(EmbeddedDocumentField(Email), required = True)
    meta = { "collection": "students2"}

    def print_info(self):
        print("Name: " + self.name)
        print("Age: " + str(self.age))
        print("Nationality: " + self.nationality)
        print("Scores: ")
        for elem in self.scores:
            print(" " * 4 + elem.type + " " + str(elem.score))


if __name__ == "__main__":

    MONGO_STUDENTS_DB_URI="mongodb://localhost/students"

    connect(host=MONGO_STUDENTS_DB_URI)

    pierre_score_exam = Score(type = "exam", score = 7.35)
    pierre_score_homework = Score(type = "homework", score = 40.81)
    pierre_personal_email = Email(type = "personal", emailAddress = "pierre@example.net")
    pierre_professional_email = Email(type = "professional", emailAddress = "pierre@work.com")
    pierre = Student(name = "Pierre",
        age = 32,
        nationality = "french",
        scores = [ pierre_score_exam,pierre_score_homework ],
        emails = [ pierre_personal_email, pierre_professional_email ] )
    pierre.print_info()

    # Guardo el objeto en la Mongo
    pierre.save()

    # Consulto el primer resultado filtrando por nombre.
    # El resultado ya es una instancia de la clase Student (un objeto)
    pierre_from_database = Student.objects(name = "Pierre")[0]
    print("Informacion recuperada de la base de datos: ")
    pierre_from_database.print_info()

```

El documento guardado en base de datos será este:

```js
{
        "_id" : ObjectId("5d8a88755da60e1b7a1f93de"),
        "name" : "Pierre",
        "age" : 32,
        "nationality" : "french",
        "scores" : [
                {
                        "score" : 7.35,
                        "type" : "exam"
                },
                {
                        "score" : 40.81,
                        "type" : "homework"
                }
        ],
        "emails" : [
                {
                        "emailAddress" : "pierre@example.net",
                        "type" : "personal"
                },
                {
                        "emailAddress" : "pierre@work.com",
                        "type" : "professional"
                }
        ]
}
```

</p>
</details>
