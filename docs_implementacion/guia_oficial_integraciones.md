# BOOTCAMP ODOO DEVELOPER & INTEGRATIONS
# Guía oficial de construcción a partir de ahora

**Objetivo general:** convertir lo que ya construiste en una base práctica para integraciones reales con Odoo, usando como base tu módulo actual `biblioteca` y un enfoque corto, ordenado y útil para tu empalme laboral.

**Duración sugerida:** 7 días de desarrollo. Opcionalmente, un día 8 de repaso y cierre si quieres bajar carga y dejar todo bien amarrado.
**Ritmo recomendado:** 2 a 3 horas por día.
**Enfoque:** aprender haciendo, validando cada bloque con un resultado visible.

---

## Punto de partida real

El proyecto ya no parte de cero. Hoy tu módulo `biblioteca` tiene esta base:

- `biblioteca.libro` con campos, acciones, `@api.depends` y `@api.onchange`
- `biblioteca.autor` con relación `One2many` hacia libros
- `biblioteca.editorial` con relación `One2many` hacia libros
- `biblioteca.etiqueta` con relación `Many2many` hacia libros

Eso significa que la guía ya puede apoyarse sobre un modelo real y no sobre ejemplos inventados.

## Qué vamos a construir

Este plan no busca repetir teoría general de Odoo. La meta es dominar el flujo real de integraciones aplicadas a `biblioteca`:

- conectar Odoo con scripts externos por XML-RPC o JSON-RPC
- consumir APIs externas desde `biblioteca.libro` para enriquecer libros o validar datos
- exponer endpoints propios con controllers para crear o consultar libros, autores o editoriales
- automatizar procesos con `ir.cron` sobre tareas de catálogo o sincronización
- manejar errores, logs y trazabilidad
- leer código estándar y depurar con criterio

La idea es que llegues al trabajo con una base práctica para entender cómo piensa Odoo cuando se integra con otros sistemas.

---

## Cómo se usará esta guía

Cada día tendrá tres partes:

- **Enfoque:** qué concepto debes entender
- **Práctica:** qué vas a construir o probar
- **Entregable:** qué debe quedar funcionando al final del día

Si un día te toma menos tiempo, no lo llenes por rellenar. Mejor deja el resultado estable y avanza con claridad.

---

## Mapa de trabajo

| Día | Tema | Resultado esperado |
|-----|------|--------------------|
| 1 | Integración externa con XML-RPC / JSON-RPC | Script de Python que lee datos de Odoo y valida la conexión |
| 2 | CRUD desde fuera de Odoo | Script que crea o actualiza libros reales desde una API externa o un cliente local |
| 3 | Consumo de APIs externas desde Odoo | Botón en `biblioteca.libro` que consulta una API pública y guarda respuesta útil |
| 4 | Controllers y API propia | Endpoint propio que recibe JSON y crea libros, autores o editoriales |
| 5 | Automatización con `ir.cron` | Tarea programada que ejecuta una sincronización de catálogo sola |
| 6 | Robustez, errores y logs | Manejo de fallos con `try/except` y `_logger` sobre el flujo de Biblioteca |
| 7 | Lectura de código y debugging | Revisión de módulos estándar y uso de breakpoints |
| 8 | Repaso opcional y cierre | Consolidación final y repaso de dudas sobre el proyecto |

---

## Día 1 — Entorno de integración y conexión externa

**Enfoque:** entender cómo un script externo se autentica y habla con Odoo sin entrar por la interfaz web.

**Práctica:** escribir un script local en Python usando `xmlrpc.client` para conectarse a tu Odoo local y leer registros de `biblioteca.libro` o `res.partner`.

**Entregable:** un script `.py` que imprima 3 libros o 3 contactos desde tu base de datos.

**Criterio de cierre:** si el script autentica y devuelve datos reales, el día está completo.

---

## Día 2 — Manipulación de datos desde fuera

**Enfoque:** ejecutar operaciones CRUD desde un script externo para entender cómo viajan los datos hacia el ORM de Odoo.

**Práctica:** extender el script del Día 1 para crear un libro nuevo, actualizar su información y, si aplica, eliminarlo al final.

**Entregable:** un script que inserte y modifique un registro real de `biblioteca.libro` en la base de datos de Odoo.

**Criterio de cierre:** si puedes crear y actualizar un registro sin usar la interfaz web, ya entendiste el flujo base de integración.

---

## Día 3 — Consumo de APIs externas desde Odoo

**Enfoque:** invertir el sentido de la integración: ahora es Odoo quien consulta una API externa.

**Práctica:** crear un botón en `biblioteca.libro` para consultar una API pública con `requests` y guardar la respuesta en un campo nuevo, por ejemplo un dato auxiliar de referencia o metadatos del libro.

**Entregable:** un botón funcional en la vista de libros que consume una API y persiste el resultado.

**Criterio de cierre:** si el botón devuelve información útil y la almacena, la integración está resuelta.

---

## Día 4 — API propia con controllers

**Enfoque:** exponer endpoints para que otros sistemas puedan enviar datos a Odoo.

**Práctica:** crear un controller con una ruta tipo `/api/v1/crear_libro` que reciba JSON y genere un libro, o una ruta para consultar el catálogo de `biblioteca.libro`.

**Entregable:** una petición desde Postman o Insomnia que reciba respuesta correcta y cree un registro en Odoo.

**Criterio de cierre:** si el endpoint procesa datos y responde bien, ya tienes una API propia mínima.

---

## Día 5 — Automatización con tareas programadas

**Enfoque:** hacer que una integración se ejecute sola sin intervención humana.

**Práctica:** crear un archivo XML en `data/` para registrar un cron job que ejecute la lógica del Día 3 cada pocos minutos y actualice datos de libros automáticamente.

**Entregable:** una tarea programada que corra automáticamente en Odoo.

**Criterio de cierre:** si no dependes del botón manual para ejecutar la integración, el proceso ya está automatizado.

---

## Día 6 — Robustez, errores y logs

**Enfoque:** aprender a proteger la integración cuando la API falla, responde mal o tarda demasiado.

**Práctica:** envolver la lógica del Día 4 con `try/except` y registrar eventos con `_logger.info` y `_logger.error`, dejando trazabilidad clara cuando falle una integración de Biblioteca.

**Entregable:** una integración que maneje errores sin romper el flujo y deje evidencia clara en logs.

**Criterio de cierre:** si puedes provocar un error y Odoo lo captura sin colapsar, la base de robustez está lista.

---

## Día 7 — Código estándar, debugging y lectura técnica

**Enfoque:** aprender a explorar módulos oficiales de Odoo y a seguir la ejecución con herramientas de depuración.

**Práctica:** revisar un módulo estándar como `sale` o `stock`, ubicar métodos relevantes y probar un breakpoint o seguimiento de variable, comparando su patrón con lo que tienes en `biblioteca.libro`.

**Entregable:** una nota de estudio con hallazgos concretos sobre cómo Odoo resuelve una operación real.

**Criterio de cierre:** si ya puedes leer código estándar sin perderte, estás mucho más cerca del trabajo real.

---

## Día 8 — Repaso y cierre opcional

**Enfoque:** bajar velocidad, revisar huecos y dejar todo documentado.

**Práctica:** repasar scripts, vistas, controllers, cron y logs; corregir lo que haya quedado flojo.

**Entregable:** lista final de aprendizajes y pendientes, si los hubiera.

**Criterio de cierre:** este día no es para meter más carga. Es para consolidar y cerrar con cabeza fría.

---

## Reglas del plan

- No avanzar al siguiente día si el entregable anterior no corre.
- No buscar profundidad innecesaria en temas que todavía no te desbloquean la práctica.
- No mezclar demasiadas integraciones en un solo día.
- Priorizar siempre que algo funcione de principio a fin.

---

## Resultado final esperado

Al terminar este bloque deberías tener:

- un script externo que lee y escribe en `biblioteca`
- un modelo de Odoo que consulta APIs externas
- un endpoint propio listo para recibir datos de Biblioteca
- una tarea programada ejecutándose sola
- manejo básico de errores y logs
- más confianza para leer código estándar y depurar

## En qué se enfoca exactamente el proyecto

La ruta de trabajo queda centrada en dos frentes:

- **Catálogo y datos maestros:** libros, autores, editoriales y etiquetas
- **Integraciones y automatización:** consumir datos externos, exponer APIs propias y dejar tareas automáticas listas para operación real

Eso hace que el aprendizaje tenga una relación directa con tu módulo actual y con lo que probablemente verás en el trabajo.

---

## Nota de enfoque

La intención de esta guía es que el aprendizaje se sienta como una transición natural hacia el trabajo real. No se trata de cubrir todo Odoo, sino de dominar un conjunto pequeño pero útil de patrones que vas a ver una y otra vez en integraciones.
