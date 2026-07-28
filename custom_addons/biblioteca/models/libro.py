from odoo import models, fields

class Libro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libro'

    name = fields.Char(string='Título', required=True)

    autor = fields.Many2one('biblioteca.autor', string='Autor', required=True)

    fecha_publicacion = fields.Date(string='Fecha de publicación')
