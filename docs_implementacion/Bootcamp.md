# Bootcamp Odoo Developer & Integrations

Guía completa del bootcamp para aprender desarrollo e integraciones en Odoo 17.0.

## Requisitos del sistema

- **Python** 3.10+
- **PostgreSQL** 15+ (recomendado vía Docker)
- **Git**
- **Docker** Desktop o Engine

### Linux (recomendado)

En Linux todo funciona de fábrica. Odoo puede compilar assets CSS usando `sassc` (paquete del sistema) o `libsass` (binding Python). No requiere pasos adicionales.

```bash
sudo apt install python3-pip python3-venv git docker.io
```

### macOS

Similar a Linux. `sassc` está disponible vía Homebrew:

```bash
brew install sassc
```

### Windows

Odoo 17.0 tiene una limitación conocida en Windows: la compilación de SCSS a CSS puede fallar porque la herramienta `sassc` (CLI nativa) no existe en el ecosistema Windows. Si el binding Python `libsass` no se carga correctamente, Odoo muestra el error:

> `Could not execute command 'sassc'`

**Solución:** crear un archivo `.pth` en el entorno virtual para precargar `sass` antes de que Odoo arranque:

```powershell
echo "import sass" > venv\Lib\site-packages\zz_preload_sass.pth
```
Esto fuerza que `import sass as libsass` en `assetsbundle.py` de Odoo siempre tenga éxito, sin importar el orden de carga o el caché de bytecode (`.pyc`).

**Nota:** si ya arrancaste Odoo antes de aplicar el fix, puede que la caché de assets en la base de datos tenga el CSS con error. Para limpiarla:

```powershell
.\venv\Scripts\python -c "import psycopg2; c=psycopg2.connect(host='localhost',user='odoo',password='odoo',dbname='bootcamp_odoo_dev'); cur=c.cursor(); cur.execute(\"DELETE FROM ir_attachment WHERE name LIKE '%assets%'\"); c.commit(); c.close()"
```

Si prefieres evitar estos problemas, usa **Docker** o **WSL2** en Windows, donde el comportamiento es idéntico al de Linux.

## Contenido

| Semana | Tema | Archivo |
|--------|------|---------|
| 1 | Comprender Odoo (arquitectura, módulos, ORM, vistas, seguridad) | [semana1.md](semana1.md) |
| 2 | Desarrollo (ORM avanzado, relaciones, vistas heredadas, campos computados y wizards) | [semana2.md](semana2.md) |

## Comandos comunes

```bash
# Arrancar Odoo en modo desarrollo
# Linux:
 docker compose up -d

# Windows:
 docker compose up -d

# Actualizar un módulo
 docker compose run --rm odoo -d bootcamp_odoo_dev -u nombre_modulo --stop-after-init

# Shell interactivo de Odoo
 docker compose exec odoo odoo shell -d bootcamp_odoo_dev
```

## PostgreSQL con Docker

```bash
 docker compose up -d
```

 Para detenerlo: `docker compose stop db`
 Para reiniciarlo: `docker compose start db`
 Para eliminarlo: `docker compose down`
