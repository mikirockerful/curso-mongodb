# Instalación básica MongoDB

Instalaremos Mongo 4.2 en la máquina virtual CentOS 7 del laboratorio.

Partimos de la instantánea "0 - Estado incial".

Referencia: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/

Los pasos a seguir son los siguientes:

#### 0. Nos aseguramos de que la máquina tiene conexión a Internet, y tiene configurados y en ejecución los servicios de DNS y NTP.

**Nota**: Este paso no funciona en el laboratorio, porque el acceso a Internet funciona a través de un proxy que sólo acepta HTTP o HTTPS. Ni el ping ni el NTP pueden atravesarlo.

Por ejemplo, podemos comprobarlo con estos comandos:
```
ping 1.1.1.1
ping www.mongodb.com
chronyc tracking
```
#### 1. Configuramos el sistema de gestión de paquetes YUM para añadir un nuevo repositorio, donde están los paquetes de MongoDB 4.2.
Para ello, crearemos el fichero `/etc/yum.repos.d/mongodb-org-4.2.repo` con el siguiente contenido:
```bash
[mongodb-org-4.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
```
Para no tener que copiarlo a mano, el fichero se ha subido al repositorio de Git. En el escenario de prácticas, bastará con copiarlo:
```
cp /root/curso-mongodb/Practicas/Instalacion/mongodb-org-4.2.repo /etc/yum.repos.d/mongodb-org-4.2.repo
```

Nos aseguramos de que el repositorio está correctamente configurado con ```yum repolist```

**Nota**: En el laboratorio, podemos tener problemas con el proxy. Para comprobar si tenemos acceso a Internet, podemos pedir una web: ```curl www.mongodb.com```. Si nos encontramos con un error 407 "Authentication Required", abrimos un navegador e iniciamos sesión en la Intranet.

#### 2. Instalamos los paquetes de mongodb
```bash
yum install mongodb-org
```
Nos listará las dependencias y el espacio ocupado. Confirmamos la instalación.

**¿Qué paquetes se han instalado?**

¡Listo! Ya tenemos MongoDB instalado. Lo podemos comprobar ejecutando la shell con el comando ```mongo```. Eso sí, todavía no tenemos ninguna base de datos levantada, por lo que el comando dará error de conexión.

#### 3. Configuración de la instancia
Al haber instalado MongoDB a través del gestor de paquetes, viene ya con cierta configuración creada por defecto. La revisaremos con: ```cat /etc/mongod.conf```

**¿En qué puerto escucha el proceso mongod?**

**¿En qué interfaz o interfaces escucha?**

**¿En qué directorio se van a guardar los datos?**

Ahora arrancaremos el proceso mongod. Podríamos arrancarlo con la opción ```--config```, pasándole el fichero de parámetros. Sin embargo en este caso, al haber hecho la instalación a través de Yum, tenemos ya configurado mongod como servicio de systemd. De esta forma, dejaremos que sea el sistema operativo quien administre el proceso mongod como un daemon de sistema, simplificando y uniformizando dicha administración.

Por tanto, arrancamos el servicio con:
```
systemctl start mongod
```

Y comprobamos que arranca, revisando el estado del servicio:
```
systemctl status mongod
```
Y buscando en el log la línea que indica que el demonio está arriba y esperando conexiones (```I NETWORK [initandlisten] waiting for connections on ...```). **Ayuda**: El fichero de log se define en ```/etc/mongod.conf```.

### 4. Prueba de conexión a la base de datos
Nos conectamos a la base de datos con: ```mongo```, obteniendo una shell. Este comando se conecta por defecto a la interfaz de loopback de la máquina en que se ejecuta (127.0.0.1), puerto 27017.

Cerramos la shell con ```quit()```.

#### Configuración adicional
Comprobemos qué ocurre con la base de datos si reiniciamos el servidor:
```
reboot
```

**¿En qué estado está el proceso mongod?**

En un entorno de producción, esto no es deseable. Normalmente querremos que la base de datos arranque con el sistema sin necesidad de intervención manual. Para ello, systemd resulta especialmente útil: simplemente lanzamos el comando ```systemctl enable mongod```, que nos indicará que se ha instalado el script de arranque. Podemos volver a reiniciar el servidor y comprobaremos que ahora, mongod arranca automáticamente.

---

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





---

# Replica Set
```bash
systemctl stop mongod
systemctl disable mongod
mkdir -p /data/rscurso_1
mkdir -p /data/rscurso_2
mkdir -p /data/rscurso_3
mongod --config "/root/curso-mongodb/Practicas/Replica Set/rscurso1.conf"
mongod --config "/root/curso-mongodb/Practicas/Replica Set/rscurso2.conf"
mongod --config "/root/curso-mongodb/Practicas/Replica Set/rscurso3.conf"
```

```
rs.initiate({_id: "rscurso", members:[{_id: 0, host: "127.0.0.1:27017"},{_id:1, host: "127.0.0.1:27018"}, {_id:2, host:"127.0.0.1:27019"}]})
```

Entrar al nodo 1, y hacer:
```
use admin
db.shutdownServer()
```
Hacer lo mismo con los nodos 2 y 3.

# ¡¡PENDIENTE PREGUNTAS RS!!


---

# Sharding
```bash
mkdir -p /data/configdb1
mkdir -p /data/configdb2
mkdir -p /data/configdb3
mongod --configsvr --replSet config --dbpath /data/configdb1 --port 27019 --logpath /data/configdb1/mongod.log &
mongod --configsvr --replSet config --dbpath /data/configdb2 --port 27029 --logpath /data/configdb2/mongod.log &
mongod --configsvr --replSet config --dbpath /data/configdb3 --port 27039 --logpath /data/configdb3/mongod.log &

rs.initiate({_id: "config", members:[{_id: 0, host: "127.0.0.1:27019"},{_id:1, host: "127.0.0.1:27029"}, {_id:2, host:"127.0.0.1:27039"}]})


mkdir -p /data/mongos_log
mongos --configdb config/127.0.0.1:27019,127.0.0.1:27029,127.0.0.1:27039 -- logpath /data/mongos_log/mongos.log &

mkdir -p /data/shard1
mkdir -p /data/shard2

mongod --shardsvr --dbpath /data/shard1 --port 27018 --logpath /data/shard1/mongod.log &
mongod --shardsvr --dbpath /data/shard2 --port 27028 --logpath /data/shard2/mongod.log &

sh.addShard("127.0.0.1:27018")
sh.addShard("127.0.0.1:27028")
use mishard
db.particion.createIndex({x:1})
for (i=0; i<1000000;i++){db.particion.insert({x:i,y:i*2,z:i-100});} --> Tarda bastante. Para ver el progreso, podemos abrir otra shell e ir contando los documentos de la colección.
sh.status()
```
# ¡¡PENDIENTE PREGUNTAS SHARDING!!
Ver rangos de la clave de partición
Ver número de chunks
Hacer un split de chunk

Apagado:
Entramos a cada nodo, hacemos ```use admin``` y luego ```db.shutdownServer()```. Order: primero apagar el mongos, luego los shards y luego el replica set de configuración.

Para el resto de las prácticas, volveremos a la configuración inicial en standalone:
```
systemctl start mongod
systemctl enable mongod
```

---

# Desarrollo con MongoDB

TODO

---

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

# MapReduce

## students

#### 1. Calcular la media de las notas por cada nacionalidad. Guardar los resultados en una nueva colección, o bien sacarlos a la consola.

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
---

# Diagnóstico y troubleshooting
 TODO
