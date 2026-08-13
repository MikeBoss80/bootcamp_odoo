from odoo import models, fields

class Autor(models.Model):
    _name = 'biblioteca.autor'
    _description = 'Autor'

    name = fields.Char(string='Nombre', required=True)

    libros_ids = fields.One2many('biblioteca.libro', 'autor', string='Libros')

    _sql_constraints = [
        (
            'autor_name_unique',
            'UNIQUE(name)',
            'El autor ya existe.'
        )
    ]