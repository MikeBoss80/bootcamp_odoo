# BOOTCAMP ODOO DEVELOPER & INTEGRATIONS
# Semana 4 — Integraciones bidireccionales y sincronización guiada

**Objetivo de la semana:** consolidar lo aprendido en integración real dando el salto de “consultar APIs” a “sincronizar datos”, trabajando con Odoo como origen y como destino, y practicando en formato pair programming para reforzar criterio técnico, lectura de código y resolución de errores.
**Resultado esperado:** flujo funcional sobre `biblioteca` que permita consultar una API pública, mapear datos a `biblioteca.libro`, usar `external_id`, importar JSON, exponer un webhook básico y registrar intentos de sincronización con control de errores.
**Días incluidos:** Día 1 a Día 6 — 18 horas de contenido

---

## Índice

- [Cómo trabajar en pair programming](#cómo-trabajar-en-pair-programming)
- [Día 1 — Revisión del flujo actual y primer mapa de integración](#día-1--revisión-del-flujo-actual-y-primer-mapa-de-integración)
- [Día 2 — API pública de libros y normalización de datos](#día-2--api-pública-de-libros-y-normalización-de-datos)
- [Día 3 — external_id, idempotencia y sincronización manual](#día-3--external_id-idempotencia-y-sincronización-manual)
- [Día 4 — Importador JSON con wizard](#día-4--importador-json-con-wizard)
- [Día 5 — Webhook de actualización y validación](#día-5--webhook-de-actualización-y-validación)
- [Día 6 — Cola de sincronización, logs y repaso final](#día-6--cola-de-sincronización-logs-y-repaso-final)

---

## Cómo trabajar en pair programming

En esta semana el foco no es solo “hacer que funcione”, sino aprender a pensar como integrador. Por eso cada sesión se trabaja en pareja con dos roles claros:

### Rol Driver
- Escribe el código.
- Explica en voz alta lo que está haciendo.
- No decide solo: propone, pero valida con el Navigator.

### Rol Navigator
- Revisa la lógica y detecta errores antes de ejecutar.
- Cuestiona nombres de campos, dominios, validaciones y casos límite.
- Obliga a justificar por qué se elige `create`, `write`, `search` o `unlink`.

### Regla de trabajo
- Cambiar roles cada 15 a 20 minutos.
- Antes de tocar código, acordar el objetivo puntual del bloque.
- Después de cada cambio, correr una validación corta.
- Si algo falla, primero entender el fallo, después corregirlo.

> La idea de la semana no es avanzar rápido, sino avanzar con criterio y con conversación técnica.

---

## Día 1 — Revisión del flujo actual y primer mapa de integración

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Revisar lo que ya existe en el módulo `biblioteca`
- Identificar dónde empieza y dónde termina una integración dentro del proyecto actual
- Entender qué partes ya resuelven Google Books y qué partes todavía faltan para una sincronización profesional
- Aprender a dividir un problema grande en pasos pequeños durante pair programming

### 📖 Teoría

Antes de integrar nada nuevo, hay que entender el punto de partida. En el proyecto actual ya existe una base muy valiosa:

- un modelo `biblioteca.libro`
- un servicio Python que consulta Google Books
- un botón en formulario para disparar la consulta
- un cron preparado para automatizar la actualización

Eso significa que el siguiente aprendizaje no debe ser repetir la consulta, sino convertir la consulta en un flujo de sincronización real. Para eso hay que mirar el problema con tres preguntas:

1. ¿De dónde viene el dato?
2. ¿Cómo identifico el mismo libro en dos sistemas distintos?
3. ¿Qué hago si el dato ya existe, cambió o falló la comunicación?

#### Diagrama: mapa inicial del proyecto

```
Usuario / script / API externa
           |
           v
    Google Books / JSON
           |
           v
   Servicio Python en Odoo
           |
           v
    biblioteca.libro
```

### 💻 Código explicado: puntos de control del flujo

```python
def action_consultar_api(self):
    errores, incompletos = self._consultar_google_books()

    if errores:
        return {
            'warning': {
                'title': 'Error al consultar Google Books',
                'message': '; '.join(errores),
            }
        }

    if incompletos:
        return {
            'warning': {
                'title': 'Autocompletado parcial',
                'message': 'No se pudo completar el título de: %s' % ', '.join(incompletos),
            }
        }

    return True
```

Este patrón enseña algo importante: una integración no solo devuelve datos, también devuelve estados. El usuario tiene que saber si la operación fue completa, parcial o fallida.

### ✅ Checklist del día

- [ ] Explicar en voz alta cómo llega un dato desde Google Books hasta Odoo
- [ ] Identificar el método que hace la consulta
- [ ] Identificar el punto donde se escribe en `biblioteca.libro`
- [ ] Revisar si existe o no un identificador externo en el modelo
- [ ] Acordar en pareja qué problema se resolverá primero

### 🧪 Reto

Haz un mapa en papel o en un archivo de notas con tres columnas:

- entrada
- transformación
- salida

Usa ese mapa para describir el flujo actual del módulo y marca dónde faltaría un `external_id`.

### ⚠️ Errores comunes
- Querer añadir sincronización sin entender primero el flujo actual
- Mezclar lectura de API con reglas de negocio sin separarlas
- No documentar qué hace cada parte antes de empezar a programar

### 📌 Buenas prácticas
- Dividir una integración en piezas pequeñas
- Nombrar claramente los puntos de entrada y salida
- Validar el flujo antes de pensar en escalarlo

### 📝 Resumen

El objetivo de este día es ver el proyecto como una arquitectura de integración, no como una colección de archivos. Antes de escribir más código, hay que entender el recorrido de cada dato.

---

## Día 2 — API pública de libros y normalización de datos

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Consumir una API pública de libros desde Odoo
- Extraer campos útiles como título, autor, editorial, fecha e ISBN
- Normalizar la respuesta para adaptarla al modelo `biblioteca.libro`
- Manejar errores, timeouts y respuestas vacías

### 📖 Teoría

Cuando una API responde, casi nunca devuelve exactamente la forma que tu modelo necesita. Por eso una parte crítica del trabajo es la normalización: transformar el JSON externo en datos coherentes para Odoo.

En este punto no basta con “leer” la respuesta. Hay que decidir:

- qué campo externo corresponde a qué campo interno
- qué hacer si un dato viene vacío
- cómo tratar fechas incompletas
- cómo evitar romper el registro si la API devuelve algo raro

#### Diagrama: transformación de datos

```
API pública
   |
   v
JSON bruto
   |
   v
Normalización
   |
   v
vals de Odoo
   |
   v
biblioteca.libro
```

### 💻 Código explicado: servicio de normalización

```python
class GoogleBooksService:
    @classmethod
    def obtener_libro(cls, isbn, api_key=None):
        data = cls.buscar_por_isbn(isbn, api_key=api_key)
        items = data.get('items', [])

        if not items:
            return None

        info = items[0].get('volumeInfo', {})

        return {
            'name': info.get('title'),
            'descripcion': info.get('description'),
            'isbn': isbn,
            'autor': info.get('authors', [None])[0],
            'editorial': info.get('publisher'),
            'fecha_publicacion': cls.normalizar_fecha(info.get('publishedDate')),
        }
```

La clave aquí es que la API no se consume directamente en la vista ni en el formulario. Primero pasa por un servicio que ordena la información. Eso hace el código más mantenible y más fácil de probar en pareja.

### 💻 Código explicado: escritura en el modelo

```python
vals = {
    'name': datos.get('name'),
    'descripcion': datos.get('descripcion'),
}

if datos.get('fecha_publicacion'):
    vals['fecha_publicacion'] = datos.get('fecha_publicacion')

libro.write(vals)
```

Este enfoque evita actualizar campos vacíos sin necesidad. Si la API no trae información suficiente, el registro no debe quedar peor de lo que estaba.

### ✅ Checklist del día

- [ ] Ejecutar una búsqueda real por ISBN
- [ ] Verificar que la API devuelve un JSON válido
- [ ] Mapear título, autor, editorial y fecha
- [ ] Comprobar qué pasa cuando no hay resultados
- [ ] Probar la normalización con un ISBN real y uno inválido

### 🧪 Reto

Haz que la API alimente solo tres campos del libro: título, descripción y fecha de publicación. Luego agrega el resto uno por uno y explica en pareja por qué cada campo se añadió.

### ⚠️ Errores comunes
- Suponer que todos los JSON tienen la misma estructura
- Escribir `write()` directamente con campos que pueden venir vacíos
- No diferenciar entre error de red, error HTTP y resultado vacío

### 📌 Buenas prácticas
- Separar consulta, transformación y persistencia
- Validar cada campo antes de escribirlo
- Registrar errores en lugar de ocultarlos

### 📝 Resumen

Hoy se aprende a convertir una API pública en datos útiles dentro de Odoo. La normalización es el puente entre el mundo externo y el modelo interno.

---

## Día 3 — `external_id`, idempotencia y sincronización manual

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Agregar un identificador externo al modelo `biblioteca.libro`
- Entender el concepto de idempotencia en integraciones
- Diferenciar cuándo crear y cuándo actualizar
- Diseñar una acción manual de sincronización sobre un libro

### 📖 Teoría

En una integración real necesitas saber si un registro ya existe en el sistema remoto. Por eso se usa un identificador externo, por ejemplo `external_id`.

Con ese campo, Odoo puede responder a una pregunta muy concreta:

- si no hay `external_id`, crear
- si ya hay `external_id`, actualizar

Eso evita duplicados y hace que la integración sea idempotente: ejecutar la misma operación varias veces no genera efectos no deseados.

#### Diagrama: decisión create / update

```
¿Tiene external_id?
      |
  ┌───┴───┐
  |       |
 NO      SÍ
  |       |
CREATE   UPDATE
```

### 💻 Código explicado: campo externo

```python
from odoo import fields, models


class Libro(models.Model):
    _name = 'biblioteca.libro'

    external_id = fields.Char(string='ID externo', index=True)
```

Ese campo no solo guarda un dato más. Define la forma en que Odoo se relaciona con otro sistema.

### 💻 Código explicado: sincronización manual

```python
def action_sincronizar_libro(self):
    for libro in self:
        if libro.external_id:
            libro.write({
                'name': libro.name,
            })
        else:
            libro.external_id = 'BOOK-%s' % libro.id
    return True
```

Este ejemplo es intencionalmente simple: sirve para practicar la lógica de decisión antes de conectar una API de verdad. En pair programming, lo importante es discutir la estrategia, no solo copiar el patrón.

### ✅ Checklist del día

- [ ] Añadir `external_id` al modelo
- [ ] Decidir si el campo será obligatorio o opcional
- [ ] Probar el flujo create/update con dos libros
- [ ] Confirmar que no se duplican registros
- [ ] Documentar la regla de sincronización en el archivo de la semana

### 🧪 Reto

Implementa un botón llamado `Sincronizar libro` que revise si el libro tiene `external_id`. Si no lo tiene, simula una creación externa; si lo tiene, simula una actualización.

### ⚠️ Errores comunes
- Crear registros nuevos cada vez que se sincroniza
- Usar un ID de base de datos como si fuera un ID externo
- No distinguir entre identificación interna y externa

### 📌 Buenas prácticas
- Tener un campo explícito para el identificador remoto
- Diseñar la integración pensando en reintentos
- Evitar duplicidad desde el inicio

### 📝 Resumen

Este día introduce la base técnica de una sincronización seria. El concepto clave es idempotencia: una integración madura no debe multiplicar registros por accidente.

---

## Día 4 — Importador JSON con wizard

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Diseñar un wizard para importar libros desde JSON
- Validar estructura, tipos y campos obligatorios
- Aplicar lógica de create/update usando `external_id`
- Practicar lectura de archivos y procesamiento por lotes

### 📖 Teoría

Importar desde JSON es una práctica excelente para fortalecer validaciones. Aquí ya no importa un solo registro: importa un lote.

El flujo típico es:

1. Subir un archivo JSON
2. Validar que el contenido sea una lista
3. Revisar que cada objeto tenga los campos mínimos
4. Buscar `external_id`
5. Crear o actualizar
6. Registrar resultado por línea

#### Diagrama: flujo del importador

```
Archivo JSON
    |
    v
Wizard
    |
    v
Validar JSON
    |
    v
Validar campos
    |
    v
Buscar external_id
    |
    v
Crear / actualizar
    |
    v
Log de importación
```

### 💻 Código explicado: estructura de ejemplo

```json
[
  {
    "external_id": "BOOK001",
    "title": "Libro 1",
    "author": "Autor 1"
  },
  {
    "external_id": "BOOK002",
    "title": "Libro 2",
    "author": "Autor 2"
  }
]
```

### 💻 Código explicado: lógica del wizard

```python
import json
from odoo import models, fields


class BibliotecaImportWizard(models.TransientModel):
    _name = 'biblioteca.import.wizard'

    archivo_json = fields.Binary(string='Archivo JSON', required=True)

    def action_importar(self):
        data = json.loads(self.archivo_json)
        for item in data:
            libro = self.env['biblioteca.libro'].search([
                ('external_id', '=', item.get('external_id'))
            ], limit=1)

            vals = {
                'name': item.get('title'),
            }

            if libro:
                libro.write(vals)
            else:
                vals['external_id'] = item.get('external_id')
                self.env['biblioteca.libro'].create(vals)
```

Este ejemplo no es el más completo posible, pero sí el más útil para practicar. En pair programming, una versión pequeña y correcta enseña más que una versión enorme y confusa.

### ✅ Checklist del día

- [ ] Crear el wizard
- [ ] Subir un JSON válido
- [ ] Detectar un JSON mal formado
- [ ] Crear registros nuevos desde el archivo
- [ ] Actualizar registros existentes cuando coincida `external_id`

### 🧪 Reto

Agrega al wizard un reporte simple con tres contadores:

- creados
- actualizados
- con error

### ⚠️ Errores comunes
- No validar que el archivo realmente contenga JSON
- Asumir que siempre llega una lista
- Escribir registros sin revisar el `external_id`

### 📌 Buenas prácticas
- Procesar lote por lote con trazabilidad
- Guardar resultados parciales
- Mostrar mensajes claros al usuario final

### 📝 Resumen

Hoy se practica importación estructurada. El wizard te obliga a pensar en validación, trazabilidad y experiencia de usuario, no solo en escritura de datos.

---

## Día 5 — Webhook de actualización y validación

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Exponer un endpoint HTTP para recibir eventos externos
- Validar autenticación, estructura y contenido
- Actualizar un libro por `external_id`
- Responder con códigos HTTP correctos

### 📖 Teoría

Un webhook es la forma inversa de una API tradicional: el sistema externo empuja un evento hacia Odoo. Esto sirve para notificaciones, cambios de estado o actualizaciones automáticas.

Cuando trabajas con webhooks debes definir con cuidado:

- cómo autenticas la petición
- qué campo identifica el registro
- qué hacer si el libro no existe
- cómo responder si la estructura es inválida

#### Diagrama: webhook

```
Sistema externo
     |
     | POST JSON
     v
Controller en Odoo
     |
     v
Validación
     |
     v
Buscar libro por external_id
     |
     v
Actualizar
     |
     v
Responder 200 / 400 / 401 / 404 / 500
```

### 💻 Código explicado: controller básico

```python
from odoo import http
from odoo.http import request


class BibliotecaWebhookController(http.Controller):

    @http.route('/api/biblioteca/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def webhook_libro(self, **payload):
        external_id = payload.get('external_id')

        if not external_id:
            return {'ok': False, 'error': 'external_id es obligatorio'}

        libro = request.env['biblioteca.libro'].sudo().search([
            ('external_id', '=', external_id)
        ], limit=1)

        if not libro:
            return {'ok': False, 'error': 'Libro no encontrado'}

        libro.write({
            'name': payload.get('title', libro.name),
        })

        return {'ok': True, 'id': libro.id}
```

### ✅ Checklist del día

- [ ] Crear el controller
- [ ] Probar el endpoint con un cliente HTTP
- [ ] Verificar el caso de `external_id` ausente
- [ ] Verificar el caso de libro inexistente
- [ ] Confirmar actualización correcta cuando el libro sí existe

### 🧪 Reto

Haz que el webhook acepte también un cambio de editorial o fecha de publicación y que ignore campos desconocidos sin romper la petición.

### ⚠️ Errores comunes
- No validar la entrada antes de escribir
- Usar permisos insuficientes o excesivos
- Responder siempre 200 aunque haya un error real

### 📌 Buenas prácticas
- Validar explícitamente el payload
- Registrar quién invoca el webhook y cuándo
- Proteger la ruta aunque sea pública

### 📝 Resumen

El webhook te enseña a recibir datos desde afuera de manera controlada. Es una pieza básica de cualquier integración bidireccional.

---

## Día 6 — Cola de sincronización, logs y repaso final

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Diseñar un modelo de log para sincronizaciones
- Guardar request, response, estado y error
- Entender cómo reintentar operaciones fallidas
- Cerrar la semana con una visión completa del flujo de integración

### 📖 Teoría

Una integración profesional no solo hace cosas; también deja evidencia de lo que pasó. Si una operación falla, necesitas saber qué se intentó, cuándo, con qué datos y qué respondió el sistema externo.

Un modelo de log ayuda a responder preguntas como:

- ¿Se intentó sincronizar?
- ¿Falló por red o por datos?
- ¿Se reintentó?
- ¿Cuántas veces falló?

#### Diagrama: cola de sincronización

```
Libro
  |
  v
Crear intento de sync
  |
  v
Sync log: pending
  |
  v
Sync log: processing
  |
  +--> success
  |
  +--> error
         |
         v
      reintento
```

### 💻 Código explicado: modelo de log

```python
from odoo import fields, models


class BibliotecaSyncLog(models.Model):
    _name = 'biblioteca.sync.log'

    operation = fields.Char(string='Operación')
    model = fields.Char(string='Modelo')
    record_id = fields.Integer(string='ID interno')
    external_id = fields.Char(string='ID externo')
    status = fields.Selection([
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('success', 'Éxito'),
        ('error', 'Error'),
    ], string='Estado')
    request = fields.Text(string='Request')
    response = fields.Text(string='Response')
    error = fields.Text(string='Error')
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now)
```

### 💻 Código explicado: reintento por cron

```python
def cron_reintentar_sync(self):
    logs = self.search([('status', '=', 'error')], limit=20)
    for log in logs:
        log.write({'status': 'processing'})
        # aquí se intentaría ejecutar de nuevo la operación real
```

Este día sirve para pensar como alguien que mantiene integraciones en producción. El objetivo no es solo terminar la tarea: es poder recuperarse si falla.

### ✅ Checklist del día

- [ ] Crear el modelo de log
- [ ] Registrar un intento exitoso y uno fallido
- [ ] Identificar qué información guardar en cada caso
- [ ] Proponer una estrategia de reintento
- [ ] Hacer un repaso oral de toda la semana

### 🧪 Reto

Construye una mini demo en la que un libro se sincronice, falle por una causa simulada y luego quede guardado en el log para ser reintentado por un cron.

### ⚠️ Errores comunes
- No guardar suficiente información para depurar
- Mezclar el log técnico con la lógica principal
- Ignorar los estados intermedios de una sincronización

### 📌 Buenas prácticas
- Registrar cada intento con contexto
- Diseñar reintentos automáticos
- Separar operación, validación y trazabilidad

### 📝 Resumen

La semana cierra con una integración más madura: ya no solo consumes una API, sino que entiendes cómo sincronizar, validar, registrar y reintentar en un flujo real de trabajo.

---

## Cierre de semana

Si completas esta semana, ya no solo estarás aprendiendo Odoo desde dentro. Estarás entrenando la lógica de un integrador: leer, transformar, decidir, sincronizar y registrar.

La práctica en pareja te obliga a explicar mejor, detectar errores antes y justificar cada decisión técnica. Ese hábito vale tanto como el código que escribas.
