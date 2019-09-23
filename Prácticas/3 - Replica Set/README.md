# Replica Set

Vamos a desplegar una arquitectura de MongoDB en Replica Set de 3 nodos.

Normalmente, cada nodo debería estar en una máquina diferente e incluso en centros de datos diferentes para proveer de redundancia geográfica. Dadas las limitaciones del entorno de laboratorio, vamos a simularlo utilizando tres procesos "mongod" que se ejecuten en la misma máquina virtual, escuchando respectivamente en los puertos 27017, 27018 y 27019.

Partimos del punto en el que terminamos la práctica anterior, o bien de la imagen "2 - Zips, estudiantes y pokemon importados" del entorno correspondiente ("lab" si estamos en la Intranet y vamos a usar un proxy).

En primer lugar, paramos y deshabilitamos el servicio de "mongod" que hemos instalado previamente:
```bash
systemctl stop mongod
systemctl disable mongod
```

Creamos 3 directorios para almacenar los datos:

```bash
mkdir -p /data/rscurso_1
mkdir -p /data/rscurso_2
mkdir -p /data/rscurso_3
```

Vamos a observar uno de los ficheros de configuración de "mongod" que vamos a usar para levantar las instancias:
```bash
cat "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso1.conf"
```

**¿Qué cambia respecto al fichero que habíamos usado para el despliegue en modo "standalone" (/etc/mongod.conf)**

<details>
<summary>Ver respuesta</summary>
<p>

La diferencia fundamental es la introducción de la sección "replication", con una única propiedad, el nombre del Replica Set: "rscurso".

Además, cambian los directorios en los que se van a almacenar los datos ("storage.dbPath") y los logs ("systemLog.path"), para que estos se guarden en el directorio que acabamos de crear.

</p>
</details>  

Revisamos también los otros dos ficheros de configuración que vamos a usar:
```bash
cat "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso2.conf"
cat "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso3.conf"
```

**¿Qué diferencias hay entre estos tres ficheros?**

<details>
<summary>Ver respuesta</summary>
<p>

Cambian los paths de datos y logs y el puerto de escucha.

</p>
</details>  

Arrancamos tres instancias de "mongod" con los ficheros de configuración correspondientes. En este caso, no vamos a utilizar "systemd", sino que vamos a utilizar los binarios que hemos instalado ejecutándolos nosotros directamente.

```bash
mongod --config "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso1.conf"
mongod --config "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso2.conf"
mongod --config "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso3.conf"
```

Comprobamos que realmente se están ejecutando tres instancias de "mongod" en nuestra máquina virtual. Podemos comprobarlo de varias formas. Por ejemplo, listando los procesos del sistema y filtrando por "mongod":

```bash
ps -ef | grep mongod
```

**¿Con qué usuario se están ejecutando los procesos "mongod"?**
<details>
<summary>Ver respuesta</summary>
<p>

Se ejecutan como usuario "root".

Cuando hemos ejecutado la base de datos utilizando "systemd", el usuario que ejecutaba la base de datos era un usuario específico llamado "mongod". Esta, y otras opciones de ejecución a nivel de sistema operativo estaban especificadas en lo que se llama el fichero de definición de servicio de "systemd", que se ha creado autmáticamente cuando hemos hecho la instalación a través de Yum.

Como referencia, este es el contenido de dicho fichero ("/usr/lib/systemd/system/mongod.service"):

```bash
[Unit]
Description=MongoDB Database Server
Documentation=https://docs.mongodb.org/manual
After=network.target

[Service]
User=mongod
Group=mongod
Environment="OPTIONS=-f /etc/mongod.conf"
EnvironmentFile=-/etc/sysconfig/mongod
ExecStart=/usr/bin/mongod $OPTIONS
ExecStartPre=/usr/bin/mkdir -p /var/run/mongodb
ExecStartPre=/usr/bin/chown mongod:mongod /var/run/mongodb
ExecStartPre=/usr/bin/chmod 0755 /var/run/mongodb
PermissionsStartOnly=true
PIDFile=/var/run/mongodb/mongod.pid
Type=forking
# file size
LimitFSIZE=infinity
# cpu time
LimitCPU=infinity
# virtual memory size
LimitAS=infinity
# open files
LimitNOFILE=64000
# processes/threads
LimitNPROC=64000
# locked memory
LimitMEMLOCK=infinity
# total threads (user+kernel)
TasksMax=infinity
TasksAccounting=false
# Recommended limits for for mongod as specified in
# http://docs.mongodb.org/manual/reference/ulimit/#recommended-settings

[Install]
WantedBy=multi-user.target
```

</p>
</details>  

En este momento, tenemos tres instancias de "mongod" en ejecución. Nos queda inicializar el Replica Set para que empiecen a mandarse "heartbeats" entre sí. Para ello:

* Nos conectamos a cualquiera de las tres. Por ejemplo:
```bash
mongo --port 27017
```
Especificar el puerto en este caso es opcional, si no lo hacemos se usa el 27017 por defecto.

* Inicializamos el Replica Set:
```
rs.initiate({_id: "rscurso", members:[{_id: 0, host: "127.0.0.1:27017"},{_id:1, host: "127.0.0.1:27018"}, {_id:2, host:"127.0.0.1:27019"}]})
```

Los comandos de MongoDB relativos al Replica Set empiezan por "rs".

Comprobamos el estado del Replica Set desde una mongo shell conectada a cualquiera de los nodos:
```bash
rs.status()
```

**¿Qué nodo es el primario?**
<details>
<summary>Ver respuesta</summary>
<p>

Puede ser cualquiera de los nodos. El campo "state" de cada elemento del array "members" nos lo da en forma numérica y el campo "stateStr" lo da en formato legible. Los estados en los que puede estar un miembro se definen [aquí](https://docs.mongodb.com/manual/reference/replica-states/).

</p>
</details>

**¿Cuál es el intervalo de heartbeats del clúster?**
<details>
<summary>Ver respuesta</summary>
<p>

2 segundos, como podemos ver en el campo "heartBeatIntervalMillis"

</p>
</details>

Entramos con una shell a cualquiera de los nodos secundarios y lanzamos cualquier comando de lectura, por ejemplo ```show dbs```. **¿Qué ocurre?**

<details>
<summary>Ver respuesta</summary>
<p>

Nos saltará un error de tipo "not master and slaveOk=false".

</p>
</details>

En un Replica Set, se debe poder leer sobre los secundarios, sin embargo, MongoDB nos obliga a confirmar que sabemos que estamos en un nodo secundario. Esto es porque si leemos sobre los secundarios, los datos que obtendremos no van a estar necesariamente actualizados (aunque eventualmente lo estarán).

Para indicar a Mongo que sabemos que estamos en un secundario, utilizamos el comando:
```js
rs.slaveOk()
```

Ahora, los comandos de lectura funcionarán correctamente.

Si probamos a lanzar un comando de escritura, este fallará con el error "not master", pues sólo se puede escribir sobre el primario.

#### Write concern
Cada query que se lanza sobre la base de datos puede utilizar el "write concern" que prefiera, pero existe un valor por defecto configurado. Está en la propiedad "settings.getLastErrorDefaults" de la configuración del Replica Set.

Teniendo en cuenta esto y la [especificación de formato del write concern](https://docs.mongodb.com/manual/reference/write-concern/#write-concern), **¿Qué tipo de write concern está configurado por defecto?**

<details>
<summary>Ver respuesta</summary>
<p>

* w: 1 significa que las escrituras se confirmarán cuando se hayan escrito en el nodo primario.
* wtimeout: 0 significa que no hay timeout de escritura.

Además, puede caber la duda de si es necesario que el dato haya sido consolidado en el journal. [Este artículo](https://docs.mongodb.com/manual/reference/write-concern/#replica-sets) lista todas las casuísticas posibles. En nuestro caso, tenemos "w:1" y "j" no especificado, por lo que basta con que el primario haya escrito el dato en memoria para darlo por válido. **Esto supone que no hay garantía de que el último dato escrito se haya consolidado a disco en caso de caída del nodo**

</p>
</details>

Supongamos que queremos garantizar que cada dato se ha escrito en el journal de la mayoría de los nodos antes de devolver el OK al cliente. **Configura este comportamiento en el clúster** Utilizar [rs.reconfig()](https://docs.mongodb.com/manual/reference/method/rs.reconfig/)

<details>
<summary>Ver respuesta</summary>
<p>

La especificación de writeConcern que queremos es:
```js
{
  w: "majority",
  j: true,
  wtimeout: 0
}
```
La propiedad "j: true" en realidad sería opcional porque está gobernada por el valor de configuración "writeConcernMajorityJournalDefault", que ya está a "true". Esto se explica en el artículo con las casuísticas del writeConcern. No hay problema por explicitarla.

Ahora, para aplicar la nueva configuración, lanzamos desde el primario:

```
configuracion = rs.conf()
configuracion.settings.getLastErrorDefaults = {w: "majority", j: true, wtimeout: 0}
rs.reconfig(configuracion)
```

Y comprobamos que todo ha funcionado lanzando de nuevo ```rs.conf()```

</p>
</details>

**Conmutar el rol de primario a otro nodo**
<details>
<summary>Ver respuesta</summary>
<p>

Entramos al primario y ejecutamos ```rs.stepDown()```.

Comprobamos que se elige otro nodo primario con ```rs.status()```.

</p>
</details>

**Apagado del Replica Set**

Entrar al nodo 1, y hacer:
```
use admin
db.shutdownServer()
```
Hacer lo mismo con los nodos 2 y 3.

---
