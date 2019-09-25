# Pipeline de agregación

Partimos del escenario de prácticas donde tengamos la Mongo levantada en standalone y con las colecciones importadas.

## Zips

Usaremos la colección zips (```use zips```), con documentos como este:

```js
{
        "_id" : "02199",
        "city" : "BOSTON",
        "loc" : [
                -71.082543,
                42.347873
        ],
        "pop" : 886,
        "state" : "MA"
}
```

El campo "\_id" es el código postal. Cada código postal pertenece a una ciudad, y a su vez cada ciudad pertenece a un estado. Los datos de población son del código postal.

#### 1. Obtener las ciudades con una población superior a 10000 habitantes

<details>
<summary>Ver solución</summary>
<p>


```javaScript
db.zips.aggregate([{
    $group: {
      _id: "$city",
      poblacion: {
        $sum: "$pop"
      }
    }
  },
  {
    $match: {
      poblacion: {
        $gt: 10000
      }
    }
  }
])
```

</p>
</details>

#### 2. Obtener los resultados de la consulta anterior ordenados de mayor a menor, y que sólo tengan un campo personalizado llamado “población” (en castellano)

<details>
<summary>Ver solución</summary>
<p>


```javaScript
db.zips.aggregate([{
    $group: {
      _id: "$city",
      poblacion: {
        $sum: "$pop"
      }
    }
  },
  {
    $match: {
      poblacion: {
        $gt: 10000
      }
    }
  }, {
    $project: {
      _id: 0,
      poblacion: 1
    }
  },
  {
    $sort: {
      poblacion: -1
    }
  }
])
```

</p>
</details>


#### 3. Queremos la población media de las ciudades de cada estado

<details>
<summary>Ver solución</summary>
<p>

```javaScript
db.zips.aggregate([{
    $group: {
      _id: {
        estado: "$state",
        ciudad: "$city"
      },
      poblacion: {
        $sum: "$pop"
      }
    }
  },
  {
    $group: {
      _id: "$_id.estado",
      poblacion_media_ciudades: {
        $avg: "$poblacion"
      }
    }
  }
])
```

Hacemos 2 fases de agrupación. La primera agrupa los documentos por ciudad y estado y calcula la población total para cada ciudad. Tras ese paso los documentos son así:

```js
{
  "_id": {
    "estado": "CO",
    "ciudad": "EDGEWATER"
  },
  "poblacion": 13154
}
```

La segunda fase de agrupación agrupa los documentos por el campo "\_id.estado" (campo "estado" en el documento "\_id") y calcula la media de población para las ciudades de cada estado.

</p>
</details>


#### 4. (Difícil) Para cada estado, obtener el nombre y número de habitantes de la ciudad más grande y la más pequeña

<details>
<summary>Ver solución</summary>
<p>


```javaScript
db.zips.aggregate([{
    $group: {
      _id: {
        estado: "$state",
        ciudad: "$city"
      },
      poblacion: {
        $sum: "$pop"
      }
    }
  },
  {
    $sort: {
      poblacion: -1
    }
  },
  {
    $group: {
      _id: "$_id.estado",
      mayorCiudad: {
        $first: "$_id.ciudad"
      },
      poblacionMayorCiudad: {
        $first: "$poblacion"
      },
      menorCiudad: {
        $last: "$_id.ciudad"
      },
      poblacionMenorCiudad: {
        $last: "$poblacion"
      }
    }
  }
])
```

</p>
</details>


## Students

#### 1. Calcular la media de edad de todos los estudiantes

Para agrupar sobre todos los documentos de la colección, se usa ```"_id": null``` dentro de la etapa de agrupación.

<details>
<summary>Ver solución</summary>
<p>


```javaScript
db.students.aggregate([{
  $group: {
    _id: null,
    media_edad: {
      $avg: "$age"
    }
  }
}])
```

</p>
</details>


#### 2. Calcular la media de edad por cada nacionalidad

<details>
<summary>Ver solución</summary>
<p>


```javaScript
db.students.aggregate([{
  $group: {
    _id: "$nationality",
    media_edad: {
      $avg: "$age"
    }
  }
}])
```

</p>
</details>


#### 3. Calcular la media de las notas de cada tipo de entregable ("exam", "homework" y "quiz")

<details>
<summary>Ver solución</summary>
<p>


```javaScript
db.students.aggregate([{
    $unwind: "$scores"
  },
  {
    $group: {
      _id: "$scores.type",
      media: {
        $avg: "$scores.score"
      }
    }
  }
])
```

Tras la etapa "unwind", cada documento de estudiante se convierte en tres documentos como estos, permitiendo ya agrupar por tipo de entragable (ya no está dentro de un array):

```js
{
  "_id": 82,
  "name": "Santiago Dollins",
  "scores": {
    "score": 33.48242310776701,
    "type": "exam"
  },
  "age": 32,
  "nationality": "italian"
}

{
  "_id": 82,
  "name": "Santiago Dollins",
  "scores": {
    "score": 60.49199094204558,
    "type": "quiz"
  },
  "age": 32,
  "nationality": "italian"
}

{
  "_id": 82,
  "name": "Santiago Dollins",
  "scores": {
    "score": 87.02564768982076,
    "type": "homework"
  },
  "age": 32,
  "nationality": "italian"
}
```

</p>
</details>


#### 4. Consideremos que sólo aprueban los alumnos que tienen más de 70 puntos en la tarea (“homework”): De los alumnos que aprueban, calcular la media de las notas del examen

<details>
<summary>Ver solución</summary>
<p>


```javaScript
db.students.aggregate([{
    $match: {
      scores: {
        $elemMatch: {
          type: "exam",
          score: {
            $gt: 70
          }
        }
      }
    }
  },
  {
    $unwind: "$scores"
  },
  {
    $match: {
      "scores.type": "exam"
    }
  },
  {
    $group: {
      _id: null,
      mediaExamen: {
        $avg: "$scores.score"
      }
    }
  }
])
```

</p>
</details>


#### 5. Para cada rango de 2 años en el intervalo [20, 30), obtener un documento con un array de las nacionalidades presentes

Esta división en intervalos, se usa habitualmente para hacer diagramas de barras. Cada uno de estos intervalos se llama en inglés "bucket". Los buckets que deberemos usar son [ 20, 22, 24, 26, 28, 30 ]. Consultar la [documentación de etapas del framework de agregación](https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/).

<details>
<summary>Ver solución</summary>
<p>


```javaScript
  db.students.aggregate(  [
    {
      $bucket: {
        groupBy: "$age",
        boundaries: [ 20, 22, 24, 26, 28, 30 ],
        default: "resto",
        output: {
          "numero": { $sum: 1 },
          "nacionalidades" : { $addToSet: "$nationality" }
        }
      }
    }
  ])
```

</p>
</details>

---
