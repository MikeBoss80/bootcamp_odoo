Construir e iniciar
docker compose up --build

Usar cuando:

modificaste Dockerfile;
agregaste paquetes;
cambiaste la imagen base.
Ejecutar en segundo plano

Para desarrollo diario normalmente usaremos:

docker compose up -d

La -d significa detached.

Ejemplo:

docker compose up -d

Te devuelve la terminal inmediatamente.

Ver logs
docker compose logs -f odoo

Para ver qué está haciendo Odoo.

Detener servicios
docker compose down

Detiene y elimina los contenedores, pero mantiene los volúmenes.

La base de datos sigue ahí.

Detener y borrar todo
docker compose down -v

⚠️ Esto elimina los volúmenes.

En nuestro caso:

elimina PostgreSQL;
elimina la base de datos;
vuelve a crearla desde cero.

Solo lo usaremos si tenemos problemas con credenciales o una instalación inicial corrupta


#PARA IMPLEMENTAR EN EL BOOTCAMP Y CORREGIR RUTA 

Resumen del entorno Odoo + GitHub Codespaces
Objetivo inicial

Crear un entorno de desarrollo profesional para Odoo 17 que cumpla con:

Desarrollo cómodo en GitHub Codespaces.
Código versionado en Git.
Fácil clonación en Windows.
Sin instalar Odoo ni PostgreSQL directamente en la máquina local.
Entorno reproducible mediante Docker.
Preparado para crear módulos personalizados (custom_addons).

La idea es que cualquier persona pueda clonar el repositorio, ejecutar Docker y tener el mismo entorno funcionando.

Arquitectura creada

Actualmente tenemos esta estructura conceptual:

bootcamp_odoo/
│
├── docker-compose.yml
├── Dockerfile
├── .env
│
├── config/
│   └── odoo.conf
│
├── custom_addons/
│   └── (aquí irán nuestros módulos)
│
└── README.md
Componentes del entorno
1. Contenedor PostgreSQL

Archivo:

docker-compose.yml

Creamos un servicio:

db:
  image: postgres:15

Responsabilidad:

Servir como motor de base de datos para Odoo.
Mantener los datos persistentes mediante volumen Docker.

Volumen:

postgres_data

Esto evita perder las bases al reiniciar contenedores.

2. Contenedor Odoo

También en:

docker-compose.yml

Servicio:

odoo:

Usa una imagen personalizada:

build:
  dockerfile: Dockerfile

Responsabilidad:

Ejecutar Odoo 17.
Cargar nuestros módulos personalizados.
Conectarse al PostgreSQL.

Puerto:

8069:8069

Este es el puerto web de Odoo.

Dockerfile creado

Actualmente:

FROM odoo:17

USER root

RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

USER odoo
¿Qué logramos?

Partimos de la imagen oficial:

odoo:17

y agregamos herramientas útiles:

git → trabajar con repositorios
curl → pruebas HTTP
vim → edición rápida dentro del contenedor

Luego regresamos al usuario:

odoo

para mantener buenas prácticas de seguridad.

Configuración Odoo

Archivo:

config/odoo.conf

Configuramos:

Addons personalizados
addons_path =
/usr/lib/python3/dist-packages/odoo/addons,
/mnt/extra-addons

Esto es clave.

Odoo buscará módulos en:

/mnt/extra-addons

que viene del volumen:

./custom_addons:/mnt/extra-addons

Entonces nuestro código local:

custom_addons/

se convierte dentro del contenedor en:

/mnt/extra-addons
Base de datos

Configuración:

db_host = db
db_port = 5432
db_user = db_user_odoo
db_password = odoopsw_db

Observación importante:

db no es una IP.

Es el nombre del servicio Docker:

services:
  db:

Docker crea automáticamente la red interna.

Proxy Mode

El ajuste importante para Codespaces:

Antes:

proxy_mode = False

Ahora:

proxy_mode = True

¿Por qué?

Porque Codespaces coloca un proxy HTTPS delante de nuestro contenedor.

Sin esto Odoo intentaba generar URLs como:

http://localhost:8069

Ahora respeta:

https://xxxxx-8069.app.github.dev
Variables de entorno


