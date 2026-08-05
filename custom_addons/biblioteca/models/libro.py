from odoo import models, fields, api
import logging

from ..services.google_books import GoogleBooksService


_logger = logging.getLogger(__name__)


class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro'
    _rec_name = 'name'


    name = fields.Char(
        string='Título',
        required=True
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
        string='Género',
        required=True
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
        string='Autor',
        required=True
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



    def action_consultar_api(self):

        _logger.info(
            '========== ENTRO ACTION_CONSULTAR_API =========='
        )


        for libro in self:


            if not libro.isbn:

                return {
                    'warning': {
                        'title': 'ISBN requerido',
                        'message': (
                            'Debe ingresar un ISBN.'
                        )
                    }
                }



            datos = GoogleBooksService.obtener_libro(
                libro.isbn
            )


            _logger.info(
                'RESPUESTA GOOGLE BOOKS: %s',
                datos
            )



            if not datos:

                return {
                    'warning': {
                        'title': 'Sin resultados',
                        'message': (
                            'No se encontró '
                            'información del libro.'
                        )
                    }
                }



            autor = self._obtener_o_crear_autor(
                datos.get('autor')
            )



            vals = {
                'name': datos.get('name'),
                'descripcion': datos.get('descripcion'),
                'fecha_publicacion': datos.get('fecha_publicacion'),
                'api_response': datos.get('api_response'),
            }

            if autor:
                vals['autor'] = autor.id

            libro.write(vals)


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