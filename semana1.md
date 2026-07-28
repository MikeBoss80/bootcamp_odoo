BOOTCAMP ODOO DEVELOPER & INTEGRATIONS
Semana 1 — Comprender Odoo
Las 6 clases completas, día a día
Objetivo de la semana	Comprender cómo funciona un ERP y dominar la arquitectura básica de Odoo
Resultado esperado	Módulo Biblioteca instalable, con modelos, vistas y seguridad por roles
Días incluidos	Día 1 a Día 6 — 18 horas de contenido
Formato	Objetivos · Teoría · Diagramas · Código explicado · Ejercicio guiado · Reto · Errores comunes · Buenas prácticas · Resumen
 Índice de la Semana


 Día 1 — ¿Qué es un ERP? Introducción a Odoo y Arquitectura General
Semana: 1 — Comprender Odoo   |   Horas: 3 (Comprender · Construir · Consolidar)
Objetivos del día
•	Explicar con tus propias palabras qué es un ERP y qué problema de negocio resuelve.
•	Entender por qué Odoo se organiza en módulos independientes que se comunican entre sí.
•	Instalar Odoo en modo desarrollo y navegar su interfaz como usuario y como administrador.
•	Identificar las carpetas principales del código fuente de Odoo (addons, odoo-bin, config).
Teoría
Antes de escribir una sola línea de código, hay que entender el problema. Una empresa pequeña suele manejar sus ventas en una hoja de cálculo, su inventario en otra, y su contabilidad en un software distinto. El resultado: información duplicada, desactualizada y sin comunicación entre áreas. Un ERP (Enterprise Resource Planning) resuelve esto centralizando todos los procesos de negocio — ventas, compras, inventario, contabilidad, recursos humanos — en una sola base de datos compartida.
Odoo es un ERP de código abierto construido sobre Python y PostgreSQL, organizado como un conjunto de aplicaciones (módulos) que se instalan según la necesidad de cada empresa. La clave de su arquitectura es que cada módulo puede extender a otro sin modificarlo: el módulo de Ventas puede leer datos del módulo de Inventario, y el módulo de Contabilidad puede reaccionar a lo que ocurre en Ventas, todo sin que ninguno de los tres necesite conocer los detalles internos del otro.
Esto se logra gracias a tres pilares que iremos profundizando durante todo el bootcamp:
•	El ORM (Object-Relational Mapping): convierte clases de Python en tablas de PostgreSQL, para que nunca escribas SQL directamente.
•	Las vistas XML: definen cómo se ve cada modelo en pantalla (formulario, lista, kanban), separadas del código Python.
•	El sistema de seguridad: controla qué puede ver y hacer cada usuario, según su grupo.
Diagrama: arquitectura general de Odoo
La petición de un usuario viaja siempre por la misma ruta, sin importar qué módulo esté usando:
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
Cada módulo (addon) sigue esta misma estructura interna de carpetas:
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
Código explicado
El archivo más importante de cualquier módulo es el manifest, porque es lo primero que Odoo lee para saber si el módulo existe y qué necesita para funcionar:
# __manifest__.py
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
•	'depends': ['base'] — le dice a Odoo que este módulo necesita que el módulo base esté instalado antes; 'base' contiene el núcleo del ORM y del sistema de usuarios.
•	'data' — lista, en orden, los archivos XML/CSV que Odoo debe cargar al instalar o actualizar el módulo. El orden importa: la seguridad normalmente se carga antes que las vistas.
•	'application': True — sin esta línea, el módulo existiría pero no aparecería como una app independiente en el menú.
Ejercicio guiado
Vamos a instalar Odoo en modo desarrollador y crear la carpeta base (vacía) del módulo Biblioteca, paso a paso:

**Linux / macOS:**
```bash
# 1. Clonar el código fuente de Odoo
git clone https://github.com/odoo/odoo.git --branch 17.0 --depth 1

# 2. Crear un entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r odoo/requirements.txt

# 3. Levantar PostgreSQL (vía Docker, para no ensuciar el sistema)
docker run -d --name odoo-db -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -p 5432:5432 postgres:15

# 4. Arrancar Odoo apuntando a una carpeta propia de módulos
python odoo/odoo-bin --addons-path=odoo/addons,custom_addons -d bootcamp_db
```

**Windows (PowerShell):**
```powershell
# 1. Clonar el código fuente de Odoo
git clone https://github.com/odoo/odoo.git --branch 17.0 --depth 1

# 2. Crear un entorno virtual e instalar dependencias
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r odoo/requirements.txt

# 3. Levantar PostgreSQL (vía Docker, para no ensuciar el sistema)
docker run -d --name odoo-db -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -p 5432:5432 postgres:15

# 4. Solucionar compilación CSS en Windows (ver Errores comunes)
echo "import sass" > venv\Lib\site-packages\zz_preload_sass.pth

# 5. Arrancar Odoo apuntando a una carpeta propia de módulos
.\venv\Scripts\python odoo/odoo-bin --addons-path=odoo/addons,custom_addons -d bootcamp_db
```

Con el servidor corriendo, entra a http://localhost:8069, crea la base de datos y activa el modo desarrollador desde Ajustes → Activar modo desarrollador. Luego crea la carpeta custom_addons/biblioteca con la estructura mostrada en el diagrama anterior (por ahora solo el manifest y los __init__.py vacíos).
Reto del día
Sin ayuda: instala Odoo desde cero en tu máquina, crea el módulo biblioteca vacío (solo estructura de carpetas y manifest) y logra que aparezca en la lista de Aplicaciones de Odoo (aunque todavía no haga nada). Documenta en un README.md los 3 problemas que se te presentaron durante la instalación y cómo los resolviste.
Errores comunes
•	Olvidar 'installable': True — el módulo existe en el disco pero Odoo nunca lo muestra en la lista de apps.
•	No reiniciar el servidor con -u nombre_modulo después de crear el manifest por primera vez, por lo que Odoo no detecta el módulo nuevo.
•	Confundir 'depends' con un import de Python: son dependencias entre módulos de Odoo, no librerías de Python.
•	**Error de compilación CSS en Windows (`Could not execute command 'sassc'`)** — 
Odoo 17.0 intenta compilar SCSS a CSS usando la herramienta `sassc` (CLI) si no detecta `libsass` (el binding Python). En Windows `sassc` no existe como ejecutable nativo, y el binding `libsass` puede quedar desactivado si el bytecode (`.pyc`) se compiló antes de instalarlo.

**Solución:** crear un archivo `.pth` en el venv para que `sass` se precargue automáticamente al iniciar Python:
```powershell
echo "import sass" > venv\Lib\site-packages\zz_preload_sass.pth
```
Esto garantiza que cuando Odoo ejecute `import sass as libsass` en `assetsbundle.py`, el módulo ya esté cargado en `sys.modules` y nunca caiga al fallback de `sassc`.

Si el error persiste, limpiar la caché de assets en la base de datos:
```powershell
.\venv\Scripts\python -c "import psycopg2; c=psycopg2.connect(host='localhost',user='odoo',password='odoo',dbname='bootcamp_db'); cur=c.cursor(); cur.execute(\"DELETE FROM ir_attachment WHERE name LIKE '%assets%'\"); c.commit(); c.close()"
```

*(Este problema es exclusivo de Windows; en Linux/macOS no ocurre porque `sassc` está disponible como paquete del sistema)*

Buenas prácticas
•	Nombrar los módulos en snake_case y en singular relacionado al dominio de negocio (ej. biblioteca, no libro_modulo_v2).
•	Nunca modificar un módulo estándar de Odoo directamente: siempre se extiende desde un módulo propio (esto se profundiza en la Semana 2).
•	Versionar el proyecto con Git desde el primer día, incluso si el módulo todavía está vacío.
Resumen del día
Un ERP centraliza los procesos de una empresa en una sola base de datos. Odoo lo logra mediante módulos independientes que se comunican a través del ORM, sin necesidad de conocerse entre sí. Cada módulo sigue una estructura de carpetas estándar (models, views, security) y se registra ante Odoo mediante su manifest. Hoy dejaste corriendo tu primer servidor Odoo y el esqueleto del proyecto que evolucionará durante las próximas 4 semanas.
 Día 2 — Arquitectura de Módulos: Estructura de Carpetas, Manifest e __init__.py
Semana: 1 — Comprender Odoo   |   Horas: 3 (Comprender · Construir · Consolidar)
Objetivos del día
•	Explicar por qué Odoo carga los módulos en un orden específico y no al azar.
•	Dominar todas las claves relevantes del __manifest__.py, no solo las básicas vistas el Día 1.
•	Entender la cadena de imports de __init__.py, desde la raíz del módulo hasta cada archivo de Python.
•	Distinguir los estados de un módulo (no instalado, instalado, por actualizar) y cuándo se dispara cada uno.
Teoría
El Día 1 dejó un módulo vacío reconocido por Odoo. Hoy se abre esa caja: ¿qué hace Odoo exactamente al arrancar, y por qué el orden de las carpetas y de los imports no es una convención estética sino un requisito técnico?
Cuando el servidor arranca, Odoo recorre cada carpeta dentro de los addons-path buscando un archivo __manifest__.py. Si lo encuentra, lee su contenido como un diccionario de Python (no lo ejecuta como lógica de negocio, solo lo evalúa como datos) y registra el módulo en la tabla ir.module.module, con estado 'no instalado'. El código Python del módulo (los modelos) no se carga en memoria hasta que el módulo se instala o actualiza explícitamente.
La clave 'depends' del manifest no es informativa: es la que determina el orden de carga. Si el módulo A depende de B, Odoo garantiza que todo el código y los datos de B ya existen en memoria y en la base de datos antes de tocar A. Esto es lo que permite que un módulo herede o extienda modelos y vistas de otro sin errores de 'modelo no encontrado'.
•	'data' vs 'demo': 'data' se carga siempre que el módulo se instala; 'demo' solo se carga si la base de datos se creó con datos de demostración activados — nunca deben mezclarse datos de ejemplo con datos de configuración real.
•	'auto_install': True convierte al módulo en un 'módulo puente' que se instala solo automáticamente en cuanto todas sus dependencias están instaladas (Odoo lo usa mucho para conectar dos apps, por ejemplo sale_stock).
•	'application': True vs un módulo normal: ambos son iguales técnicamente, la única diferencia es que uno aparece como ícono en el launcher principal de aplicaciones.
Diagrama: cadena de imports y orden de carga
__manifest__.py  ---- Odoo lee esto primero, sin ejecutar Python
     |
     | 'depends': ['base', 'mail']  --> resuelve el grafo de dependencias
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
models/libro.py   models/autor.py   <-- aquí sí se ejecuta código Python real
Si se omite una línea en cualquier eslabón de esta cadena, el archivo simplemente nunca se ejecuta — es el error más frecuente de un modelo 'que no aparece' aunque el archivo exista en disco.
Código explicado
Un manifest más completo que el visto el Día 1, con las claves que se usarán durante todo el bootcamp:
# __manifest__.py
{
    'name': 'Biblioteca',
    'version': '1.0.0',
    'category': 'Custom/Biblioteca',
    'summary': 'Gestión de libros, autores y préstamos',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/libro_views.xml',
        'views/biblioteca_menus.xml',
    ],
    'demo': [
        'demo/libro_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
Y la cadena de __init__.py correspondiente:
# __init__.py  (raíz del módulo)
from . import models
 
# models/__init__.py
from . import libro
from . import autor
•	'depends': ['base', 'mail'] — se agrega 'mail' porque más adelante (Semana 2) el módulo usará el chatter (historial de mensajes) que provee ese módulo estándar.
•	'category' organiza el módulo dentro del selector de Apps de Odoo; no afecta el funcionamiento, solo la presentación.
•	'license' es obligatorio desde versiones recientes de Odoo: sin esta clave, el módulo no pasa la validación al instalar.
Ejercicio guiado
Vamos a comprobar en vivo qué ocurre si se rompe cada eslabón de la cadena, para verlo una sola vez y reconocerlo siempre:
# 1. Comenta la línea 'from . import autor' en models/__init__.py
# 2. Reinicia el servidor con -u biblioteca
# 3. Observa: el modelo Autor no genera error, simplemente no existe para Odoo
 
python odoo-bin --addons-path=odoo/addons,custom_addons -d bootcamp_db -u biblioteca
 
# 4. Verifica en el shell que el modelo no está registrado:
python odoo-bin shell -d bootcamp_db
>>> env['biblioteca.autor']
# KeyError: 'biblioteca.autor'
Luego descomenta la línea, actualiza el módulo de nuevo y confirma que env['biblioteca.autor'] ya responde correctamente.
Reto del día
Sin ayuda: agrega un tercer modelo (Editorial) al módulo Biblioteca, con su propio archivo en models/, su import correspondiente en models/__init__.py, y una entrada en el manifest para su futura vista. Verifica en el shell que Odoo lo reconoce tras un -u biblioteca.
Errores comunes
•	Olvidar el import en __init__.py después de crear un archivo de modelo nuevo — el error más común de toda la semana.
•	Poner archivos en 'demo' que en realidad son configuración necesaria para que el módulo funcione (esto rompe el módulo en bases de datos sin datos de demostración).
•	Modificar el manifest y olvidar que los cambios en 'depends' requieren reiniciar el servidor, no solo actualizar el módulo.
Buenas prácticas
•	Un archivo de modelo por entidad de negocio (libro.py, autor.py), nunca todos los modelos en un solo archivo gigante.
•	Mantener 'depends' con el mínimo necesario: cada dependencia extra es complejidad y tiempo de carga adicional.
•	Revisar el log del servidor al arrancar: Odoo reporta claramente si un módulo falló al cargar y por qué.
Resumen del día
El manifest es el contrato entre el módulo y Odoo: declara de qué depende, qué datos carga y cómo se presenta. La cadena de __init__.py es lo que realmente pone en memoria el código Python. Entender este mecanismo evita el error más común de un desarrollador Odoo principiante: escribir código correcto que Odoo nunca llega a ejecutar porque falta un import.
 Día 3 — El ORM: Modelos, Campos Básicos y self.env
Semana: 1 — Comprender Odoo   |   Horas: 3 (Comprender · Construir · Consolidar)
Objetivos del día
•	Explicar qué hace el ORM de Odoo y por qué nunca se escribe SQL directamente en un módulo.
•	Declarar un modelo con _name, _description y los tipos de campo básicos.
•	Entender qué es self.env y usarlo para crear y consultar registros.
•	Crear la primera tabla real en PostgreSQL a partir de una clase de Python.
Teoría
Hasta ahora el módulo Biblioteca existe, arranca y carga sus archivos, pero no tiene ninguna tabla propia en la base de datos. Hoy se crea la primera: el modelo Libro. Para eso hay que entender el ORM (Object-Relational Mapping), la pieza que traduce una clase de Python en una tabla de PostgreSQL sin que el desarrollador escriba una sola sentencia SQL.
Cada modelo es una clase de Python que hereda de models.Model. Dos atributos son obligatorios en la práctica: _name, que define el identificador técnico del modelo (y el nombre de la tabla, reemplazando los puntos por guiones bajos: biblioteca.libro se convierte en la tabla biblioteca_libro), y _description, una etiqueta legible que Odoo usa en mensajes y logs.
Los campos de la clase (fields.Char, fields.Integer, etc.) se traducen, cada uno, en una columna de esa tabla. Cuando el módulo se instala o se actualiza, el ORM compara la definición de la clase con la estructura real de la tabla en PostgreSQL y aplica los cambios necesarios (crear columnas nuevas, por ejemplo) automáticamente — este proceso se llama, dentro de Odoo, actualización del esquema.
•	self.env es la puerta de entrada a todo lo demás en Odoo: el entorno de ejecución actual. self.env['modelo'] devuelve el modelo con el que se puede trabajar (crear, buscar, leer).
•	self.env.user devuelve el usuario que está ejecutando la acción; self.env.company, la compañía activa. Estos datos son fundamentales para la seguridad y la lógica multiempresa que se verá más adelante.
•	Un recordset (el resultado de una búsqueda o creación) no es una lista de diccionarios: es una colección especial de registros del mismo modelo, sobre la cual se puede iterar, filtrar y acceder a los campos como si fueran atributos de Python (libro.titulo, no libro['titulo']).
Diagrama: de la clase Python a la tabla PostgreSQL
class Libro(models.Model):              tabla real en PostgreSQL: biblioteca_libro
    _name = 'biblioteca.libro'    ---->  ------------------------------------------
    _description = 'Libro'              | id | titulo | anio | disponible | ...  |
                                         ------------------------------------------
    titulo = fields.Char()        ---->  columna 'titulo'   (varchar)
    anio = fields.Integer()       ---->  columna 'anio'     (integer)
    disponible = fields.Boolean() ---->  columna 'disponible' (boolean)
 
    # 'id' se crea siempre automáticamente, nunca se declara a mano
Código explicado
El primer modelo real del bootcamp:
# models/libro.py
from odoo import models, fields
 
 
class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro de la biblioteca'
    _rec_name = 'titulo'          # qué campo se muestra al referenciar el registro
 
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
•	required=True hace que el ORM impida guardar el registro sin ese valor, tanto desde la interfaz como desde código.
•	default=True o default=fields.Date.today asigna un valor automático cuando no se especifica ninguno al crear el registro.
•	fields.Selection define un conjunto cerrado de opciones — a diferencia de Char, no admite cualquier texto libre.
•	_rec_name le dice a Odoo qué campo usar cuando este modelo se muestre como texto dentro de otro (por ejemplo, dentro de un campo Many2one apuntando a Libro).
Ejercicio guiado
Con el modelo ya declarado, se actualiza el módulo y se prueba el ORM directamente desde el shell interactivo, sin pasar todavía por ninguna vista:
# Actualizar el módulo para crear la tabla en PostgreSQL
python odoo-bin --addons-path=odoo/addons,custom_addons -d bootcamp_db -u biblioteca --stop-after-init
 
# Entrar al shell interactivo
python odoo-bin shell -d bootcamp_db
 
>>> libro = env['biblioteca.libro'].create({
...     'titulo': 'Cien años de soledad',
...     'anio_publicacion': 1967,
...     'genero': 'ficcion',
... })
>>> libro.titulo
'Cien años de soledad'
>>> env['biblioteca.libro'].search([('genero', '=', 'ficcion')])
biblioteca.libro(1,)
Confirma en pgAdmin o psql que la tabla biblioteca_libro ya existe en PostgreSQL con las columnas correspondientes a cada campo declarado.
Reto del día
Sin ayuda: crea el modelo Autor (biblioteca.autor) con al menos nombre, nacionalidad y fecha_nacimiento, créalo en el shell, y consulta desde el shell todos los autores cuya nacionalidad sea la tuya usando search(). Todavía no se relaciona con Libro — eso ocurre en la Semana 2.
Errores comunes
•	Usar _name con puntos incorrectos o mayúsculas (biblioteca.Libro en vez de biblioteca.libro) — Odoo es sensible a esto y genera nombres de tabla inconsistentes.
•	Olvidar el -u nombre_modulo tras cambiar los campos de un modelo — sin esa actualización, la tabla en PostgreSQL no refleja los cambios del código.
•	Confundir create() (que devuelve un recordset) con simplemente pasar un diccionario: fuera del ORM, ese diccionario no tiene ningún significado para Odoo.
Buenas prácticas
•	Siempre declarar _description: aparece en logs, en mensajes de error y en el selector de modelos de Ajustes técnicos.
•	Usar string= explícito en cada campo aun cuando Odoo pueda inferir una etiqueta — hace el código más claro y evita etiquetas técnicas feas en pantalla (p. ej. 'Anio Publicacion' en vez de 'Año de publicación').
•	Probar cada modelo nuevo en el shell antes de construir su vista — aísla si un problema es del modelo o de la interfaz.
Resumen del día
El ORM traduce clases de Python en tablas reales de PostgreSQL: cada campo declarado se convierte en una columna. self.env es la puerta de entrada para crear y consultar esos datos desde código, y devuelve siempre recordsets, no diccionarios. Hoy quedó creada la primera tabla real del proyecto Biblioteca, verificada tanto desde el shell de Odoo como directamente en la base de datos.
 Día 4 — Vistas XML: Formulario, Lista, Acciones de Ventana y Menús
Semana: 1 — Comprender Odoo   |   Horas: 3 (Comprender · Construir · Consolidar)
Objetivos del día
•	Explicar por qué Odoo separa completamente la vista (XML) de la lógica (Python).
•	Construir una vista de formulario y una vista de lista para el modelo Libro.
•	Conectar esas vistas a una acción de ventana (ir.actions.act_window).
•	Ubicar esa acción dentro de un menú navegable (ir.ui.menu).
Teoría
El modelo Libro ya existe y tiene datos, pero solo es accesible desde el shell — un usuario normal no puede verlo ni editarlo. Hoy se cierra ese círculo con las vistas: las plantillas XML que le dicen a Odoo cómo dibujar cada modelo en pantalla.
La separación entre modelo (Python) y vista (XML) no es una preferencia estética: permite que distintos módulos modifiquen cómo se ve un mismo modelo sin tocar su lógica, y es la base de la herencia de vistas que se estudiará en la Semana 2. Cada vista se guarda como un registro del modelo técnico ir.ui.view, con tres partes clave: model (a qué modelo aplica), type (form, tree/list, kanban, etc.) y arch (el XML que define la estructura visual).
Para que una vista sea alcanzable por un usuario, se necesitan dos piezas adicionales: una acción de ventana (ir.actions.act_window), que dice 'al abrir esto, muestra este modelo con estas vistas', y un menú (ir.ui.menu), que dice 'aquí, en la barra de navegación, hay un enlace a esa acción'.
•	Vista de lista (tree): muestra varios registros en formato tabla, pensada para explorar y comparar.
•	Vista de formulario (form): muestra un solo registro con todos sus campos, pensada para crear y editar en detalle.
•	Una misma acción de ventana puede combinar varias vistas (por ejemplo, lista + formulario): Odoo pasa de una a otra automáticamente al hacer clic en un registro de la lista.
Diagrama: de la vista al menú
ir.ui.menu (menú visible)
      |
      | 'action'
      v
ir.actions.act_window (acción de ventana)
      |
      | 'res_model': 'biblioteca.libro'
      | 'view_mode': 'tree,form'
      v
ir.ui.view (type='tree')     ir.ui.view (type='form')
      |                             |
      v                             v
Lista de libros              Formulario de un libro
Código explicado
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
<!-- views/biblioteca_menus.xml -->
<odoo>
    <menuitem id="menu_biblioteca_root" name="Biblioteca"/>
    <menuitem id="menu_libro" name="Libros"
              parent="menu_biblioteca_root"
              action="action_libro"/>
</odoo>
•	El id de cada record (view_libro_tree, action_libro) es un identificador externo único dentro del módulo — se usa para referenciar ese registro desde otros XML, incluso desde otros módulos (clave para la herencia de vistas).
•	'view_mode': 'tree,form' — el orden importa: define que al abrir la acción se muestre primero la lista, y que al hacer clic en un registro se pase al formulario.
•	menuitem sin 'action' (menu_biblioteca_root) actúa solo como carpeta contenedora; el que sí abre algo es menu_libro, gracias a su atributo action.
Ejercicio guiado
Agrega ambos archivos XML al manifest, actualiza el módulo y navega a la app:
# En __manifest__.py, dentro de 'data':
'data': [
    'security/ir.model.access.csv',
    'views/libro_views.xml',
    'views/biblioteca_menus.xml',
],
 
# Actualizar el módulo
python odoo-bin --addons-path=odoo/addons,custom_addons -d bootcamp_db -u biblioteca --stop-after-init
Con el servidor corriendo, entra a la interfaz, activa el modo desarrollador si aún no lo hiciste, y busca 'Biblioteca' en el menú principal de apps: debe aparecer la lista de libros creados desde el shell el Día 3, y debe poder crearse uno nuevo desde el botón Nuevo.
Reto del día
Sin ayuda: crea la vista de lista y de formulario para el modelo Autor del reto del Día 3, con su propia acción y su propio ítem de menú dentro de la carpeta 'Biblioteca'. Al finalizar, ambos modelos (Libro y Autor) deben ser navegables desde el mismo menú raíz.
Errores comunes
•	Olvidar el atributo type="xml" en el campo arch — sin él, Odoo interpreta el contenido como texto plano, no como estructura de vista.
•	Repetir un mismo id de record en dos archivos distintos del módulo, sobrescribiendo una vista sin darse cuenta.
•	Definir la acción de ventana pero olvidar el menuitem correspondiente: la acción existe, pero ningún usuario puede llegar a ella desde la interfaz.
Buenas prácticas
•	Prefijar los ids con el nombre del modelo (view_libro_tree, view_libro_form) para evitar colisiones cuando el módulo crezca.
•	Un archivo de vistas por modelo (libro_views.xml, autor_views.xml) y un archivo aparte solo para menús, siguiendo la convención estándar de Odoo.
•	Agrupar campos relacionados dentro de <group> en el formulario: mejora la lectura y es la base para diseños de dos columnas más adelante.
Resumen del día
Una vista XML nunca funciona sola: necesita una acción de ventana que la invoque y un menú que la haga alcanzable. Hoy el modelo Libro dejó de ser un dato invisible en el shell para convertirse en una pantalla real, navegable, con lista y formulario — el primer CRUD visual completo del bootcamp.
 Día 5 — Seguridad Básica: Grupos, ir.model.access.csv y Reglas de Registro
Semana: 1 — Comprender Odoo   |   Horas: 3 (Comprender · Construir · Consolidar)
Objetivos del día
•	Explicar por qué todo modelo en Odoo, sin excepción, necesita una entrada de acceso explícita.
•	Crear el archivo ir.model.access.csv del módulo Biblioteca.
•	Definir un grupo de seguridad propio (Bibliotecario) y restringir el acceso según ese grupo.
•	Entender la diferencia entre permisos por modelo (access rights) y permisos por registro (record rules).
Teoría
Hasta este punto, cualquier usuario administrador puede ver y editar los libros sin restricción. En una empresa real eso casi nunca es aceptable: un vendedor no debería poder borrar facturas, y un bibliotecario junior quizás no debería poder eliminar libros, solo consultarlos y prestarlos. Odoo resuelve esto con dos capas de seguridad complementarias.
•	Permisos por modelo (ir.model.access.csv): responden a la pregunta '¿puede este grupo de usuarios leer / crear / escribir / borrar registros de este modelo, en general?'. Es un permiso de todo o nada sobre el modelo completo.
•	Reglas de registro (ir.rule): responden a una pregunta más fina: '¿puede este usuario ver este registro en particular?'. Por ejemplo, que un vendedor solo vea sus propias ventas, no las de todo el equipo. Se implementan con un dominio (domain_force) que filtra automáticamente qué registros son visibles.
Sin al menos una línea en ir.model.access.csv para un modelo, ese modelo es completamente inaccesible para cualquier usuario que no sea administrador técnico — este es, de lejos, el error de seguridad más común en un módulo nuevo: no es que falte restringir, es que falta directamente el permiso mínimo para poder usarlo.
Los grupos de seguridad (res.groups) son la unidad sobre la que se construyen estos permisos: un usuario pertenece a uno o varios grupos, y cada línea de acceso o cada regla se asocia a un grupo, nunca a un usuario individual directamente.
Diagrama: las dos capas de seguridad
Usuario ---pertenece a---> Grupo (res.groups)
                               |
         -----------------------------------------------
         |                                              |
         v                                              v
  ir.model.access.csv                              ir.rule
  '¿puede leer/crear/escribir/                 '¿cuáles registros
   borrar en este modelo?'                       específicos puede ver?'
         |                                              |
         v                                              v
  Todo o nada sobre el modelo                Filtro (domain) sobre los registros
Código explicado
El archivo de permisos por modelo, en formato CSV, siempre con esta cabecera exacta:
# security/ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_biblioteca_libro_bibliotecario,biblioteca.libro.bibliotecario,model_biblioteca_libro,biblioteca.group_bibliotecario,1,1,1,0
access_biblioteca_libro_lector,biblioteca.libro.lector,model_biblioteca_libro,biblioteca.group_lector,1,0,0,0
•	model_id:id usa el id técnico generado automáticamente por Odoo para cada modelo: model_ + nombre del modelo con guiones bajos (model_biblioteca_libro para biblioteca.libro).
•	Los cuatro últimos valores son booleanos (1/0) en este orden fijo: leer, escribir, crear, borrar. El grupo Lector solo puede leer; el Bibliotecario puede todo menos borrar.
•	Si un usuario pertenece a ambos grupos, Odoo combina los permisos: prevalece el más permisivo entre las líneas que apliquen.
La definición de los grupos y una regla de registro de ejemplo:
<!-- security/biblioteca_security.xml -->
<odoo>
    <record id="group_lector" model="res.groups">
        <field name="name">Biblioteca / Lector</field>
    </record>
 
    <record id="group_bibliotecario" model="res.groups">
        <field name="name">Biblioteca / Bibliotecario</field>
        <field name="implied_ids" eval="[(4, ref('group_lector'))]"/>
    </record>
 
    <!-- Regla: un Lector solo ve los libros marcados como disponibles -->
    <record id="rule_libro_solo_disponibles" model="ir.rule">
        <field name="name">Lector: solo libros disponibles</field>
        <field name="model_id" ref="model_biblioteca_libro"/>
        <field name="domain_force">[('disponible', '=', True)]</field>
        <field name="groups" eval="[(4, ref('group_lector'))]"/>
    </record>
</odoo>
•	implied_ids hace que cualquier usuario en el grupo Bibliotecario herede automáticamente los permisos del grupo Lector — evita duplicar líneas de acceso para el rol 'superior'.
•	domain_force usa la misma sintaxis de dominio que search(): aquí filtra para que el grupo Lector nunca vea, en ninguna pantalla, un libro no disponible.
Ejercicio guiado
Con los archivos anteriores agregados al manifest (security/biblioteca_security.xml antes que ir.model.access.csv), se actualiza el módulo y se valida con dos usuarios distintos:
python odoo-bin --addons-path=odoo/addons,custom_addons -d bootcamp_db -u biblioteca --stop-after-init
 
# Desde Ajustes > Usuarios y compañías > Usuarios:
# 1. Crea un usuario de prueba y asígnale el grupo 'Biblioteca / Lector'
# 2. Inicia sesión con ese usuario en una ventana privada
# 3. Verifica que solo ve libros disponibles y que el botón Nuevo no permite guardar (perm_create=0)
Reto del día
Sin ayuda: agrega una tercera línea de acceso para el modelo Autor, de forma que el grupo Lector pueda leerlo pero no modificarlo, y el grupo Bibliotecario pueda además crear y editar autores (pero no borrarlos). Verifica ambos casos con el usuario de prueba creado en el ejercicio guiado.
Errores comunes
•	Crear un modelo nuevo y olvidar su línea en ir.model.access.csv — el modelo queda invisible incluso para el administrador si no hereda un grupo con acceso total.
•	Invertir el orden de los archivos en el manifest: si ir.model.access.csv se carga antes que biblioteca_security.xml, los grupos referenciados aún no existen y falla la instalación.
•	Confundir perm_write (editar campos de un registro existente) con perm_create (crear registros nuevos) — son permisos independientes.
Buenas prácticas
•	Nombrar los ids de acceso siguiendo el patrón access_<modelo>_<grupo> — hace evidente, a simple vista, a qué corresponde cada línea del CSV.
•	Diseñar los grupos pensando en roles de negocio (Lector, Bibliotecario), no en personas específicas.
•	Probar siempre con un usuario de prueba de bajo privilegio, nunca asumir que 'funciona' solo porque el administrador ve todo correctamente.
Resumen del día
La seguridad en Odoo se construye en dos capas: ir.model.access.csv decide si un grupo puede operar sobre un modelo en general, e ir.rule filtra qué registros específicos puede ver dentro de lo permitido. Ningún modelo es accesible por defecto — la ausencia de una línea de acceso es, en sí misma, una restricción total. Con esto, el módulo Biblioteca ya tiene roles reales y diferenciados, cerrando el conjunto de conceptos que se integrará mañana en el proyecto completo.
 Día 6 — Repaso General + Proyecto Biblioteca Completo
Semana: 1 — Comprender Odoo   |   Horas: 3 (Comprender · Construir · Consolidar)
Objetivos del día
•	Integrar en un solo módulo coherente todo lo construido en los cinco días anteriores.
•	Verificar, sin ayuda, que cada pieza (modelos, vistas, seguridad) funciona en conjunto y no solo aislada.
•	Cerrar la Semana 1 con un entregable documentado, tal como se pediría en un entorno profesional.
Teoría: de piezas sueltas a un módulo real
Durante la semana se construyó, día a día, cada pieza por separado: la arquitectura y el manifest (Día 2), el modelo con el ORM (Día 3), las vistas y la navegación (Día 4), y la seguridad por grupos (Día 5). Hoy no se aprende un concepto nuevo: se verifica que las piezas encajan como un sistema único, que es exactamente lo que se evalúa en un code review profesional antes de dar por cerrado un desarrollo.
Este es también el primer momento del bootcamp en el que se aplica, de forma completa, el ciclo de vida real de un módulo de Odoo: instalar, poblar con datos, exponer una interfaz, restringir por seguridad y documentar — el mismo ciclo que se repetirá, con mayor complejidad, en los proyectos de la Semana 2, 3 y 4.
Diagrama: arquitectura final del módulo Biblioteca
biblioteca/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── libro.py        (Día 3)
│   └── autor.py        (Reto del Día 3)
├── views/
│   ├── libro_views.xml       (Día 4)
│   ├── autor_views.xml       (Reto del Día 4)
│   └── biblioteca_menus.xml  (Día 4)
├── security/
│   ├── biblioteca_security.xml   (Día 5 — grupos y reglas)
│   └── ir.model.access.csv       (Día 5 — permisos por modelo)
└── README.md
El manifest final debe reflejar el orden de carga correcto, consolidando todo lo trabajado en la semana:
# __manifest__.py
{
    'name': 'Biblioteca',
    'version': '1.0.0',
    'category': 'Custom/Biblioteca',
    'summary': 'Gestión de libros, autores y préstamos',
    'depends': ['base', 'mail'],
    'data': [
        'security/biblioteca_security.xml',
        'security/ir.model.access.csv',
        'views/libro_views.xml',
        'views/autor_views.xml',
        'views/biblioteca_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
Por qué el orden de 'data' no es arbitrario
Los grupos deben existir antes de que ir.model.access.csv los referencie, y los modelos deben existir antes de que cualquier vista los use. Este orden es, en miniatura, el mismo principio de dependencias del Día 2 aplicado dentro de un mismo módulo.
Checklist de integración (a resolver sin ayuda)
•	El módulo se instala desde cero, en una base de datos nueva, sin errores en el log.
•	Existen al menos dos modelos relacionados por el negocio: Libro y Autor (la relación formal entre ambos se formaliza recién en la Semana 2; por ahora conviven en el mismo módulo).
•	Ambos modelos tienen vista de lista y de formulario, alcanzables desde el mismo menú raíz 'Biblioteca'.
•	Existen al menos dos grupos de seguridad (Lector, Bibliotecario) con permisos diferenciados verificados con un usuario de prueba real, no solo revisando el XML.
•	La regla de registro del Día 5 (solo libros disponibles para el grupo Lector) sigue funcionando tras los cambios de esta semana.
•	Existe un README.md que explica cómo instalar el módulo y qué decisiones se tomaron.
Ejercicio guiado: instalación desde cero
La prueba definitiva de que un módulo está bien construido es que se instale de forma limpia en una base de datos que nunca lo ha visto:
# Crear una base de datos completamente nueva
createdb -U odoo bootcamp_verificacion
 
# Instalar el módulo por primera vez en esa base
python odoo-bin --addons-path=odoo/addons,custom_addons \
  -d bootcamp_verificacion -i biblioteca --stop-after-init
 
# Revisar el log: no debe haber ninguna línea con nivel ERROR ni CRITICAL
Si esta instalación falla, casi siempre es por uno de los tres errores más comunes de la semana: un import olvidado (Día 2), un modelo referenciado en una vista antes de existir (Día 3/4), o una línea de seguridad que referencia un grupo que aún no se cargó (Día 5).
Reto de cierre de semana
Sin ayuda: escribe el README.md del proyecto Biblioteca, documentando (a) cómo instalar el módulo desde cero, (b) qué modelos existen y para qué sirven, (c) qué grupos de seguridad existen y qué puede hacer cada uno, y (d) qué decisiones de diseño tomaste que no eran obvias (por ejemplo, por qué el grupo Bibliotecario hereda del grupo Lector). Este README es, en sí mismo, la evidencia de que el bloque quedó comprendido y no solo copiado.
Errores comunes al integrar
•	Dejar datos de prueba creados desde el shell en días anteriores mezclados con los datos reales del módulo — antes de la entrega, se recomienda validar en una base de datos limpia (ver ejercicio guiado).
•	Detectar un error de seguridad (Día 5) e intentar 'arreglarlo' abriendo permisos totales al grupo Lector, en vez de revisar si la regla de registro está bien formulada.
•	Dar por cerrada la semana sin haber probado nunca con un usuario que no sea administrador — es el error de verificación más frecuente en proyectos reales.
Buenas prácticas de cierre
•	Versionar este punto del proyecto con un commit de Git claro (ej. 'Semana 1: módulo Biblioteca completo con seguridad por roles'), antes de empezar la Semana 2.
•	Revisar el log completo del servidor al menos una vez, no solo confiar en que la interfaz 'se ve bien'.
•	Guardar este README como plantilla: el mismo formato se reutilizará para documentar los proyectos de Inventario, Integraciones y el ERP Comercial final.
Resumen de la Semana 1
En cinco días, el módulo Biblioteca pasó de no existir a ser una aplicación instalable, con modelos propios respaldados por tablas reales en PostgreSQL, una interfaz navegable con lista y formulario, y seguridad diferenciada por roles de negocio. Más importante que el módulo en sí es el patrón que queda instalado: comprender la arquitectura antes de programar, verificar cada pieza de forma aislada, y solo al final integrar y validar el conjunto — el mismo patrón que se repetirá, semana a semana, durante el resto del bootcamp.
