# BOOTCAMP ODOO DEVELOPER & INTEGRATIONS
# Semana 1 — Comprender Odoo

**Objetivo de la semana:** Comprender cómo funciona un ERP y dominar la arquitectura básica de Odoo
**Resultado esperado:** Módulo Biblioteca instalable, con modelos, vistas y seguridad por roles
**Días incluidos:** Día 1 a Día 6 — 18 horas de contenido

---

## Índice

- [Día 1 — ¿Qué es un ERP? Introducción a Odoo](#día-1--qué-es-un-erp-introducción-a-odoo)
- [Día 2 — Arquitectura de Módulos](#día-2--arquitectura-de-módulos)
- [Día 3 — El ORM: Modelos y Campos](#día-3--el-orm-modelos-y-campos)
- [Día 4 — Vistas XML y Menús](#día-4--vistas-xml-y-menús)
- [Día 5 — Seguridad: Grupos y Permisos](#día-5--seguridad-grupos-y-permisos)
- [Día 6 — Repaso y Proyecto Completo](#día-6--repaso-general--proyecto-biblioteca-completo)

---

## Día 1 — ¿Qué es un ERP? Introducción a Odoo

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Explicar con tus propias palabras qué es un ERP y qué problema de negocio resuelve
- Entender por qué Odoo se organiza en módulos independientes
- Instalar Odoo en modo desarrollo y navegar su interfaz
- Identificar las carpetas principales del código fuente

### 📖 Teoría

Un **ERP (Enterprise Resource Planning)** centraliza todos los procesos de negocio —ventas, compras, inventario, contabilidad, RRHH— en una sola base de datos compartida. Odoo es un ERP de código abierto construido sobre **Python** y **PostgreSQL**, organizado como un conjunto de aplicaciones (módulos) que se instalan según la necesidad.

**Tres pilares de Odoo:**
- **ORM** — convierte clases de Python en tablas de PostgreSQL (nunca escribes SQL directo)
- **Vistas XML** — definen la interfaz separada de la lógica Python
- **Sistema de seguridad** — controla qué ve y hace cada usuario según su grupo

#### Diagrama: arquitectura general

```
Navegador (usuario)
      |
      v
  Servidor Odoo (Python) --- interpreta la vista XML
      |                       y ejecuta la lógica de negocio
      v
  ORM (models.Model)  ------- traduce objetos Python a filas
      |
      v
  PostgreSQL (base de datos) - almacenamiento real de los datos
```

#### Estructura de un módulo (addon)

```
mi_modulo/
├── __init__.py          # importa los submódulos de Python
├── __manifest__.py      # ficha técnica: nombre, versión, dependencias
├── models/
│   ├── __init__.py
│   └── mi_modelo.py     # define las clases (tablas)
├── views/
│   └── mi_modelo_views.xml   # define formularios, listas, menús
└── security/
    └── ir.model.access.csv   # define permisos por grupo
```

### 💻 Código explicado: __manifest__.py

```python
{
    'name': 'Biblioteca',
    'version': '1.0',
    'depends': ['base'],       # módulos de los que depende
    'data': [
        'security/ir.model.access.csv',
        'views/libro_views.xml',
    ],
    'installable': True,
    'application': True,       # aparece como app en el menú principal
}
```

- `depends`: le dice a Odoo qué módulos deben estar instalados antes
- `data`: lista ordenada de archivos XML/CSV a cargar al instalar/actualizar
- `application: True`: sin esto el módulo no aparece como app independiente

### 🐳 Entorno Docker (este proyecto)

```powershell
# Ya tienes Docker funcionando con:
docker compose up -d

# Verificar que Odoo responde
curl http://localhost:8069/web/login

# Ver logs
docker compose logs -f odoo

# Detener
docker compose down

# Reconstruir (si cambias Dockerfile)
docker compose up --build -d
```

> **Nota:** La instalación directa con `python odoo-bin` NO se usa en este proyecto. Todo corre dentro de contenedores Docker.

### ✅ Tu progreso

| Concepto | Estado |
|----------|--------|
| Docker funcionando con Odoo 17 | ✅ |
| PostgreSQL corriendo | ✅ |
| Acceso a `http://localhost:8069` | ✅ |
| Modo desarrollador activado | ⬜ Desde Ajustes → Activar modo desarrollador |
| Carpeta `custom_addons/biblioteca` creada | ✅ |

### 🧪 Reto
Sin ayuda: crea el módulo `biblioteca` vacío (solo estructura de carpetas y manifest) y logra que aparezca en la lista de Aplicaciones de Odoo. Documenta en un README.md los 3 problemas que se te presentaron y cómo los resolviste.

### ⚠️ Errores comunes
- Olvidar `installable: True` — el módulo existe pero Odoo nunca lo muestra
- No reiniciar con `-u nombre_modulo` tras crear el manifest por primera vez
- Confundir `depends` con imports de Python: son dependencias entre módulos Odoo

### 📌 Buenas prácticas
- Nombrar módulos en **snake_case** singular (ej. `biblioteca`, no `libro_modulo_v2`)
- Nunca modificar un módulo estándar de Odoo directamente: siempre extiendes desde uno propio
- Versionar con **Git** desde el primer día

### 📝 Resumen
Un ERP centraliza los procesos en una sola BD. Odoo lo logra mediante módulos independientes que se comunican a través del ORM. Cada módulo sigue una estructura estándar (`models/`, `views/`, `security/`) y se registra mediante su manifest.

---

## Día 2 — Arquitectura de Módulos

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Explicar por qué Odoo carga los módulos en un orden específico
- Dominar todas las claves del `__manifest__.py`
- Entender la cadena de imports desde `__init__.py` hasta cada modelo
- Distinguir los estados de un módulo: no instalado, instalado, por actualizar

### 📖 Teoría

Cuando el servidor arranca, Odoo recorre cada carpeta dentro de los addons-path buscando un `__manifest__.py`. Si lo encuentra, lo lee como diccionario y registra el módulo en la tabla `ir.module.module` con estado **no instalado**. El código Python no se carga hasta que el módulo se **instala o actualiza**.

**Claves del manifest:**

| Clave | Función |
|-------|---------|
| `depends` | Define orden de carga. Si A depende de B, Odoo carga B antes que A |
| `data` | Se carga **siempre** que el módulo se instala |
| `demo` | Solo se carga si la BD se creó con datos de demostración |
| `auto_install` | Convierte el módulo en "puente" que se instala automáticamente |
| `application` | `True` = aparece como ícono en el launcher de apps |
| `license` | Obligatorio desde versiones recientes de Odoo |

#### Diagrama: cadena de imports

```
__manifest__.py  ---- Odoo lee esto primero, sin ejecutar Python
     |
     | 'depends': ['base', 'mail']
     v
__init__.py (raíz del módulo)
     |
     | from . import models
     v
models/__init__.py
     |
     | from . import libro
     | from . import autor
     v
models/libro.py   models/autor.py   <-- aquí se ejecuta código Python real
```

> Si se omite una línea en cualquier eslabón de esta cadena, el archivo simplemente nunca se ejecuta.

### 💻 Código explicado

```python
{
    'name': 'Biblioteca',
    'version': '1.0.0',
    'category': 'Custom/Biblioteca',
    'summary': 'Gestión de libros, autores y préstamos',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/libro_views.xml',
        'views/menus.xml',
    ],
    'demo': [
        'demo/libro_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
```

```python
# __init__.py (raíz)
from . import models

# models/__init__.py
from . import libro
from . import autor
```

### 🐳 Comandos Docker

```powershell
# Actualizar módulo biblioteca
docker compose run --rm odoo -d postgres -u biblioteca --stop-after-init

# Shell interactivo de Odoo
docker compose run --rm odoo shell -d postgres

# Dentro del shell:
>>> env['biblioteca.autor']
# KeyError si falta el import en __init__.py
```

### ✅ Tu progreso en Día 2

| Concepto | Estado |
|----------|--------|
| `__manifest__.py` completo con todas las claves | ⬜ |
| `__init__.py` raíz importando `models` | ✅ |
| `models/__init__.py` importando `libro` y `autor` | ✅ |
| Modelo `Editorial` creado (reto del día) | ⬜ |

### 🧪 Reto
Agrega un tercer modelo **Editorial** al módulo Biblioteca, con su propio archivo en `models/`, su import en `models/__init__.py`, y una entrada en el manifest para su futura vista. Verifica en el shell que Odoo lo reconoce tras un `-u biblioteca`.

### ⚠️ Errores comunes
- Olvidar el import en `__init__.py` después de crear un modelo nuevo — **el más común de toda la semana**
- Poner archivos en `demo` que en realidad son configuración necesaria
- Cambiar `depends` y olvidar reiniciar el servidor (no solo actualizar)

### 📌 Buenas prácticas
- Un archivo de modelo por entidad de negocio (`libro.py`, `autor.py`)
- Mantener `depends` con el mínimo necesario
- Revisar el log del servidor al arrancar: Odoo reporta claramente fallos de carga

### 📝 Resumen
El manifest es el contrato entre el módulo y Odoo. La cadena de `__init__.py` es lo que realmente pone en memoria el código Python. El error más común: escribir código correcto que Odoo nunca ejecuta porque falta un import.

---

## Día 3 — El ORM: Modelos y Campos

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Explicar qué hace el ORM de Odoo y por qué nunca escribes SQL directo
- Declarar un modelo con `_name`, `_description` y campos básicos
- Entender `self.env` y usarlo para crear y consultar registros
- Crear la primera tabla real en PostgreSQL desde una clase Python

### 📖 Teoría

Cada modelo hereda de `models.Model`. Dos atributos obligatorios: `_name` (identificador técnico, ej. `biblioteca.libro` → tabla `biblioteca_libro`) y `_description` (etiqueta legible). Los campos (`fields.Char`, `fields.Integer`, etc.) se traducen en columnas de esa tabla.

- `self.env['modelo']` — devuelve el modelo para operar (crear, buscar, leer)
- `self.env.user` — usuario actual
- `self.env.company` — compañía activa
- Un **recordset** no es una lista: es una colección sobre la que puedes iterar y acceder a campos como atributos (`libro.titulo`, no `libro['titulo']`)

#### Diagrama: clase → tabla PostgreSQL

```
class Libro(models.Model):         tabla real: biblioteca_libro
    _name = 'biblioteca.libro'  -->  --------------------------------
    _description = 'Libro'          | id | titulo | anio | disponible |
                                     --------------------------------
    titulo = fields.Char()      -->  columna 'titulo'   (varchar)
    anio = fields.Integer()     -->  columna 'anio'     (integer)
    disponible = fields.Boolean()--> columna 'disponible' (boolean)
```

### 💻 Código explicado: modelo Libro completo

```python
from odoo import models, fields

class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro de la biblioteca'
    _rec_name = 'titulo'          # campo a mostrar al referenciar

    titulo = fields.Char(string='Título', required=True)
    isbn = fields.Char(string='ISBN')
    anio_publicacion = fields.Integer(string='Año de publicación')
    disponible = fields.Boolean(string='Disponible', default=True)
    genero = fields.Selection(
        selection=[
            ('ficcion', 'Ficción'),
            ('tecnico', 'Técnico'),
            ('historia', 'Historia'),
        ],
        string='Género',
    )
    fecha_ingreso = fields.Date(string='Fecha de ingreso', default=fields.Date.today)
```

### ✅ Tu modelo ACTUAL de libro vs el modelo de la guía

| Campo | Tu modelo actual | Guía (Día 3) | Acción |
|-------|-----------------|--------------|--------|
| `name` / `titulo` | `name` (funciona como `_rec_name` por defecto) | `titulo` con `_rec_name` | ⬜ Pendiente |
| `isbn` | ❌ No existe | `fields.Char('ISBN')` | ⬜ Agregar |
| `anio_publicacion` | ❌ No existe (tienes `fecha_publicacion`) | `fields.Integer('Año publicación')` | ⬜ Agregar |
| `disponible` | ❌ No existe | `fields.Boolean(default=True)` | ⬜ Agregar |
| `genero` (Selection) | ❌ No existe | `ficcion, tecnico, historia` | ⬜ Agregar |
| `fecha_ingreso` | ❌ No existe | `fields.Date(default=today)` | ⬜ Agregar |
| `autor` (Many2one) | ✅ Lo tienes | No lo pide aún (Semana 2) | ✅ Dejar |

### 🐳 Comandos Docker

```powershell
# Actualizar módulo para crear/actualizar tablas
docker compose run --rm odoo -d postgres -u biblioteca --stop-after-init

# Shell interactivo
docker compose run --rm odoo shell -d postgres

# Probar creación y búsqueda
>>> libro = env['biblioteca.libro'].create({
...     'titulo': 'Cien años de soledad',
...     'anio_publicacion': 1967,
...     'genero': 'ficcion',
... })
>>> libro.titulo
'Cien años de soledad'
>>> env['biblioteca.libro'].search([('genero', '=', 'ficcion')])
biblioteca.libro(1,)
```

### 🧪 Reto
Crea el modelo **Autor** (`biblioteca.autor`) con al menos: `name` (nombre), `nacionalidad` y `fecha_nacimiento`. Créalo en el shell y consulta todos los autores cuya nacionalidad sea la tuya usando `search()`. Todavía no se relaciona con Libro — eso es en Semana 2.

### ⚠️ Errores comunes
- Usar `_name` con mayúsculas (`biblioteca.Libro` en vez de `biblioteca.libro`)
- Olvidar `-u nombre_modulo` tras cambiar campos del modelo — la tabla no refleja los cambios
- Confundir `create()` (devuelve recordset) con un diccionario normal

### 📌 Buenas prácticas
- Siempre declarar `_description`: aparece en logs y en Ajustes técnicos
- Usar `string=` explícito en cada campo para etiquetas claras (ej. "Año de publicación" en vez de "Anio Publicacion")
- Probar cada modelo nuevo en el **shell** antes de construir su vista

### 📝 Resumen
El ORM traduce clases Python en tablas PostgreSQL. `self.env` es la puerta de entrada para crear y consultar datos. Hoy se crea la primera tabla real del proyecto.

---

## Día 4 — Vistas XML y Menús

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Explicar por qué Odoo separa la vista (XML) de la lógica (Python)
- Construir vista de formulario y lista para el modelo Libro
- Conectar vistas a una acción de ventana (`ir.actions.act_window`)
- Ubicar la acción dentro de un menú (`ir.ui.menu`)

### 📖 Teoría

Cada vista es un registro del modelo técnico `ir.ui.view` con: `model` (a qué modelo aplica), `type` (form, tree, kanban...) y `arch` (XML visual).

**Piezas necesarias para que un usuario acceda:**
1. **Vista** (`ir.ui.view`) — define el layout
2. **Acción de ventana** (`ir.actions.act_window`) — dice "al abrir esto, muestra este modelo"
3. **Menú** (`ir.ui.menu`) — enlace a la acción en la barra de navegación

#### Diagrama: vista → menú

```
ir.ui.menu (menú visible)
      |
      | 'action'
      v
ir.actions.act_window
      |
      | 'res_model': 'biblioteca.libro'
      | 'view_mode': 'tree,form'
      v
ir.ui.view (tree)     ir.ui.view (form)
      |                      |
      v                      v
 Lista de libros       Formulario de un libro
```

### 💻 Código explicado

```xml
<!-- views/libro_views.xml -->
<odoo>
    <!-- Vista de lista -->
    <record id="view_libro_tree" model="ir.ui.view">
        <field name="name">biblioteca.libro.tree</field>
        <field name="model">biblioteca.libro</field>
        <field name="arch" type="xml">
            <tree>
                <field name="titulo"/>
                <field name="genero"/>
                <field name="anio_publicacion"/>
                <field name="disponible"/>
            </tree>
        </field>
    </record>

    <!-- Vista de formulario -->
    <record id="view_libro_form" model="ir.ui.view">
        <field name="name">biblioteca.libro.form</field>
        <field name="model">biblioteca.libro</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="titulo"/>
                        <field name="isbn"/>
                        <field name="genero"/>
                        <field name="anio_publicacion"/>
                        <field name="disponible"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Acción de ventana -->
    <record id="action_libro" model="ir.actions.act_window">
        <field name="name">Libros</field>
        <field name="res_model">biblioteca.libro</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

```xml
<!-- views/menus.xml -->
<odoo>
    <menuitem id="menu_biblioteca_root" name="Biblioteca"/>
    <menuitem id="menu_libro" name="Libros"
              parent="menu_biblioteca_root"
              action="action_libro"/>
</odoo>
```

### ✅ Tu progreso en Día 4

| Concepto | Estado |
|----------|--------|
| Vista tree para Libro | ✅ |
| Vista form para Libro | ✅ |
| Vista tree para Autor | ✅ |
| Vista form para Autor | ✅ |
| Acción `biblioteca_libro_action` | ✅ |
| Acción `biblioteca_autor_action` | ✅ |
| Menú raíz "Biblioteca" | ✅ |
| Submenú "Libros" | ✅ |
| Submenú "Autores" | ✅ |

### 🐳 Comandos Docker

```powershell
# Actualizar módulo con nuevas vistas/menús
docker compose run --rm odoo -d postgres -u biblioteca --stop-after-init

# Reiniciar Odoo para ver cambios
docker compose restart odoo
```

### 🧪 Reto
Crea la vista de lista y formulario para el modelo **Autor** (del reto del Día 3), con su propia acción y menú dentro de "Biblioteca". Ambos modelos deben ser navegables desde el mismo menú raíz.

### ⚠️ Errores comunes
- Olvidar `type="xml"` en el campo `arch` — Odoo interpreta el contenido como texto plano
- Repetir un mismo `id` en dos archivos distintos, sobrescribiendo una vista sin darte cuenta
- Definir la acción pero olvidar el `menuitem` — la acción existe pero nadie puede llegar a ella

### 📌 Buenas prácticas
- Prefijar IDs con el nombre del modelo (`view_libro_tree`, `view_libro_form`)
- Un archivo de vistas por modelo y un archivo aparte solo para menús
- Agrupar campos relacionados dentro de `<group>` en el formulario

### 📝 Resumen
Una vista nunca funciona sola: necesita una acción que la invoque y un menú que la haga alcanzable. Hoy el modelo Libro se convierte en un CRUD visual completo.

---

## Día 5 — Seguridad: Grupos y Permisos

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Explicar por qué TODO modelo necesita una entrada de acceso explícita
- Crear el archivo `ir.model.access.csv` del módulo Biblioteca
- Definir grupos de seguridad propios (Bibliotecario, Lector)
- Entender la diferencia entre permisos por modelo y reglas por registro

### 📖 Teoría

Dos capas de seguridad:

1. **Permisos por modelo** (`ir.model.access.csv`) — ¿puede este grupo leer/crear/escribir/borrar en este modelo?
2. **Reglas de registro** (`ir.rule`) — ¿qué registros específicos puede ver? Se implementan con un `domain_force`

> Sin al menos una línea en `ir.model.access.csv` para un modelo, ese modelo es **completamente inaccesible** para cualquier usuario no administrador.

#### Diagrama: las dos capas

```
Usuario → Grupo (res.groups)
               |
     -------------------------
     |                       |
     v                       v
ir.model.access.csv      ir.rule
"¿puede operar en        "¿qué registros
 este modelo?"             específicos ve?"
     |                       |
     v                       v
Todo o nada              Filtro (domain)
```

### 💻 Código explicado

**security/ir.model.access.csv:**
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_biblioteca_libro_bibliotecario,biblioteca.libro.bibliotecario,model_biblioteca_libro,biblioteca.group_bibliotecario,1,1,1,0
access_biblioteca_libro_lector,biblioteca.libro.lector,model_biblioteca_libro,biblioteca.group_lector,1,0,0,0
```

**security/biblioteca_security.xml** (grupos y reglas):
```xml
<odoo>
    <record id="group_lector" model="res.groups">
        <field name="name">Biblioteca / Lector</field>
    </record>

    <record id="group_bibliotecario" model="res.groups">
        <field name="name">Biblioteca / Bibliotecario</field>
        <field name="implied_ids" eval="[(4, ref('group_lector'))]"/>
    </record>

    <record id="rule_libro_solo_disponibles" model="ir.rule">
        <field name="name">Lector: solo libros disponibles</field>
        <field name="model_id" ref="model_biblioteca_libro"/>
        <field name="domain_force">[('disponible', '=', True)]</field>
        <field name="groups" eval="[(4, ref('group_lector'))]"/>
    </record>
</odoo>
```

> **Orden en `data` del manifest:** `security/biblioteca_security.xml` **antes** que `security/ir.model.access.csv` — los grupos deben existir antes de que el CSV los referencie.

### ✅ Tu progreso en Día 5

| Concepto | Estado |
|----------|--------|
| `ir.model.access.csv` con permisos básicos | ✅ |
| Grupo "Biblioteca / Lector" | ⬜ Pendiente |
| Grupo "Biblioteca / Bibliotecario" | ⬜ Pendiente |
| Regla: Lector solo ve libros disponibles | ⬜ Pendiente |
| Archivo `security/biblioteca_security.xml` | ⬜ Pendiente |
| Permisos para modelo Autor | ⬜ Pendiente |

### 🐳 Comandos Docker

```powershell
# Actualizar módulo con seguridad
docker compose run --rm odoo -d postgres -u biblioteca --stop-after-init

docker compose restart odoo
```

**Probar con usuarios reales:**
1. Ve a Ajustes → Usuarios y compañías → Usuarios
2. Crea un usuario de prueba con grupo "Biblioteca / Lector"
3. Inicia sesión en ventana privada con ese usuario
4. Verifica que solo ve libros disponibles y no puede crear

### 🧪 Reto
Agrega líneas de acceso para el modelo **Autor**: el grupo Lector solo puede leer, el grupo Bibliotecario puede crear y editar (pero no borrar). Verifica con usuarios de prueba.

### ⚠️ Errores comunes
- Crear un modelo nuevo y olvidar su línea en `ir.model.access.csv` — queda invisible
- Invertir el orden en `data`: si `ir.model.access.csv` se carga antes que `biblioteca_security.xml`, los grupos no existen y falla
- Confundir `perm_write` (editar existentes) con `perm_create` (crear nuevos)

### 📌 Buenas prácticas
- Nombrar IDs de acceso: `access_<modelo>_<grupo>`
- Diseñar grupos pensando en roles de negocio, no en personas
- Probar siempre con un usuario de **bajo privilegio**, no solo como administrador

### 📝 Resumen
La seguridad en Odoo tiene dos capas: `ir.model.access.csv` (permisos sobre el modelo completo) e `ir.rule` (filtro por registro). Ningún modelo es accesible por defecto.

---

## Día 6 — Repaso General + Proyecto Biblioteca Completo

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Integrar todo lo construido en un módulo coherente
- Verificar que cada pieza funciona en conjunto
- Cerrar la Semana 1 con un entregable documentado

### 📖 Teoría

Hoy no se aprende un concepto nuevo: se verifica que las piezas **encajan como un sistema único**. Es el ciclo de vida real de un módulo Odoo: instalar → poblar → exponer interfaz → restringir → documentar.

#### Arquitectura final del módulo

```
biblioteca/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── libro.py
│   ├── autor.py
│   └── editorial.py       (Reto Día 2)
├── views/
│   ├── libro_views.xml
│   ├── autor_views.xml
│   └── menus.xml
├── security/
│   ├── biblioteca_security.xml
│   └── ir.model.access.csv
└── README.md
```

### ✅ Checklist de integración

| Requisito | Estado |
|-----------|--------|
| El módulo se instala desde cero sin errores en el log | ⬜ |
| Existen al menos 2 modelos: Libro y Autor | ✅ |
| Modelo Editorial adicional (Reto Día 2) | ⬜ |
| Ambos modelos tienen vista tree + form | ✅ |
| Menú raíz "Biblioteca" con submenús funcionales | ✅ |
| Grupo "Lector" (solo lectura) | ⬜ |
| Grupo "Bibliotecario" (lectura + escritura, sin borrar) | ⬜ |
| Regla: Lector solo ve libros disponibles | ⬜ |
| Probado con usuario de prueba no administrador | ⬜ |
| README.md documentado | ⬜ |

### 🐳 Comandos Docker — prueba desde cero

```powershell
# Detener todo
docker compose down

# Conectar a PostgreSQL y crear BD limpia
docker compose run --rm db psql -U db_user_odoo -c "CREATE DATABASE bootcamp_verificacion OWNER db_user_odoo;"

# Instalar módulo en BD nueva
docker compose run --rm odoo -d bootcamp_verificacion -i biblioteca --stop-after-init

# Revisar logs: no debe haber ERROR ni CRITICAL
docker compose logs --tail=50 odoo
```

### 🧪 Reto de cierre
Escribe el **README.md** del proyecto Biblioteca documentando:
1. Cómo instalar el módulo desde cero
2. Qué modelos existen y para qué sirven
3. Qué grupos de seguridad existen y qué puede hacer cada uno
4. Decisiones de diseño (ej. por qué Bibliotecario hereda de Lector)

### ⚠️ Errores comunes al integrar
- Dejar datos de prueba creados desde el shell mezclados con datos reales
- Detectar error de seguridad y "arreglarlo" abriendo permisos totales en vez de revisar la regla
- Dar por cerrada la semana sin probar con un usuario no administrador

### 📌 Buenas prácticas de cierre
- Versiona este punto con Git: `git commit -m "Semana 1: módulo Biblioteca completo"`
- Revisa el log completo al menos una vez, no solo la interfaz
- Guarda este README como plantilla para las próximas semanas

### 📝 Resumen de la Semana 1

En cinco días, el módulo Biblioteca pasó de no existir a ser una aplicación instalable con:
- Modelos propios respaldados por tablas PostgreSQL
- Interfaz navegable con lista y formulario
- Seguridad diferenciada por roles de negocio

El patrón que queda instalado: **comprender antes de programar, verificar cada pieza aislada, integrar y validar al final**.