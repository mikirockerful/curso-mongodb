# Pipeline de agregación

## Zips

#### 1. Obtener las ciudades con una población superior a 10000
#### 2. Obtener los resultados de la consulta anterior ordenados de mayor a menor, y que sólo tengan un campo personalizado llamado “población” (en castellano)
#### 3. Queremos los estados con una población superior a 10 millones
#### 4. Queremos la población media de las ciudades de cada estado
#### 5. Queremos las ciudades más grandes y más pequeñas por estado


## Students

#### 1. Calcular la media de edad de todos los estudiantes
#### 2. Calcular la media de edad por cada nacionalidad
#### 3. Calcular la media de las notas (ponderando por igual cada tipo de calificación)
#### 4. Consideremos que sólo aprueban los alumnos que tienen más de 70 puntos en la tarea (“homework”): De los alumnos que aprueban, calcular la media de las notas del examen
#### 5. Para cada rango de 2 años en el intervalo [20, 30), obtener un documento con un array de las nacionalidades presentes
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

---
