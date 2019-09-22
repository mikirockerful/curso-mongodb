# Replica Set
```bash
systemctl stop mongod
systemctl disable mongod
mkdir -p /data/rscurso_1
mkdir -p /data/rscurso_2
mkdir -p /data/rscurso_3
mongod --config "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso1.conf"
mongod --config "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso2.conf"
mongod --config "/root/curso-mongodb/Prácticas/3 - Replica Set/rscurso3.conf"
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
