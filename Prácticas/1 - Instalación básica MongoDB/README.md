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
cp "/root/curso-mongodb/Prácticas/1 - Instalación básica MongoDB/mongodb-org-4.2.repo" /etc/yum.repos.d/mongodb-org-4.2.repo
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
