# BOOTCAMP ODOO DEVELOPER & INTEGRATIONS
# Semana 3 — Integraciones y Automatización

**Objetivo de la semana:** pasar de desarrollar modelos y vistas a construir integraciones reales con Odoo, usando el módulo `biblioteca` como base práctica para aprender a conectarse con scripts externos, APIs, controllers y tareas programadas.
**Resultado esperado:** un flujo funcional de integración sobre `biblioteca` que permita leer datos, consumir APIs externas, exponer un endpoint propio y automatizar procesos con `ir.cron`.
**Días incluidos:** Día 1 a Día 7 — 16 a 18 horas de contenido

---

## Índice

- [Día 1 — Conexión externa con XML-RPC / JSON-RPC](#día-1--conexión-externa-con-xml-rpc--json-rpc)
- [Día 2 — CRUD desde un script externo](#día-2--crud-desde-un-script-externo)
- [Día 3 — Consumo de APIs externas desde Odoo](#día-3--consumo-de-apis-externas-desde-odoo)
- [Día 4 — Controllers y endpoint propio](#día-4--controllers-y-endpoint-propio)
- [Día 5 — Automatización con tareas programadas](#día-5--automatización-con-tareas-programadas)
- [Día 6 — Robustez, errores y logs](#día-6--robustez-errores-y-logs)
- [Día 7 — Debugging y lectura de código estándar](#día-7--debugging-y-lectura-de-código-estándar)
- [Día 8 — Repaso y cierre opcional](#día-8--repaso-y-cierre-opcional)

---

## Día 1 — Conexión externa con XML-RPC / JSON-RPC

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Entender cómo un script externo se autentica contra Odoo
- Conectar Python con Odoo sin usar la interfaz web
- Leer información real desde `biblioteca.libro`
- Diferenciar entre `common.authenticate` y `execute_kw`

### 📖 Teoría

Una integración externa normalmente empieza por una conexión segura a Odoo desde un script de Python. En este caso, el script no “simula” un usuario del navegador; en realidad usa la API de Odoo desde fuera.

El flujo básico es:

1. Conectarse al endpoint XML-RPC de Odoo
2. Autenticar el usuario con usuario, contraseña, base de datos y URL
3. Ejecutar un método sobre un modelo como `biblioteca.libro`

La idea principal es que Odoo expone una API que otros programas pueden consumir.

### 💻 Código explicado: script de conexión

```python
import xmlrpc.client

url = 'http://localhost:8069'
db = 'bootcamp_odoo_dev'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    libros = models.execute_kw(
        db, uid, password,
        'biblioteca.libro',
        'search_read',
        [[('name', '!=', False)]],
        {'fields': ['name', 'isbn', 'disponible'], 'limit': 3}
    )
    for libro in libros:
        print(libro['name'], ' | ', libro['isbn'])
else:
    print('No se pudo autenticar')
```

### ✅ Checklist del día

- [ ] Confirmar que Odoo está corriendo en el puerto 8069
- [ ] Crear un script `.py` local
- [ ] Probar autenticación con `common.authenticate`
- [ ] Obtener al menos 3 registros de `biblioteca.libro`
- [ ] Guardar el script en una carpeta de trabajo como `scripts/`

### 🧪 Reto

Modifica el script para que muestre solo libros disponibles y ordenados por nombre.

### ⚠️ Errores comunes
- Usar la base de datos incorrecta
- Confundir `username` con `uid`
- Intentar leer datos sin autenticación previa

### 📝 Resumen

Este día te enseña el punto de entrada real de una integración: conectar un sistema externo con Odoo y extraer datos de negocio.

---

## Día 2 — CRUD desde un script externo

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Crear registros desde un script externo
- Actualizar registros usando XML-RPC
- Entender la diferencia entre `create`, `write` y `unlink`
- Trabajar con datos reales del modelo `biblioteca.libro`

### 📖 Teoría

Una vez que el script puede leer datos, el siguiente paso es escribirlos. Aquí es donde una integración deja de ser “consulta” y pasa a ser “automatización real”.

Con Odoo RPC puedes ejecutar métodos del ORM igual que si lo hicieras desde Python dentro del servidor.

### 💻 Código explicado: crear y actualizar

```python
import xmlrpc.client

url = 'http://localhost:8069'
db = 'bootcamp_odoo_dev'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

libro_id = models.execute_kw(
    db, uid, password,
    'biblioteca.libro',
    'create',
    [{
        'name': 'Libro integrado',
        'isbn': 'RPC-001',
        'disponible': True,
        'genero': 'ficcion',
        'autor': 1,
    }]
)

print('Libro creado con ID:', libro_id)

models.execute_kw(
    db, uid, password,
    'biblioteca.libro',
    'write',
    [[libro_id], {'name': 'Libro integrado actualizado'}]
)
```

### ✅ Checklist del día

- [ ] Crear un libro desde el script
- [ ] Actualizar el nombre del libro creado
- [ ] Verificar el registro en Odoo
- [ ] Guardar el resultado del ID generado
- [ ] Dejar el script listo para reutilizar en el siguiente día

### 🧪 Reto

Haz que el script cree un libro, lo actualice y luego lo elimine si el usuario lo desea. Usa una bandera booleana para controlar el flujo.

### ⚠️ Errores comunes
- Enviar datos con nombres incorrectos de campo
- Intentar usar `write` sin pasar el ID del registro
- Crear registros sin cumplir los requisitos del modelo

### 📝 Resumen

Este día te enseña a manipular el ORM desde fuera de Odoo. Eso es esencial para cualquier integración de tipo ETL, sincronización o automatización.

---

## Día 3 — Consumo de APIs externas desde Odoo

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Entender cómo Odoo puede consultar una API externa
- Usar `requests` desde un método de un modelo
- Guardar datos obtenidos en el registro de `biblioteca.libro`
- Entender la diferencia entre consultar una API desde Python externo y desde el propio servidor Odoo

### 📖 Teoría

Hasta ahora el script externo era quien pedía datos a Odoo. En este día, invertimos el flujo: Odoo va a pedir datos a internet. Eso es común cuando necesitas validar información, obtener tipos de cambio, consultar catálogos o enriquecer registros.

Para esto se usa la librería `requests` dentro del entorno del servidor Odoo.

### 💻 Código explicado: botón y método

```python
import requests
from odoo import api, fields, models

class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro'

    name = fields.Char(string='Título', required=True)
    api_response = fields.Text(string='Respuesta API')

    def action_consultar_api(self):
        try:
            response = requests.get('https://jsonplaceholder.typicode.com/todos/1', timeout=10)
            response.raise_for_status()
            self.write({'api_response': response.text})
            return True
        except Exception:
            self.write({'api_response': 'Error al consumir la API'})
            return False
```

> Si `requests` no está disponible en el entorno de Odoo, debes instalarlo en el contenedor antes de probar.

### ✅ Checklist del día

- [ ] Agregar un campo nuevo al modelo `biblioteca.libro`
- [ ] Crear un botón o acción que dispare el método
- [ ] Consumir una API pública con `requests`
- [ ] Guardar el resultado en el campo correspondiente
- [ ] Probar desde la interfaz de Odoo

### 🧪 Reto

Haz que la acción consulte una API pública que devuelva un valor útil para un libro, por ejemplo un texto de referencia o una nota de prueba. Luego muestra ese contenido en el formulario.

### ⚠️ Errores comunes
- No manejar excepciones cuando la API falla
- Usar un tiempo de espera demasiado largo
- Establecer un campo incorrecto para almacenar la respuesta

### 📝 Resumen

Este día conecta Odoo con el mundo exterior. La integración ya no está solo dentro de la base de datos: ahora el sistema consume información real de internet.

---

## Día 4 — Controllers y endpoint propio

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Crear un endpoint propio en Odoo
- Recibir JSON desde Postman o Insomnia
- Crear registros desde peticiones HTTP externas
- Comprender el rol de `http.Controller`

### 📖 Teoría

Un controller permite que Odoo exponga rutas HTTP propias. Esto es muy útil cuando otra aplicación necesita enviar información a Odoo, por ejemplo un webhook o una integración de terceros.

En este caso, la ruta podrá recibir JSON y convertirlo en un registro de `biblioteca.libro`.

### 💻 Código explicado: controller básico

```python
from odoo import http
from odoo.http import request

class BibliotecaApiController(http.Controller):
    @http.route('/api/v1/crear_libro', type='json', auth='user', methods=['POST'])
    def crear_libro(self, **post):
        data = post.get('data', {})
        libro = request.env['biblioteca.libro'].create({
            'name': data.get('name', 'Sin título'),
            'isbn': data.get('isbn', 'SIN-ISBN'),
            'disponible': data.get('disponible', True),
            'genero': data.get('genero', 'ficcion'),
            'autor': data.get('autor', False),
        })
        return {'ok': True, 'id': libro.id}
```

### ✅ Checklist del día

- [ ] Crear un controller nuevo en el módulo
- [ ] Definir una ruta con `@http.route`
- [ ] Probar la ruta desde Postman o Insomnia
- [ ] Enviar JSON y verificar que se crea un libro
- [ ] Revisar la respuesta HTTP del endpoint

### 🧪 Reto

Haz que el endpoint acepte además un autor o editorial y cree el registro relacionado según el JSON entrante.

### ⚠️ Errores comunes
- Olvidar `type='json'`
- No usar `auth='user'` o un usuario válido
- Enviar el body con estructura distinta a la esperada

### 📝 Resumen

Este día convierte a Odoo en un servicio que recibe eventos de afuera. Esa es una de las formas más comunes de integrar sistemas.

---

## Día 5 — Automatización con tareas programadas

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Registrar una tarea programada en Odoo
- Entender qué hace `ir.cron`
- Programar una integración repetitiva sin intervención manual
- Conectar la automatización con la lógica del Día 3

### 📖 Teoría

Muchas integraciones no deben ejecutarse a mano. En producción, las tareas suelen correr en segundo plano con un cron. Odoo permite registrar estos procesos usando `ir.cron`.

El patrón típico es:

1. Crear un método reusable en el modelo
2. Registrar un cron que lo ejecute cada cierto tiempo
3. Verificar que el proceso se dispara automáticamente

### 💻 Código explicado: cron XML

```xml
<odoo>
    <record id="ir_cron_consultar_api_libros" model="ir.cron">
        <field name="name">Consultar API de libros</field>
        <field name="model_id" ref="model_biblioteca_libro"/>
        <field name="state">code</field>
        <field name="code">model.action_consultar_api()</field>
        <field name="interval_number">5</field>
        <field name="interval_type">minutes</field>
        <field name="numbercall">-1</field>
        <field name="active">True</field>
    </record>
</odoo>
```

### ✅ Checklist del día

- [ ] Crear un archivo `data/` si aún no existe
- [ ] Registrar un cron con `ir.cron`
- [ ] Definir intervalo de ejecución
- [ ] Verificar que la tarea aparece en Odoo
- [ ] Asegurar que el método llamado sea estable y seguro

### 🧪 Reto

Haz que el cron actualice un campo de los libros cada 5 minutos usando una acción que ya hayas probado manualmente.

### ⚠️ Errores comunes
- Registrar el cron en el archivo equivocado
- No actualizar el módulo después de agregar el XML
- Llamar un método con lógica pesada sin validaciones

### 📝 Resumen

Este día te enseña a pasar de una integración manual a una automatizada. Ese cambio es clave para trabajar en entornos reales.

---

## Día 6 — Robustez, errores y logs

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Manejar fallos sin romper la ejecución
- Usar `try/except` en integraciones
- Registrar mensajes con `_logger.info` y `_logger.error`
- Aprender a diagnosticar problemas con trazabilidad

### 📖 Teoría

En producción, una API externa puede fallar, devolver JSON mal formado o tardar demasiado. Por eso necesitas escribir código que no “se rompa” y que deje evidencia cuando algo salga mal.

El patrón correcto es:

1. Intentar ejecutar la integración
2. Capturar errores
3. Registrar lo que pasó
4. Retornar un resultado controlado

### 💻 Código explicado: logs y excepciones

```python
import logging

_logger = logging.getLogger(__name__)

class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro'

    def action_consultar_api(self):
        try:
            response = requests.get('https://example.com', timeout=5)
            response.raise_for_status()
            _logger.info('Integración OK para libro %s', self.name)
            return True
        except Exception as error:
            _logger.error('Error en integración: %s', error)
            return False
```

### ✅ Checklist del día

- [ ] Encerrar la lógica de integración en `try/except`
- [ ] Agregar logs de información y error
- [ ] Simular un fallo intencional para probar el flujo
- [ ] Revisar los mensajes en la consola o logs de Odoo

### 🧪 Reto

Provoca una excepción intencional en tu integración y demuestra que Odoo no se cae, sino que registra el fallo.

### ⚠️ Errores comunes
- Capturar todo sin saber qué se está manejando
- No registrar el error real, solo un mensaje genérico
- Olvidar el import de `logging`

### 📝 Resumen

Este día te enseña algo que se valora mucho en trabajo real: cómo escribir integraciones resilientes y fáciles de diagnosticar.

---

## Día 7 — Debugging y lectura de código estándar

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Explorar módulos estándar de Odoo como `sale` o `stock`
- Entender cómo leer código ajeno con criterio
- Usar puntos de interrupción para seguir el flujo
- Relacionar lo que ves en módulos estándar con tu propio módulo `biblioteca`

### 📖 Teoría

Los desarrolladores que trabajan con Odoo no solo crean código; también leen y comprenden código ya escrito. Eso te ayuda a aprender patrones reales y a entender cómo Odoo resuelve procesos estándar.

La práctica recomendada es:

1. Abrir un módulo estándar del repositorio de Odoo
2. Buscar un método relacionado con el proceso que estás construyendo
3. Poner un breakpoint y revisar variables
4. Comparar la lógica con tu módulo propio

### 💻 Código explicado: lectura y seguimiento

```python
# Ejemplo de patrón que puedes buscar en módulos estándar
# se suele ver en métodos como action_confirm, action_done, etc.

for record in self:
    if record.state == 'draft':
        record.write({'state': 'done'})
```

### ✅ Checklist del día

- [ ] Abrir un módulo estándar como `sale` o `stock`
- [ ] Buscar un método similar a una acción de tu proyecto
- [ ] Poner un breakpoint o revisar el flujo manualmente
- [ ] Anotar 3 aprendizajes que puedas aplicar a `biblioteca`

### 🧪 Reto

Compara un método de un módulo estándar con una acción tuya en `biblioteca.libro` y escribe en una nota qué patrón te parece útil y por qué.

### ⚠️ Errores comunes
- Leer código sin contexto de negocio
- Quedarse solo en la firma del método y no en su lógica interna
- Intentar copiar sin entender el problema real

### 📝 Resumen

Este día te entrena para pensar como desarrollador de Odoo, no solo como quien escribe código nuevo.

---

## Día 8 — Repaso y cierre opcional

**Horas:** 2 (Repasar · Consolidar · Cerrar)

### 🎯 Objetivos
- Reunir todo lo aprendido en una sola ruta
- Corregir lo que aún no esté claro
- Dejar el proyecto listo para continuar con más profundidad

### ✅ Checklist final

- [ ] Tienes un script que se conecta a Odoo
- [ ] Puedes crear y actualizar registros desde fuera
- [ ] Tienes un botón o acción que consume una API externa
- [ ] Tienes un endpoint propio que recibe JSON
- [ ] Tienes una tarea programada registrada
- [ ] Tienes logs y manejo de errores implementados
- [ ] Entiendes cómo revisar código estándar de Odoo

### 📝 Cierre

Este día no es para cargar más contenido. Es para consolidar lo que ya construiste y asumir que la base está lista para seguir creciendo.

---

## Reglas del plan

- No avanzar al siguiente día si el entregable anterior sigue incompleto
- Cada día debe terminar con una prueba real, no solo con teoría
- Prioriza que el resultado funcione sobre hacer el contenido perfecto
- Si un día se alarga, no lo “desordenes”; mejor deja un entregable estable y continúa

---

## Resultado final esperado

Al terminar esta semana deberías tener:

- una integración básica con Odoo desde Python externo
- un flujo de creación y actualización de registros desde un script
- una integración que consuma una API externa desde Odoo
- un endpoint propio para recibir datos
- un cron programado que ejecute una tarea automáticamente
- manejo básico de errores y logs
- mayor confianza para leer y depurar código estándar
