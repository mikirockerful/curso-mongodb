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
