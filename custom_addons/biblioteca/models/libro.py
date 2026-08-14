from odoo import models, fields, api
import logging, os
from psycopg2 import IntegrityError


from ..services.google_books import GoogleBooksError, GoogleBooksService


_logger = logging.getLogger(__name__)


class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro'
    _rec_name = 'name'

    _sql_constraints = [
        (
            'external_id_unique',
            'UNIQUE(external_id)',
            'El ID externo ya existe en otro libro.'
        )
    ]

    external_id = fields.Char(
        string='ID externo',
        index=True,
        copy=False,
        readonly=True,
        help='ID externo del libro en el sistema de origen'
    )

    name = fields.Char(
        string='Título'
    )

    descripcion = fields.Text(
        string='Descripción'
    )

    isbn = fields.Char(
        string='ISBN',
        required=True,
        index=True
    )

    disponible = fields.Boolean(
        string='Disponible',
        default=True
    )


    estado = fields.Selection(
        selection=[
            ('disponible', 'Disponible'),
            ('prestado', 'Prestado'),
        ],
        string='Estado',
        compute='_compute_estado',
    )


    genero = fields.Selection(
        selection=[
            ('ficcion', 'Ficción'),
            ('drama', 'Drama'),
            ('fantasia', 'Fantasía'),
            ('ciencia_ficcion', 'Ciencia Ficción'),
            ('romance', 'Romance'),
            ('misterio', 'Misterio'),
            ('terror', 'Terror'),
        ],
        string='Género'
    )


    etiqueta_ids = fields.Many2many(
        'biblioteca.etiqueta',
        'biblioteca_etiqueta_libro_rel',
        'libro_id',
        'etiqueta_id',
        string='Etiquetas'
    )


    autor = fields.Many2one(
        'biblioteca.autor',
        string='Autor'
    )


    editorial_id = fields.Many2one(
        'biblioteca.editorial',
        string='Editorial'
    )


    antiguedad = fields.Integer(
        string='Años desde publicación',
        compute='_compute_antiguedad'
    )


    fecha_publicacion = fields.Date(
        string='Fecha de publicación'
    )


    fecha_ingreso = fields.Date(
        string='Fecha de ingreso',
        default=fields.Date.today
    )


    api_response = fields.Text(
        string='Respuesta API'
    )


    estado_sincronizacion = fields.Selection(
        selection=[
            ('pendiente', 'Pendiente'),
            ('sincronizando', 'Sincronizando'),
            ('sincronizado', 'Sincronizado'),
            ('error', 'Error'),
        ],
        string='Estado de sincronización',
        default='pendiente',
        readonly=True,
        copy=False,
    )

    ultima_sincronizacion = fields.Datetime(
        string='Última sincronización',
        readonly=True,
        copy=False,
    )

    sync_error = fields.Text(
        string='Error de sincronización',
        readonly=True,
        copy=False,
    )


    @api.depends('fecha_publicacion')
    def _compute_antiguedad(self):

        for libro in self:

            if libro.fecha_publicacion:

                try:
                    pub_date = fields.Date.from_string(libro.fecha_publicacion)
                    today = fields.Date.from_string(fields.Date.today())
                    libro.antiguedad = today.year - pub_date.year
                except Exception:
                    libro.antiguedad = 0

            else:

                libro.antiguedad = 0



    @api.depends('disponible')
    def _compute_estado(self):

        for libro in self:

            libro.estado = (
                'disponible'
                if libro.disponible
                else 'prestado'
            )



    def action_marcar_disponible(self):

        self.write({
            'disponible': True
        })

        return True



    def action_marcar_no_disponible(self):

        self.write({
            'disponible': False
        })

        return True



    def action_eliminar_sin_isbn(self):

        libros = self.search([
            ('isbn', '=', False)
        ])

        libros.unlink()

        return True



    @api.model
    def buscar_disponibles(self, texto):

        dominio = [
            ('name', 'ilike', texto),
            ('disponible', '=', True),
        ]

        return self.search(dominio)



    @api.onchange('fecha_publicacion')
    def _onchange_fecha_publicacion(self):

        hoy = fields.Date.today()

        if (
            self.fecha_publicacion
            and self.fecha_publicacion > hoy
        ):

            return {
                'warning': {
                    'title': 'Fecha inválida',
                    'message': (
                        'La fecha de publicación '
                        'no puede ser futura.'
                    ),
                }
            }

    def _preparar_vals_google_books(self, datos):

        self.ensure_one()

        if datos:
            autor = self._obtener_o_crear_autor(
                datos.get("autor")
            )

            editorial = self._obtener_o_crear_editorial(
                datos.get("editorial")
            )

            vals = {
                "external_id": datos.get("external_id"),
                "name": datos.get("name"),

                "descripcion": datos.get("descripcion"),

                "fecha_publicacion": datos.get("fecha_publicacion"),

                "genero": datos.get("genero"),

                "api_response": datos.get("api_response"),
            }

            if autor:
                vals["autor"] = autor.id

            if editorial:
                vals["editorial_id"] = editorial.id

        return vals

    def _consultar_google_books(self):
        api_key = os.environ.get("GOOGLE_BOOKS_API_KEY")

        incompletos = []
        errores = []

        for libro in self:

            if not libro.isbn:
                _logger.warning(
                    "Libro sin ISBN, se omite: %s",
                    libro.name
                )
                continue

            libro.write({
                'estado_sincronizacion': 'sincronizando',
                'sync_error': False,
            })

            try:
                datos = GoogleBooksService.obtener_libro(
                    libro.isbn,
                    api_key=api_key
                )

            except GoogleBooksError as e:
                _logger.error(
                    "Falló consulta Google Books. ISBN: %s | Error: %s",
                    libro.isbn,
                    e
                )
                libro.write({
                    'estado_sincronizacion': 'error',
                    'sync_error': str(e),
                })
                errores.append(str(e))
                continue

            if not datos:
                _logger.warning(
                    "Sin resultados para %s",
                    libro.isbn
                )
                libro.write({
                    'estado_sincronizacion': 'error',
                    'sync_error': "Google Books no devolvió resultados.",
                })
                continue

            external_id = datos.get("external_id")

            if not external_id:
                _logger.warning(
                    "Google Books no devolvió external_id para ISBN %s",
                    libro.isbn
                )
                mensaje = (
                    "Google Books no devolvió un ID externo para ISBN %s"
                    % libro.isbn
                )
                libro.write({
                    'estado_sincronizacion': 'error',
                    'sync_error': mensaje,
                })
                errores.append(mensaje)
                continue


            try:
                conflicto = libro._verificar_conflicto_external_id(
                    external_id
                )
            except ValueError as e:
                libro.write({
                    'estado_sincronizacion': 'error',
                    'sync_error': str(e),
                })
                errores.append(str(e))
                continue

            vals = libro._preparar_vals_google_books(
                datos
            )
            vals.update({
                'estado_sincronizacion': 'sincronizado',
                'ultima_sincronizacion': fields.Datetime.now(),
                'sync_error': False,
            })

            libro.write(vals)


            if not datos.get("name"):
                incompletos.append(libro.isbn)

        return errores, incompletos

    def action_consultar_api(self):
        _logger.info("Consulta manual desde formulario")

        errores, incompletos = self._consultar_google_books()

        if errores:

            return {
                "warning": {
                    "title": "Error al consultar Google Books",
                    "message": "; ".join(errores),
                }
            }

        if incompletos:

            return {
                "warning": {
                    "title": "Autocompletado parcial",
                    "message": (
                        "No se pudo completar el título de: %s"
                    ) % ", ".join(incompletos)
                }
            }

        return True

    def _obtener_o_crear_autor(self, nombre):

        if not nombre:

            return False



        autor = self.env[
            'biblioteca.autor'
        ].search(
            [
                ('name', '=', nombre)
            ],
            limit=1
        )


        if not autor:

            try:
                with self.env.cr.savepoint():
                    autor = self.env[
                        'biblioteca.autor'
                    ].create({
                        'name': nombre
                    })
            except IntegrityError:
                autor = self.env[
                    'biblioteca.autor'
                ].search(
                    [('name', '=', nombre)],
                    limit=1
                )
                if not autor:
                    raise


        return autor

    def _obtener_o_crear_editorial(self, nombre):

        if not nombre:
            return False

        editorial = self.env['biblioteca.editorial'].search(
            [('name', '=', nombre)], limit=1
        )

        if not editorial:
            try:
                with self.env.cr.savepoint():
                    editorial = self.env['biblioteca.editorial'].create({
                        'name': nombre,
                        'pais': '',
                    })
            except IntegrityError:
                editorial = self.env['biblioteca.editorial'].search(
                    [('name', '=', nombre)], limit=1
                )
                if not editorial:
                    raise

        return editorial

    @api.model
    def cron_actualizar_libros_api(self):
        _logger.info("=== Inicio cron Google Books ===")

        libros = self.search([
            ('isbn', '!=', False),
            ('name', '=', False),
            ('estado_sincronizacion', 'in', ['pendiente', 'error']),
        ])

        _logger.info(
            "Se encontraron %s libros pendientes.",
            len(libros)
        )

        errores, incompletos = libros._consultar_google_books()

        if errores:
            _logger.warning(
                "Errores encontrados: %s",
                errores
            )

        if incompletos:
            _logger.warning(
                "Libros incompletos: %s",
                incompletos
            )

        _logger.info("=== Fin cron Google Books ===")

        return True

    

    def _buscar_external_id(self, external_id):

        return self.search([
            ('external_id', '=', external_id)
        ], limit=1)

    def _verificar_conflicto_external_id(self, external_id):

        self.ensure_one()

        libro = self._buscar_external_id(external_id)

        if libro and libro.id != self.id:

            raise ValueError(
                "El ID externo '%s' ya existe en otro libro."
                % (
                    external_id,
                    libro.display_name
                )
            )
        
        return libro
