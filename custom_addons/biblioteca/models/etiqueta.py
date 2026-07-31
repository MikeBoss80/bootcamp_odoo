from odoo import fields, models


class Etiqueta(models.Model):
    _name = 'biblioteca.etiqueta'
    _description = 'Etiqueta de libros'

    name = fields.Char(string='Nombre', required=True)
    
    libros_ids = fields.Many2many(
        'biblioteca.libro',
        'biblioteca_etiqueta_libro_rel',
        'etiqueta_id',
        'libro_id',
        string='Libros'
    )

    