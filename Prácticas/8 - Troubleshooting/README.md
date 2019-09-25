# Diagnóstico y troubleshooting

#### 1. En la coleccion de Pokémon, ejecutar una búsqueda con un filtro por el campo "id" (ojo, no "\_id", son campos diferentes) Obtener las estadísticas de ejecución con ".explain()".

#### 2. Crear un índice sobre dicho campo

#### 3. Repetir la query del apartado 1. ¿Está nuestra búsqueda utilizando el índice que hemos creado?

#### 4. Activar el profiling de todas las queries para la base de datos de Pokémon. Hacer alguna query y comprobar qué es lo que aparece en la colección system.profile para dichas queries

#### 5. Ejecutar mongostat con una frecuencia de refresco de 1 minuto. Durante ese minuto, lanzar algunas queries contra la base de datos y comprobar que vemos esas operaciones en la salida de mongostat.

#### 6. Usando mongotop, medir el tiempo que se pasa leyendo y escribiendo en cada colección a intervalos de 1 minuto. Repetir las queries del ejercicio anterior.

#### 7. Probar mongoreplay: capturar algunas queries sobre la base de datos, levantar una instancia de mongo en el puerto 27018 y lanzar esas queries contra la nueva instancia.

Veremos que mongoreplay no está instalado. En el issue [SERVER-39595](https://jira.mongodb.org/browse/SERVER-39595) del issue tracker de Jira de MongoDB se explica por qué motivos ya no se instala mongoreplay cuando se instala Mongo usando el gestor de paquetes Yum.

Para poder hacer este ejercicio, habrá que instalar mongoreplay descargando el paquete "tar.gz" (TGZ) para RHEL 7.0 (es equivalente a CentOS 7) desde el [MongoDB Download Center](https://www.mongodb.com/download-center/community?jmp=docs). A fecha de septiembre 2019, este paquete sí que contiene mongoreplay. Para descomprimirlo desde la línea de comandos:

```bash
tar -zxvf mongodb-linux-x86_64-rhel70-4.2.0.tgz
```

Ayuda para levantar la nueva instancia:
```
mkdir -p /data/troubleshooting
mongod --dbPath /data/troubleshooting --port 27018 --logpath /data/troubleshooting &
```

Esta instancia representaría una maqueta sobre la que estamos probando el tráfico de producción.
