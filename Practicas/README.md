# Instalación básica MongoDB

Instalaremos Mongo 4.2 en la máquina virtual CentOS 7 del laboratorio.

Partimos de la instantánea "0 - Estado incial". Los pasos a seguir son los siguientes:

0. Nos aseguramos de que la máquina tiene conexión a Internet, y tiene configurados y en ejecución los servicios de DNS y NTP. Por ejemplo, podemos comprobarlo con estos comandos:
```
ping 1.1.1.1
ping www.mongodb.com
chronyc tracking
```
1. Configuramos el sistema de gestión de paquetes YUM para añadir un nuevo repositorio, donde están los paquetes de MongoDB 4.2.
Para ello, crearemos el fichero `/etc/yum.repos.d/mongodb-org-4.2.repo` con el siguiente contenido:
```shell
[mongodb-org-4.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
```


# Comandos y queries Mongo Shell

TODO

# Replica Set

TODO

# Sharding

TODO

# Desarrollo con MongoDB

TODO

# Pipeline de agregación

## Zips

1. Obtener las ciudades con una población superior a 10000
2. Obtener los resultados de la consulta anterior ordenados de mayor a menor, y que sólo tengan un campo personalizado llamado “población” (en castellano)
3. Queremos los estados con una población superior a 10 millones
4. Queremos la población media de las ciudades de cada estado
5. Queremos las ciudades más grandes y más pequeñas por estado


## Students

1. Calcular la media de edad de todos los estudiantes
2. Calcular la media de edad por cada nacionalidad
3. Calcular la media de las notas (ponderando por igual cada tipo de calificación)
4. Consideremos que sólo aprueban los alumnos que tienen más de 70 puntos en la tarea (“homework”): De los alumnos que aprueban, calcular la media de las notas del examen
5. Para cada rango de 2 años en el intervalo [20, 30), obtener un documento con un array de las nacionalidades presentes
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

# MapReduce

## students

1. Calcular la media de las notas por cada nacionalidad. Guardar los resultados en una nueva colección, o bien sacarlos a la consola.

# ¡¡PENDIENTE PROBAR EN LOCAL!!

Con funciones anónimas:

```javaScript
db.students.mapReduce(
  function() {
    totalScore = 0;
    this.scores.forEach(function(element) {
      totalScore += element.score;
    });
    emit(this.nationality, totalScore)
  },
  function(key, values) {
    return Array.average( values )
  },
  { out: { inline: 1 }}
)
```

Usando funciones nombradas:

```javaScript
var calculateStudentScores = function() {
  totalScore = 0;
  this.scores.forEach(function(element) {
    totalScore += element.score;
  });
  emit(this.nationality, totalScore)
}

var averageValuesArray = function(key, values) {
  return Array.average(values)
}


db.students.mapReduce(
  calculateStudentScores,
  averageValuesArray,
  {
    out: {
      inline: 1
    }
  }
)
```
