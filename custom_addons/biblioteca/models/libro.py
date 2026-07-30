from odoo import models, fields

class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro'
    _rec_name = 'name'



    name = fields.Char(string='Título', required=True)
    isbn = fields.Char(string='ISBN', required=True)
    disponible = fields.Boolean(string='Disponible', default=True)
    genero =fields.Selection([
        ('ficcion', 'Ficción'),
        ('drama', 'Drama'),
        ('fantasia', 'Fantasía'),
        ('ciencia_ficcion', 'Ciencia Ficción'),
        ('romance', 'Romance'),
        ('misterio', 'Misterio'),
        ('terror', 'Terror'),
    ], string='Género', required=True)


    autor = fields.Many2one('biblioteca.autor', string='Autor', required=True)

    editorial_id = fields.Many2one(
        'biblioteca.editorial',
        string='Editorial'
    )

    fecha_publicacion = fields.Date(string='Fecha de publicación')
    fecha_ingreso = fields.Date(string='Fecha de ingreso', default=fields.Date.today)

    def action_marcar_no_disponible(self):
        self.write({
            "disponible": False
        })
        return True

    
