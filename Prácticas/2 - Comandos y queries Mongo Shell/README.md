# Comandos y queries Mongo Shell

## Importando algunos datos

Lo primero que vamos a hacer es cargar algunos datos en nuestra base de datos. Los datos de muestra los podemos encontrar en el directorio ```/root/curso-mongodb/Datos```.

En este directorio hay 3 conjuntos de datos:

* **students**: Contiene datos de estudiantes y sus notas
* **zips**: Datos de códigos postales, ciudades y estados de Estados Unidos
* **samples_pokemon**: La pokédex de los primeros juegos de Pokémon

Podemos ver que algunos de ellos están en formato BSON (con su correspondiente fichero de metadatos) y otros en formato JSON. Empezaremos importando la colección de zips, en formato JSON.

Para importaciones y exportaciones en formato JSON, MongoDB incluye las herramientas ```mongoimport``` y ```mongoexport```. Importaremos la colección sobre nuestra instancia de MongoDB, en una nueva base de datos llamada **zips** y en una nueva colección dentro de esa base de datos también llamada **zips**:
```
mongoimport --db zips --collection zips --file /root/curso-mongodb/Datos/zips.json
```
De nuevo, no especificamos a qué base de datos hay que conectarse, por lo que tomará por defecto la instancia local en el puerto 27017.

**¿Cuántos documentos se han insertado en la base de datos?**

Mongoimport y mongoexport trabajan con datos en formato JSON, en lugar de BSON. La ventaja es que los ficheros generados son directamente legibles por humanos, lo que podemos comprobar lanzando un ```head /root/curso-mongodb/Datos/zips.json```. La principal desventaja es que hay algunos tipos de datos soportados por BSON que no están especificados en JSON, por lo que nunca se deben usar mongoimport / mongoexport en producción.

La alternativa son los comandos mongodump y mongorestore, que son equivalentes pero generan la salida en BSON. Normalmente generan dos ficheros, el de los datos propiamente dichos y otro fichero de metadatos que contiene, entre otras cosas, los índices, que deben recrearse al ejecutar ```mongorestore```.

Usando estas herramientas, importamos los datos de estudiantes y pokemon. De nuevo, para cada archivo crearemos una base de datos y una colección nueva:
```
mongorestore --db students --collection students students.bson
mongorestore --db pokemon --collection pokemon samples_pokemon.bson
```

**¿Cuántos documentos se han insertado en la base de datos en cada caso?**

## Primeros pasos con la shell

Abrimos una shell con el comando ```mongo```.

A partir de aquí, la mayoría de los comandos tienen la forma de funciones JavaScript (acabados en paréntesis). Sin embargo, existen unos pocos comandos con alias, llamados "helpers". Usemos algunos de ellos para descubrir qué tenemos en la instancia.

Listamos las bases de datos disponibles:
```
show dbs
```
Las bases de datos ```admin```, ```config``` y ```local``` son propias del sistema y se crean automáticamente. El resto deben ser las que hemos creado.
Nos posicionamos en cualquiera de las que hemos creado:
```
use <nombre_db>
```

Y listamos las colecciones de dicha base de datos:
```
show collections
```

Si no aparece nada, es posible que nos hayamos posicionado en una base de datos que no existe (por un error al teclear). Es importante tener en cuenta esto, la shell de MongoDB es muy permisiva, y, si en ese caso decidiésemos insertar un documento en una colección, crearíamos tanto la base de datos como la colección en ese momento. Hay que tener especial cuidado con este tipo de errores en la shell de MongoDB.

**Ayuda**: Para limpiar la pantalla de la shell de Mongo, podemos usar el comando ```cls``` (clear screen)

## CRUD: Create, Read, Update, Delete
Vamos a aprender a manipular los datos. Se plantean una serie de preguntas, es importante intentar resolverlas antes de ver la respuesta.

Empezaremos con los datos de los estudiantes. Desde la shell de Mongo:

```
use students
```

El primer paso es tener claro el esquema de los documentos. Saquemos uno como ejemplo:
```
db.students.findOne()
```

```js
{
        "_id" : 0,
        "name" : "aimee Zank",
        "scores" : [
                {
                        "score" : 1.463179736705023,
                        "type" : "exam"
                },
                {
                        "score" : 11.78273309957772,
                        "type" : "quiz"
                },
                {
                        "score" : 35.8740349954354,
                        "type" : "homework"
                }
        ],
        "age" : 17,
        "nationality" : "american"
}
```

Los campos "\_id" y "age" son numéricos, "name" y "nationality" son strings y el campo "scores" es un array de objetos.

A continuación se plantean una serie de ejercicios, el objetivo es escribir una consulta que permita obtener lo que se pide. Es importante al menos intentar crear la consulta antes de ver el resultado de cada pregunta.

### Read: Leer documentos

#### 1. Obtener todos los documentos de la colección de estudiantes
<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find()
```

O bien:

```js
db.students.find({})
```

</p>
</details>  

#### 2. Obtener todos los estudiantes de más de 20 años

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({age: {$gt: 20}})
```

</p>
</details>  

#### 3. Obtener todos los estudiantes de 20 años o más

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({age: {$gte: 20}})
```

</p>
</details>  

#### 4. Obtener todos los estudiantes entre 20 y 25 años

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  age: {
    $gte: 20,
    $lte: 25
  }
})
```

O bien:

```js
db.students.find({
  $and: [{
    age: {
      $gte: 20
    }
  }, {
    age: {
      $lte: 25
    }
  }]
})
```

</p>
</details>  

#### 5. Contar el número de estudiantes entre 20 y 25 años

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  age: {
    $gte: 20,
    $lte: 25
  }
}).count()
```

</p>
</details>  



#### 6. Para los estudiantes entre 20 y 25 años, sacar sólo los campos nombre y nacionalidad de cada uno de ellos

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  age: {
    $gte: 20,
    $lte: 25
  }
}, {
  _id: 0,
  name: 1,
  nationality: 1
})
```

</p>
</details>  

#### 7. Obtener todos los estudiantes ordenados por edad en sentido ascendente

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find().sort({
  age: 1
})
```

</p>
</details>  

#### 8. Obtener todos los estudiantes ordenados por edad en sentido descendente

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find().sort({
  age: -1
})
```

</p>
</details>

#### 9. Obtener los 10 estudiantes de mayor edad

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find().sort({
  age: -1
}).limit(10)
```

</p>
</details>

#### 10. Obtener los segundos 20 estudiantes de mayor edad (saltándose los 20 primeros)

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find().sort({
  age: -1
}).skip(20).limit(20)
```

</p>
</details>


#### 11. Obtener los estudiantes que sacaron más de 70 puntos en el examen
**Nota**: No se puede confiar en que las calificaciones aparezcan siempre en el mismo orden en el array "scores". Es decir, el examen no tiene por qué ir en primer lugar.

<details>
<summary>Ver pista</summary>
<p>
El operador [$elemMatch](https://docs.mongodb.com/manual/reference/operator/query/elemMatch/) hace match con los documentos que contienen un campo array con al menos un elemento que cumpla con todos los criterios especificados.
</p>
</details>

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  scores: {
    $elemMatch: {
      type: "exam",
      score: {
        $gt: 70
      }
    }
  }
})
```

</p>
</details>

#### 12. Obtener los estudiantes que sacaron más de 30 puntos en la calificación que aparezca en primer lugar en el array scores (sea la que sea)

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  "scores.0.score": {
    $gt: 30
  }
})
```

Recordar que para utilizar la notación con el punto, es obligatorio utilizar comillas para la clave.

</p>
</details>

#### 13. Obtener los estudiantes que sacaron más de 70 puntos en el examen y más de 50 en la tarea ("homework")

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  $and: [{
    scores: {
      $elemMatch: {
        type: "exam",
        score: {
          $gt: 70
        }
      }
    }
  }, {
    scores: {
      $elemMatch: {
        type: "homework",
        score: {
          $gt: 50
        }
      }
    }
  }]
})
```

</p>
</details>

#### 14. Obtener los estudiantes que cumplen con cualquiera de las siguientes afirmaciones:
* Sacaron más de 70 puntos en el examen y más de 50 en la tarea ("homework")
* Son franceses

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  $or: [{
    $and: [{
      scores: {
        $elemMatch: {
          type: "exam",
          score: {
            $gt: 70
          }
        }
      }
    }, {
      scores: {
        $elemMatch: {
          type: "homework",
          score: {
            $gt: 50
          }
        }
      }
    }]
  }, {
    nationality: "french"
  }]
})
```

</p>
</details>

#### 15. Obtener los estudiantes que no entregaron la tarea

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  "scores": {
    $not: {
      $elemMatch: {
        type: "exam"
      }
    }
  }
})
```

No hay ninguno, con lo que es difícil comprobar si la query está bien. Podemos probar a insertar un estudiante sin examen, y comprobar la consulta. Por ejemplo:

```js
db.students.insert({
  "_id": 300,
  "name": "Maren Scheider",
  "scores": [{
    "score": 77.28263690107663,
    "type": "quiz"
  }, {
    "score": 59.46326216544371,
    "type": "homework"
  }],
  "age": 19,
  "nationality": "english"
})
```
Y veremos que este resultado se devuelve correctamente.

Otra alternativa correcta para la query sería esta:
```js
db.students.find({
  "scores.type": {$ne: "exam"}
  })
```
Que se basa en buscar dentro de un campo embebido en un array de documentos sin conocer el índice del documento que buscamos. Esta forma de búsqueda está descrita [aquí](https://docs.mongodb.com/manual/tutorial/query-array-of-documents/#specify-a-query-condition-on-a-field-embedded-in-an-array-of-documents)

</p>
</details>

#### 16. Obtener los estudiantes que sean de alguna de estas nacionalidades: ["german", "italian", "french"]

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  "nationality": {
    $in: ["german", "italian", "french"]
  }
})
```

</p>
</details>

#### 17. Obtener los estudiantes que no sean de ninguna de estas nacionalidades: ["german", "italian", "french"]

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  "nationality": {
    $nin: ["german", "italian", "french"]
  }
})
```

</p>
</details>

#### 18. Comprobar si hay algún estudiante cuyo campo "\_id" no sea de tipo "number"

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  "_id": {
    $not: {
      $type: "number"
    }
  }
})
```

De nuevo, la respuesta es cero así que es difícil de probar. Vamos a introducir un documento sin campo "\_id" para que Mongo le cree automáticamente el campo de tipo ObjectId y así poder comprobar la consulta:

```js
db.students.insert({
  name: "prueba"
})
```

Veremos que la consulta nos devuelve este documento.

</p>
</details>

#### 19. Comprobar si hay algún estudiante que no tenga el campo "age"

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  "age": {
      $exists: false
    }
})
```

No hay ninguno en la colección original, podemos volver a utilizar el documento de prueba.

</p>
</details>

#### 20. Obtener los estudiantes cuya edad sea múltiplo de 5

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  age: {
    $mod: [5, 0]
  }
})
```

</p>
</details>

#### 21. Obtener los estudiantes que no tienen exactamente tres entregas en el array "scores"

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  scores: {
    $not: {
      $size: 3
    }
  }
})
```

No hay ninguno en la colección original, podemos volver a utilizar el documento de prueba.


</p>
</details>



#### 22. Obtener los estudiantes cuyo nombre tenga 5 letras y su apellido también.
<details>
<summary>Ver pista</summary>
<p>
Ayuda: La expresión regular para un string que empieza con una palabra de 5 caracteres seguida de otra palabra de 5 caracteres es: /^[A-Za-z]{5} [A-Za-z]{5}/
</p>
</details>

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  name: {$regex: /^[A-Za-z]{5} [A-Za-z]{5}/}
})
```

</p>
</details>

#### 23. Sacar en mayúsculas el nombre y apellidos de los estudiantes que cumplan con las mismas condiciones que en la pregunta anterior. Los documentos resultado no deben tener ningún campo más.

<details>
<summary>Ver pista</summary>
<p>
No hay ninguna función en el lenguaje de consultas CRUD de MongoDB para transformar los resultados. La solución requiere usar la función toUpperCase() de JavaScript. Ejemplo de uso:

```js
"alphabet".toUpperCase() //"ALPHABET"
```

**Nota**: Existe un toUpper(), pero pertenece al framework de agregación que veremos más adelante.

</p>
</details>

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.find({
  name: {
    $regex: /^[A-Za-z]{5} [A-Za-z]{5}/
  }
}).forEach(function(myDoc) {
  print(myDoc.name.toUpperCase())
})
```

</p>
</details>


Si hemos insertado el documento de prueba, lo borramos para continuar con las prácticas:

```js
db.students.remove({
 name: "prueba"
})
```

### Create: Crear documentos

#### 1. Insertar un nuevo estudiante en la colección

Insertaremos este estudiante:

```js
{
  "_id": 300,
  "name": "Arthur Dent",
  "scores": [{
      "score": 62.20457822364115,
      "type": "exam"
    },
    {
      "score": 61.03733414415722,
      "type": "quiz"
    },
    {
      "score": 82.41688205392703,
      "type": "homework"
    }
  ],
  "age": 38,
  "nationality": "english"
}
```

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.insert({
  "_id": 300,
  "name": "Arthur Dent",
  "scores": [{
      "score": 62.20457822364115,
      "type": "exam"
    },
    {
      "score": 61.03733414415722,
      "type": "quiz"
    },
    {
      "score": 82.41688205392703,
      "type": "homework"
    }
  ],
  "age": 38,
  "nationality": "english"
})
```

</p>
</details>

### Delete: Borrar documentos

#### 1. Borrar todos los documentos correspondientes a estudiantes españoles

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.remove({
  "nationality": "spanish"
})
```
Podemos hacer un "find" para verificar que se han borrado.

</p>
</details>

Por defecto, remove() borra todos los documentos que cumplen la condición. Si no le ponemos condiciones, **borraremos todos los documentos de la colección**. Se haría así: ```db.students.remove({})```

Recuerda que las operaciones no son reversibles, no existen los conceptos de "commit" y "rollback" en la shell de MongoDB.


#### 2. Borrar un único documento (cualquiera) con una nota en el examen menor de 50

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.remove({
  scores: {
    $elemMatch: {
      type: "exam",
      score: {
        $lt: 50
      }
    }
  }
}, {
  justOne: true
})
```

</p>
</details>

### Update: Actualizar documentos

#### 1. Cambiar el nombre de "Gennie Ratner" a "Gennie Smith"

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.update({
  name: "Gennie Ratner"
}, {
  "$set": {
    name: "Gennie Smith"
  }
})
```

</p>
</details>

#### 2. Incrementar la edad de "Lucinda Vanderburg" en 1 año

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.update({
  name: "Lucinda Vanderburg"
}, {
  "$inc": {
    age: 1
  }
})
```

</p>
</details>

#### 3. Cambiar la nacionalidad de todos los italianos para que pasen a ser belgas ("belgian")

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.update({
  nationality: "italian"
  }, {
  "$set": {
    nationality: "belgian"
    }
  }, {
  multi: true
})
```

</p>
</details>

#### 4. Cambiar el documento de "Flora Duell" por este otro
```js
{
        "_id" : 109,
        "name" : "Flora Duell",
        "scores" : [
                {
                        "score" : 60.68238966626067,
                        "type" : "exam"
                },
                {
                        "score" : 32.77972040308903,
                        "type" : "quiz"
                },
                {
                        "score" : 85.732755740408484,
                        "type" : "homework"
                }
        ],
        "age" : 19,
        "nationality" : "french"
}
```

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.update({
  name: "Flora Duell"
}, {
  "_id": 109,
  "name": "Flora Duell",
  "scores": [{
      "score": 60.68238966626067,
      "type": "exam"
    },
    {
      "score": 32.77972040308903,
      "type": "quiz"
    },
    {
      "score": 85.732755740408484,
      "type": "homework"
    }
  ],
  "age": 19,
  "nationality": "french"
})
```

</p>
</details>

#### 5. Suponiendo que "Rosana Vales" no existiese, ¿Cómo podríamos hacer para que en ese caso, el nuevo documento simplemente se hubiese insertado?

<details>
<summary>Ver respuesta</summary>
<p>

```js
db.students.update({
  name: "Flora Duell"
}, {
  "_id": 109,
  "name": "Flora Duell",
  "scores": [{
      "score": 60.68238966626067,
      "type": "exam"
    },
    {
      "score": 32.77972040308903,
      "type": "quiz"
    },
    {
      "score": 85.732755740408484,
      "type": "homework"
    }
  ],
  "age": 19,
  "nationality": "french"
}, {
  upsert: true
})
```

La clave es la opción **upsert**, que hace que si ningún documento cumple con los criterios de la consulta, el nuevo documento se inserta igualmente. Podemos comprobarlo lanzando la misma consulta para un nombre que no exista. Será necesario especificar un nuevo valor para el campo "\_id", porque es un índice único. Si no lo hacemos, la inserción fallará.

</p>
</details>




---
