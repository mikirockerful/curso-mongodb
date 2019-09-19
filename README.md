# Curso MongoDB - Repositorio de prácticas

En este repositorio se puede encontrar todo lo necesario para reproducir las prácticas del curso de MongoDB.

En el aula, el repo ha sido clonado en el directorio raíz del usuario ```root```. Se puede reproducir en otro equipo con ```git clone https://github.com/mikirockerful/curso-mongodb.git```.

Para actualizar el repositorio, entramos a la carpeta correspondiente con ```cd /root/curso-mongodb/``` y ejecutamos ```git pull```.

## Descripción del entorno de laboratorio
Las prácticas se basan en una máquina virtual Linux CentOS 7 de 64 bits, que irá evolucionando durante el curso.

Para evitar que problemas en una práctica supongan la imposibilidad de seguir el desarrollo del curso, las máquinas virtuales incluyen una serie de snapshots que permiten regenerar el escenario en cada momento.

Esto significa que se puede experimentar libremente sin miedo a "romper" el escenario de prácticas.

Datos de la máquina virtual:
  Usuario: vagrant
  Contraseña: vagrant

  Superusuario: root
  Contraseña: vagrant


## Requisitos para hacer las prácticas
Durante el desarrollo del curso, el material de prácticas estará preinstalado en los ordenadores corporativos.

Para poder hacer las prácticas en otro ordenador, es necesario instalar:
* Oracle virtualbox: https://www.virtualbox.org/ -> Es el hipervisor, software que ejecuta las máquinas virtuales
* Vagrant: https://www.vagrantup.com/ -> Para la provision automática de las máquinas virtuales

Opcionalmente:
* Docker: https://www.docker.com/ -> Para practicar la combinación de Docker y MongoDB
