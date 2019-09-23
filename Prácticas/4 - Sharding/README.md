# Sharding

Partimos de un escenario en el que no tenemos corriendo ninguna instancia de "mongod", lo verificamos con ```ps -ef | grep mongod```

Una vez más, vamos a simular el escenario completo en una única máquina virtual, por las limitaciones de recursos del entorno de laboratorio.

### 1. Levantamos el Replica Set de los config servers
Creamos directorios de datos:

```bash
mkdir -p /data/configdb1
mkdir -p /data/configdb2
mkdir -p /data/configdb3
```

Arrancamos los tres nodos del Replica Set. En esta ocasión, en lugar de utilizar un fichero de configuración, pasaremos los parámetros por línea de comandos. Nota: En la shell de Linux, "&" sirve para que el proceso pase a ejecutarse en segundo plano, y podamos seguir trabajando con la consola.
```bash
mongod --configsvr --replSet config --dbpath /data/configdb1 --port 27019 --logpath /data/configdb1/mongod.log &
mongod --configsvr --replSet config --dbpath /data/configdb2 --port 27029 --logpath /data/configdb2/mongod.log &
mongod --configsvr --replSet config --dbpath /data/configdb3 --port 27039 --logpath /data/configdb3/mongod.log &
```
Nos conectamos a uno de los nodos, inicializamos el Replica Set y comprobamos su estado:
```js
rs.initiate({_id: "config", members:[{_id: 0, host: "127.0.0.1:27019"},{_id:1, host: "127.0.0.1:27029"}, {_id:2, host:"127.0.0.1:27039"}]})
rs.status()
```

### 2. Levantamos el proceso mongos

```bash
mkdir -p /data/mongos_log
mongos --configdb config/127.0.0.1:27019,127.0.0.1:27029,127.0.0.1:27039 --logpath /data/mongos_log/mongos.log &
```

### 3. Creamos y levantamos los shards

En un entorno productivo, cada shard debe ser a su vez un Replica Set. En este caso, levantaremos los shards en modo standalone.

```bash
mkdir -p /data/shard1
mkdir -p /data/shard2
mongod --shardsvr --dbpath /data/shard1 --port 27018 --logpath /data/shard1/mongod.log &
mongod --shardsvr --dbpath /data/shard2 --port 27028 --logpath /data/shard2/mongod.log &
```

### 4. Añadimos los shards

Nos conectamos a la instancia de mongos y añadimos los shards:

```js
sh.addShard("127.0.0.1:27018")
sh.addShard("127.0.0.1:27028")
```

La respuesta a estos comandos nos indicará los nombres de los shards que se han creado.

### 5. Creamos una base de datos llamada mishard e inicializamos el shard

Vamos a utilizar como shard key el campo "x", que será numérico y que iremos insertando en los documentos.

```js
use mishard
db.particion.createIndex({x:1})
sh.enableSharding("mishard")
sh.shardCollection("mishard.particion",{x:1})
```

### 6. Alimentamos la colección particionada
```js
for (i=0; i<1000000;i++){db.particion.insert({x:i,y:i*2,z:i-100});}
```
Tarda bastantes minutos en terminar. Para ver el progreso, podemos abrir otra shell e ir contando los documentos de la colección.

Este rendimiento tan bajo se debe a que en una máquina virtual con una sola vCPU y 1 GB de memoria asignados tenemos 5 procesos "mongod" en ejecución, más el "mongos", más la mongo shell donde ejecutamos el código.

## Operaciones y preguntas sharding

Lanzamos el comando para obtener el estado del clúster:
```js
sh.status()
```
### 1. ¿Cuántos chunks tiene la colección?

<details>
<summary>Ver respuesta</summary>
<p>

Tiene un único chunk:
```yaml
chunks:
    shard0000 1
    { "x" : { "$minKey" : 1 } } -->> { "x" : { "$maxKey" : 1 } } on : shard0000 Timestamp(1, 0)
```
</p>
</details>

### 2. ¿Qué rango de la shard key corresponde a cada chunk?

<details>
<summary>Ver respuesta</summary>
<p>

Al haber un solo chunk, tiene todo el rango de valores para la shard key, desde el máximo al mínimo.

</p>
</details>

### 3. ¿Cuál es el tamaño de chunk?
Utilizaremos la base de datos "config", accesible desde mongos:
```
use config
```

Aquí ejecutamos:

```
db.settings.find()
```

Y vemos que no hay resultados. Esto implica que los valores son los valores por defecto. Si se hubiese modificado el tamaño de chunk, habría que haber escrito en esta colección. Ver ["Modificar el tamaño de chunk"](https://docs.mongodb.com/manual/tutorial/modify-chunk-size-in-sharded-cluster/#modify-chunk-size-in-a-sharded-cluster).

<details>
<summary>Ver respuesta</summary>
<p>

Al no haber sido modificado, el valor por defecto, 64 MB.

</p>
</details>

### 4. Dividir los datos en dos chunks con los siguientes rangos: [x: minKey, x:500000), [x: 500000, x: maxKey)

<details>
<summary>Ver respuesta</summary>
<p>

```js
sh.splitAt("mishard.particion", {x: 500000})
```

Podemos verificar que ahora existen dos chunks con el ```sh.status()```
</p>
</details>

Normalmente, si el autoSplit está habilitado, la división de un chunk se hará automáticamente cuando se inserte un documento que haga que el chunk supere los 64 MB. Igualmente, si el balanceador de chunks está activado, MongoDB decidirá autónomamente en qué shard vive cada chunk.

### 5. ¿Está el autoSplit habilitado? ¿Y el balanceador?

<details>
<summary>Ver respuesta</summary>
<p>

```js
sh.status()
```

```yaml
autosplit:
      Currently enabled: yes
balancer:
      Currently enabled:  yes
      Currently running:  no
      Failed balancer rounds in last 5 attempts:  5
      Last reported error:  Error connecting to 127.0.0.1:27018 :: caused by :: Connection refused
      Time of Reported error:  Mon Sep 23 2019 23:46:33 GMT+0200 (CEST)
      Migration Results for the last 24 hours:
              No recent migrations
```

</p>
</details>

## Apagado del clúster completo
Entramos a cada nodo, hacemos ```use admin``` y luego ```db.shutdownServer()```. Orden: primero apagar el mongos, luego los shards y luego el replica set de configuración.

Para el resto de las prácticas, volveremos a la configuración inicial en standalone:
```
systemctl start mongod
systemctl enable mongod
```

---
