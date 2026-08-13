from odoo import models, fields


class Editorial(models.Model):

    _name = 'biblioteca.editorial'
    _description = 'Editorial'


    name = fields.Char(
        string='Nombre',
        required=True
    )

    pais = fields.Char(
        string='País',
    )


    libros_ids = fields.One2many(
        'biblioteca.libro',
        'editorial_id',
        string='Libros'
    )
    _sql_constraints = [
        (
            'editorial_name_unique',
            'UNIQUE(name)',
            'La editorial ya existe.'
        )
    ]