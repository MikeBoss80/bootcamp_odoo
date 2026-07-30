# BOOTCAMP ODOO DEVELOPER & INTEGRATIONS
# Semana 2 — Desarrollo

**Objetivo de la semana:** dominar el ORM en profundidad, trabajar con relaciones entre modelos, construir vistas heredadas y aplicar campos computados — las herramientas que distinguen a un desarrollador Odoo de alguien que solo sabe Python.
**Resultado esperado:** proyecto de Inventario funcional con relaciones, vistas heredadas, campos computados, wizard de ajuste y reportes básicos.
**Días incluidos:** Día 7 a Día 12 — 18 horas de contenido

---

## Índice

- [Día 7 — ORM avanzado: create, write, unlink, search, browse, domains y contextos](#día-7--orm-avanzado-create-write-unlink-search-browse-domains-y-contextos)
- [Día 8 — Relaciones entre modelos: Many2one, One2many, Many2many](#día-8--relaciones-entre-modelos-many2one-one2many-many2many)
- [Día 9 — Vistas avanzadas: herencia de vistas con XPath, kanban y calendario](#día-9--vistas-avanzadas-herencia-de-vistas-con-xpath-kanban-y-calendario)
- [Día 10 — Campos computados, @api.depends y @api.onchange](#día-10--campos-computados-apidepends-y-api-onchange)
- [Día 11 — Wizards (TransientModel) y acciones de servidor](#día-11--wizards-transientmodel-y-acciones-de-servidor)
- [Día 12 — Repaso general + Proyecto Inventario completo](#día-12--repaso-general--proyecto-inventario-completo-relaciones-permisos-reportes)

---

## Día 7 — ORM avanzado: create, write, unlink, search, browse, domains y contextos

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Entender el ciclo de vida completo de un registro en Odoo
- Diferenciar `create()`, `write()`, `unlink()`, `search()` y `browse()`
- Usar dominios para filtrar registros con precisión
- Aprovechar el contexto para cambiar el comportamiento sin tocar la vista ni duplicar lógica

### 📖 Teoría

El ORM de Odoo no es solo una capa para crear tablas; es una API de negocio. Cada método expresa una intención distinta:

- `create()` inserta un registro nuevo
- `write()` actualiza uno o varios registros existentes
- `unlink()` elimina registros
- `search()` busca por dominio y devuelve un recordset
- `browse()` construye un recordset a partir de IDs conocidos

En Odoo, un recordset puede contener uno o muchos registros. Esa es una diferencia crítica con Python puro: las operaciones se aplican sobre colecciones de registros y no sobre diccionarios sueltos.

#### Diagrama: flujo ORM

```
Usuario / botón / wizard
      |
      v
Método Python en el modelo
      |
      +--> create()  -> nuevo registro
      +--> write()   -> actualización
      +--> unlink()  -> eliminación
      +--> search()  -> filtrado por dominio
      +--> browse()  -> acceso por IDs
      |
      v
bootcamp_odoo_dev
```

### 💻 Código explicado: modelo Inventario con métodos personalizados

```python
from odoo import api, fields, models


class InventarioProducto(models.Model):
    _name = 'inventario.producto'
    _description = 'Producto de inventario'

    name = fields.Char(string='Nombre', required=True)
    sku = fields.Char(string='SKU')
    cantidad = fields.Integer(string='Cantidad', default=0)
    minimo = fields.Integer(string='Cantidad mínima', default=0)
    activo = fields.Boolean(string='Activo', default=True)

    def action_reponer(self, cantidad=1):
        for producto in self:
            producto.write({'cantidad': producto.cantidad + cantidad})
        return True

    def action_marcar_inactivo(self):
        self.write({'activo': False})
        return True

    def action_eliminar_vacios(self):
        vacios = self.search([('cantidad', '=', 0)])
        vacios.unlink()
        return True

    @api.model
    def buscar_disponibles(self, texto):
        dominio = [('name', 'ilike', texto), ('activo', '=', True)]
        return self.search(dominio)
```

### 💻 Código explicado: dominio y contexto

```python
# Buscar productos con poco stock
productos_bajos = env['inventario.producto'].search([
    ('cantidad', '<=', 10),
    ('activo', '=', True),
])

# Acceder por IDs concretos
productos = env['inventario.producto'].browse([1, 3, 7])

# Contexto: modificar el comportamiento sin cambiar la lógica base
productos_contexto = env['inventario.producto'].with_context(
    default_activo=False,
    from_wizard=True,
)
```

> `with_context()` no cambia los datos por sí solo; solo transporta información adicional para que otros métodos la consulten.

### ✅ Tu progreso en Día 7

| Concepto | Estado |
|----------|--------|
| Diferencia entre `create()` y `write()` | ⬜ |
| Uso de `search()` con dominios | ⬜ |
| Uso de `browse()` con IDs | ⬜ |
| Método personalizado sobre Inventario | ⬜ |
| Contexto aplicado a una acción | ⬜ |

### 🐳 Comandos Docker

```powershell
# Actualizar módulo para probar métodos nuevos
docker compose run --rm odoo -d bootcamp_odoo_dev -u inventario --stop-after-init

# Abrir shell de Odoo
docker compose exec odoo odoo shell -d bootcamp_odoo_dev

# Probar búsqueda manual
>>> env['inventario.producto'].search([('cantidad', '<=', 10)])
```

### 🧪 Reto
Implementa tres acciones en el modelo de Inventario: reponer stock, desactivar producto y eliminar productos sin cantidad. Luego prueba cada una desde el shell y documenta qué hace cada método.

### ⚠️ Errores comunes
- Usar `search()` esperando un único registro cuando devuelve un recordset
- Llamar `write()` sobre un diccionario en lugar de sobre un recordset
- Borrar con `unlink()` sin validar primero si el usuario tiene permiso

### 📌 Buenas prácticas
- Preferir métodos de negocio con nombres claros como `action_reponer` o `action_marcar_inactivo`
- Validar en el método, no solo en la vista
- Usar dominios pequeños y legibles para no esconder lógica importante

### 📝 Resumen
Hoy se aprende a manipular el ORM como herramienta de negocio. `create()`, `write()`, `search()` y `unlink()` no son solo operaciones técnicas: son el lenguaje con el que Odoo expresa procesos reales.

---

## Día 8 — Relaciones entre modelos: Many2one, One2many, Many2many

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Entender cómo Odoo modela relaciones relacionales sobre bootcamp_odoo_dev
- Declarar campos `Many2one`, `One2many` y `Many2many`
- Diseñar un modelo de Productos con Categorías relacionadas
- Leer correctamente qué lado guarda la clave foránea

### 📖 Teoría

Las relaciones son la base de un modelo de datos serio. En Odoo:

- `Many2one` guarda una referencia a un único registro de otro modelo
- `One2many` es el reverso lógico de `Many2one`
- `Many2many` crea una relación múltiple entre ambos modelos

En bootcamp_odoo_dev, `Many2one` suele materializarse como una columna con ID. `One2many` no crea columna propia: depende del campo inverso. `Many2many` usa una tabla intermedia.

#### Diagrama: relaciones

```
inventario.categoria 1 ----- * inventario.producto
       ^                           |
       |                           |
       |                       Many2one
       |                           v
   One2many               inventario.producto

inventario.producto * ----- * inventario.etiqueta
              Many2many
```

### 💻 Código explicado: productos y categorías

```python
from odoo import fields, models


class InventarioCategoria(models.Model):
    _name = 'inventario.categoria'
    _description = 'Categoría de inventario'

    name = fields.Char(string='Nombre', required=True)
    producto_ids = fields.One2many(
        comodel_name='inventario.producto',
        inverse_name='categoria_id',
        string='Productos',
    )


class InventarioProducto(models.Model):
    _name = 'inventario.producto'
    _description = 'Producto de inventario'

    name = fields.Char(string='Nombre', required=True)
    categoria_id = fields.Many2one(
        comodel_name='inventario.categoria',
        string='Categoría',
        ondelete='restrict',
    )
    etiqueta_ids = fields.Many2many(
        comodel_name='inventario.etiqueta',
        string='Etiquetas',
    )
```

### 💻 Código explicado: relación Many2many

```python
class InventarioEtiqueta(models.Model):
    _name = 'inventario.etiqueta'
    _description = 'Etiqueta de producto'

    name = fields.Char(string='Nombre', required=True)
```

```python
producto = env['inventario.producto'].create({
    'name': 'Teclado mecánico',
    'categoria_id': categoria.id,
    'etiqueta_ids': [(4, etiqueta_oficina.id), (4, etiqueta_gaming.id)],
})
```

> En `Many2many`, Odoo acepta comandos especiales como `(4, id)` para enlazar registros existentes.

### ✅ Tu progreso en Día 8

| Concepto | Estado |
|----------|--------|
| `Many2one` definido correctamente | ⬜ |
| `One2many` como reverso lógico | ⬜ |
| `Many2many` funcionando | ⬜ |
| Categorías relacionadas con productos | ⬜ |
| Registros creados desde shell | ⬜ |

### 🐳 Comandos Docker

```powershell
docker compose run --rm odoo -d bootcamp_odoo_dev -u inventario --stop-after-init
docker compose run --rm odoo shell -d bootcamp_odoo_dev
```

### 🧪 Reto
Crea el modelo `inventario.categoria` y relaciónalo con `inventario.producto`. Agrega al menos una relación `Many2many` adicional para etiquetas o proveedores preferidos y comprueba el resultado desde el shell.

### ⚠️ Errores comunes
- Poner `One2many` sin el `inverse_name` correcto
- Pensar que `One2many` almacena datos por sí mismo
- Borrar una categoría sin definir `ondelete` y provocar efectos inesperados

### 📌 Buenas prácticas
- Modelar primero las relaciones de negocio, no la interfaz
- Usar nombres técnicos consistentes: `categoria_id`, `producto_ids`
- Elegir `ondelete` de forma consciente según la regla del negocio

### 📝 Resumen
La relación correcta entre modelos es lo que convierte datos sueltos en un sistema usable. En Odoo, las relaciones deben diseñarse pensando en la semántica de negocio y en cómo se traducen a bootcamp_odoo_dev.

---

## Día 9 — Vistas avanzadas: herencia de vistas con XPath, kanban y calendario

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Heredar una vista estándar sin modificar el módulo original
- Usar XPath para insertar, reemplazar o mover elementos
- Construir una vista kanban para visualizar inventario rápidamente
- Entender cuándo conviene usar calendario o kanban

### 📖 Teoría

La herencia de vistas es una de las técnicas más importantes en Odoo. En lugar de reescribir una vista base, se crea una vista heredada que modifica puntos concretos del XML original con `xpath`.

Eso permite extender módulos estándar como `sale`, `stock` o `product` sin tocar el código fuente del módulo original.

#### Diagrama: herencia de vistas

```
Vista base del módulo estándar
      |
      v
Vista heredada de tu módulo
      |
      +--> xpath inserta un campo
      +--> xpath reemplaza un bloque
      +--> xpath oculta un elemento
```

### 💻 Código explicado: heredar una vista estándar

```xml
<odoo>
    <record id="view_product_template_form_inherit_inventory" model="ir.ui.view">
        <field name="name">product.template.form.inherit.inventory</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_only_form_view"/>
        <field name="arch" type="xml">
            <xpath expr="//sheet//group" position="inside">
                <field name="x_stock_minimo"/>
            </xpath>
        </field>
    </record>
</odoo>
```

> El `inherit_id` apunta a la vista original. El `xpath` define el punto exacto donde insertar el cambio.

### 💻 Código explicado: vista kanban

```xml
<record id="view_inventario_producto_kanban" model="ir.ui.view">
    <field name="name">inventario.producto.kanban</field>
    <field name="model">inventario.producto</field>
    <field name="arch" type="xml">
        <kanban>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_global_click">
                        <strong><field name="name"/></strong>
                        <div>Cantidad: <field name="cantidad"/></div>
                        <div>Categoría: <field name="categoria_id"/></div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

### 💻 Código explicado: vista calendario

```xml
<record id="view_inventario_movimiento_calendar" model="ir.ui.view">
    <field name="name">inventario.movimiento.calendar</field>
    <field name="model">inventario.movimiento</field>
    <field name="arch" type="xml">
        <calendar string="Movimientos" date_start="fecha_programada">
            <field name="name"/>
            <field name="producto_id"/>
        </calendar>
    </field>
</record>
```

### ✅ Tu progreso en Día 9

| Concepto | Estado |
|----------|--------|
| Vista heredada con `inherit_id` | ⬜ |
| XPath funcionando sin romper la vista base | ⬜ |
| Vista kanban creada | ⬜ |
| Vista calendario creada | ⬜ |
| Extensión de módulo estándar sin editarlo | ⬜ |

### 🐳 Comandos Docker

```powershell
docker compose run --rm odoo -d bootcamp_odoo_dev -u inventario --stop-after-init
docker compose restart odoo
```

### 🧪 Reto
Extiende una vista estándar de Odoo con XPath para agregar un campo propio del módulo Inventario. Luego crea una vista kanban para revisar rápidamente el estado de los productos.

### ⚠️ Errores comunes
- Apuntar a un `xpath` que no existe en la vista base
- Olvidar cargar la vista heredada en `data`
- Reescribir toda la vista original cuando solo hace falta un ajuste pequeño

### 📌 Buenas prácticas
- Heredar solo lo necesario
- Elegir selectores XPath estables
- Mantener una vista por objetivo: formulario, lista, kanban o calendario

### 📝 Resumen
Las vistas heredadas permiten extender módulos estándar con seguridad y limpieza. XPath es el mecanismo clave para alterar la interfaz sin romper la base original.

---

## Día 10 — Campos computados, @api.depends y @api.onchange

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Crear campos computados que dependan de otros campos
- Diferenciar `@api.depends` de `@api.onchange`
- Entender cuándo un campo debe almacenarse con `store=True`
- Implementar un stock total calculado automáticamente

### 📖 Teoría

Los campos computados evitan duplicar información y centralizan reglas. Odoo recalcula un campo cuando cambian sus dependencias declaradas con `@api.depends`.

- `@api.depends` recalcula en servidor cuando cambian los campos fuente
- `@api.onchange` reacciona en la interfaz antes de guardar el registro

#### Diagrama: reactividad

```
Usuario cambia cantidad
      |
      v
@api.onchange -> reacción visual inmediata
      |
      v
Guardar registro
      |
      v
@api.depends -> recalculo persistente
```

### 💻 Código explicado: stock total calculado

```python
from odoo import api, fields, models


class InventarioProducto(models.Model):
    _name = 'inventario.producto'
    _description = 'Producto de inventario'

    name = fields.Char(string='Nombre', required=True)
    stock_disponible = fields.Integer(string='Stock disponible', default=0)
    stock_reservado = fields.Integer(string='Stock reservado', default=0)
    stock_total = fields.Integer(
        string='Stock total',
        compute='_compute_stock_total',
        store=True,
    )

    @api.depends('stock_disponible', 'stock_reservado')
    def _compute_stock_total(self):
        for producto in self:
            producto.stock_total = producto.stock_disponible + producto.stock_reservado

    @api.onchange('stock_disponible', 'stock_reservado')
    def _onchange_stock(self):
        if self.stock_disponible < 0:
            self.stock_disponible = 0
```

### 💻 Código explicado: campo auxiliar para UX

```python
estado_stock = fields.Selection(
    selection=[
        ('alto', 'Alto'),
        ('medio', 'Medio'),
        ('bajo', 'Bajo'),
    ],
    compute='_compute_estado_stock',
    store=True,
)

@api.depends('stock_total')
def _compute_estado_stock(self):
    for producto in self:
        if producto.stock_total >= 100:
            producto.estado_stock = 'alto'
        elif producto.stock_total >= 20:
            producto.estado_stock = 'medio'
        else:
            producto.estado_stock = 'bajo'
```

### ✅ Tu progreso en Día 10

| Concepto | Estado |
|----------|--------|
| Campo computado con `@api.depends` | ⬜ |
| Uso correcto de `store=True` | ⬜ |
| `@api.onchange` para experiencia de usuario | ⬜ |
| Stock total calculado automáticamente | ⬜ |
| Reglas de negocio centralizadas | ⬜ |

### 🐳 Comandos Docker

```powershell
docker compose run --rm odoo -d bootcamp_odoo_dev -u inventario --stop-after-init
docker compose run --rm odoo shell -d bootcamp_odoo_dev
```

### 🧪 Reto
Implementa el campo `stock_total` y un campo de estado visual que cambie según el nivel de existencias. Prueba el comportamiento tanto en shell como desde el formulario.

### ⚠️ Errores comunes
- Olvidar declarar todas las dependencias en `@api.depends`
- No usar `store=True` cuando el campo debe filtrarse o agruparse
- Confundir `onchange` con lógica persistente de negocio

### 📌 Buenas prácticas
- Guardar (`store=True`) solo cuando exista una razón clara
- Mantener el cálculo en un método pequeño y legible
- Usar `onchange` para UX, no para validaciones críticas

### 📝 Resumen
Los campos computados permiten derivar información sin duplicarla. La combinación correcta de `@api.depends` y `@api.onchange` crea modelos más consistentes y una interfaz más reactiva.

---

## Día 11 — Wizards (TransientModel) y acciones de servidor

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Entender qué es un wizard y por qué usa `TransientModel`
- Crear una pantalla temporal para ajuste de inventario
- Lanzar un wizard desde un botón o una acción de ventana
- Conectar una acción de servidor para automatizar una operación frecuente

### 📖 Teoría

Un wizard es una interfaz de uso temporal. Sus datos no están pensados para persistir como un modelo de negocio; por eso se usa `models.TransientModel`.

Los wizards son útiles para:
- confirmar acciones delicadas
- recolectar datos antes de ejecutar una operación
- asistir procesos que requieren varios pasos

#### Diagrama: flujo de wizard

```
Botón / acción
      |
      v
TransientModel (wizard)
      |
      v
Ejecuta lógica sobre modelos reales
      |
      v
Resultado en Inventario
```

### 💻 Código explicado: wizard de ajuste de inventario

```python
from odoo import fields, models


class InventarioAjusteWizard(models.TransientModel):
    _name = 'inventario.ajuste.wizard'
    _description = 'Wizard de ajuste de inventario'

    producto_id = fields.Many2one('inventario.producto', string='Producto', required=True)
    cantidad_nueva = fields.Integer(string='Cantidad nueva', required=True)
    motivo = fields.Char(string='Motivo')

    def action_confirmar(self):
        self.ensure_one()
        self.producto_id.write({'cantidad': self.cantidad_nueva})
        return {'type': 'ir.actions.act_window_close'}
```

### 💻 Código explicado: abrir wizard desde una acción

```python
def action_abrir_ajuste(self):
    self.ensure_one()
    return {
        'type': 'ir.actions.act_window',
        'name': 'Ajustar inventario',
        'res_model': 'inventario.ajuste.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'default_producto_id': self.id,
        },
    }
```

### 💻 Código explicado: acción de servidor

```xml
<record id="action_server_reponer_stock" model="ir.actions.server">
    <field name="name">Reponer stock mínimo</field>
    <field name="model_id" ref="model_inventario_producto"/>
    <field name="state">code</field>
    <field name="code">
        records.filtered(lambda p: p.cantidad < p.minimo).action_reponer(10)
    </field>
</record>
```

> Una acción de servidor ejecuta código en el servidor sin necesidad de abrir un formulario intermedio.

### ✅ Tu progreso en Día 11

| Concepto | Estado |
|----------|--------|
| Wizard con `TransientModel` | ⬜ |
| Botón para abrir el wizard | ⬜ |
| Acción de confirmación funcionando | ⬜ |
| Acción de servidor configurada | ⬜ |
| Ajuste de inventario probado | ⬜ |

### 🐳 Comandos Docker

```powershell
docker compose run --rm odoo -d bootcamp_odoo_dev -u inventario --stop-after-init
docker compose restart odoo
```

### 🧪 Reto
Construye un wizard para ajustar inventario y ejecútalo desde la vista formulario del producto. Luego agrega una acción de servidor que reponga automáticamente productos por debajo del mínimo.

### ⚠️ Errores comunes
- Usar `models.Model` en lugar de `TransientModel` para un formulario temporal
- Olvidar `target='new'` y abrir el wizard en navegación normal
- Ejecutar lógica crítica solo desde el wizard sin reutilizar el método en el modelo

### 📌 Buenas prácticas
- Reutilizar el método de negocio desde el wizard
- Mantener los wizards pequeños y centrados en una tarea
- Usar contexto para prellenar valores por defecto

### 📝 Resumen
Los wizards resuelven flujos guiados y temporales. Las acciones de servidor automatizan tareas repetitivas y permiten dejar reglas de operación dentro de Odoo.

---

## Día 12 — Repaso general + Proyecto Inventario completo (relaciones, permisos, reportes)

**Horas:** 3 (Comprender · Construir · Consolidar)

### 🎯 Objetivos
- Integrar todo lo visto en un proyecto único
- Verificar relaciones, vistas, seguridad y wizards
- Generar reportes básicos para cierre de semana
- Entender qué significa que el módulo esté realmente listo para uso

### 📖 Teoría

Hoy no se introduce una técnica nueva aislada. El objetivo es confirmar que el proyecto funciona como sistema: modelos relacionados, vistas heredadas, seguridad por grupos, campos computados, wizard y reportes.

#### Arquitectura final del proyecto Inventario

```
inventario/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── producto.py
│   ├── categoria.py
│   ├── etiqueta.py
│   └── ajuste_wizard.py
├── views/
│   ├── producto_views.xml
│   ├── categoria_views.xml
│   ├── inventario_menu.xml
│   └── product_inherit_views.xml
├── security/
│   ├── inventario_security.xml
│   └── ir.model.access.csv
└── reports/
    └── inventario_report.xml
```

### ✅ Checklist de integración

| Requisito | Estado |
|-----------|--------|
| Existe el modelo `inventario.producto` | ⬜ |
| Existe al menos una relación `Many2one` | ⬜ |
| Existe una relación `One2many` coherente | ⬜ |
| Existe una relación `Many2many` funcional | ⬜ |
| Hay una vista heredada con XPath | ⬜ |
| Existe un campo computado con `store=True` | ⬜ |
| El wizard de ajuste funciona | ⬜ |
| Los permisos por grupo están definidos | ⬜ |
| Hay al menos un reporte básico | ⬜ |
| El módulo instala desde cero sin errores | ⬜ |

### 📌 Pendientes reales para continuar

- Completar el reporte QWeb del inventario para imprimir fichas o listados.
- Validar que el wizard reutiliza métodos del modelo y no duplica lógica.
- Probar el módulo con un usuario de bajo privilegio para confirmar permisos.
- Documentar decisiones de diseño: por qué ciertas relaciones son `Many2one` y no `Many2many`, o cuándo se guarda un campo computado.

### 💻 Código explicado: estructura de reporte básico

```xml
<record id="action_report_inventario_producto" model="ir.actions.report">
    <field name="name">Ficha de Producto</field>
    <field name="model">inventario.producto</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">inventario.report_producto_ficha</field>
    <field name="report_file">inventario.report_producto_ficha</field>
</record>
```

```xml
<template id="report_producto_ficha">
    <t t-call="web.external_layout">
        <div class="page">
            <h2 t-esc="doc.name"/>
            <p t-esc="doc.categoria_id.name"/>
            <p t-esc="doc.stock_total"/>
        </div>
    </t>
</template>
```

### 🐳 Comandos Docker — prueba desde cero

```powershell
# Detener todo
docker compose down

# Arrancar servicios limpios
docker compose up -d

# Instalar el módulo Inventario en una base nueva
docker compose run --rm odoo -d bootcamp_inventario -i inventario --stop-after-init

# Verificar logs
docker compose logs --tail=50 odoo
```

### 🧪 Reto de cierre
Escribe el README del proyecto Inventario documentando:
1. Cómo instalar el módulo desde cero
2. Qué modelos existen y cómo se relacionan
3. Qué permisos y grupos de seguridad existen
4. Qué hace el wizard de ajuste
5. Qué reportes quedaron disponibles

### ⚠️ Errores comunes al integrar
- Dejar datos de prueba dispersos y no limpiar la base antes de validar
- Corregir un error de permisos abriendo acceso total en vez de revisar la regla o el grupo
- Dar por terminado el proyecto sin probar el flujo completo: alta, edición, ajuste y reporte

### 📌 Buenas prácticas de cierre
- Probar instalación limpia antes de considerar el trabajo terminado
- Revisar el log completo del servidor
- Versionar este punto con Git y dejar un mensaje claro del avance

### 📝 Resumen de la Semana 2

En seis días, el proyecto pasa de ser una colección de modelos a un módulo de Inventario más robusto, con:
- Operaciones ORM reales y controladas
- Relaciones entre modelos bien definidas
- Vistas extendidas con XPath
- Campos computados y comportamiento reactivo
- Wizards para flujos guiados
- Base suficiente para reportes y permisos de uso real

El patrón que queda instalado es el mismo de la semana anterior, pero más profundo: **modelar el negocio, reutilizar lógica, extender sin romper, y verificar todo con una instalación limpia**.