from odoo import models, fields, api
import logging, os


from ..services.google_books import GoogleBooksError, GoogleBooksService


_logger = logging.getLogger(__name__)


class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro'
    _rec_name = 'name'


    name = fields.Char(
        string='Título'
    )

    descripcion = fields.Text(
        string='Descripción'
    )

    isbn = fields.Char(
        string='ISBN',
        required=True
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

            try:
                datos = GoogleBooksService.obtener_libro(
                    libro.isbn,
                    #api_key=api_key
                )

            except GoogleBooksError as e:

                _logger.error(
                    "Falló consulta Google Books. ISBN: %s | Error: %s",
                    libro.isbn,
                    e
                )

                
                errores.append(str(e))
                continue


            if not datos:

                _logger.warning(
                    "Sin resultados para %s",
                    libro.isbn
                )

                continue


            autor = self._obtener_o_crear_autor(
                datos.get("autor")
            )

            editorial = self._obtener_o_crear_editorial(
                datos.get("editorial")
            )


            vals = {

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


            libro.write(vals)


            if not libro.name:
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

            autor = self.env[
                'biblioteca.autor'
            ].create({

                'name': nombre

            })



        return autor

    def _obtener_o_crear_editorial(self, nombre):

        if not nombre:
            return False

        editorial = self.env['biblioteca.editorial'].search(
            [('name', '=', nombre)], limit=1
        )

        if not editorial:
            editorial = self.env['biblioteca.editorial'].create({
                'name': nombre,
                'pais': '',
            })

        return editorial

    
    def cron_actualizar_libros_api(self):
        _logger.info("=== Inicio cron Google Books ===")

        libros = self.search([
            ('isbn', '!=', False),
            ('name', '=', False),
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