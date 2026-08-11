from odoo import http
from odoo.http import request

class BibliotecaAPIController(http.Controller):

    @http.route('/api/v1/crear_libro', type='json', auth='public', methods=['POST'])
    def crear_libro(self):
        data = request.get_json_data()

        if not data.get('name') or not data.get('isbn'):
            return {'ok': False, 'error': 'El nombre y el ISBN son obligatorios'}

        autor = False
        if data.get('autor_id'):
            autor = request.env['biblioteca.autor'].sudo().browse(data['autor_id'])
            if not autor.exists():
                return {'ok': False, 'error': 'No existe el autor indicado'}
        elif data.get('autor'):
            autor = request.env['biblioteca.autor'].sudo().search(
                [('name', '=', data['autor'])], limit=1
            )
            if not autor:
                autor = request.env['biblioteca.autor'].sudo().create({
                    'name': data['autor']
                })

        editorial = False
        if data.get('editorial_id'):
            editorial = request.env['biblioteca.editorial'].sudo().browse(data['editorial_id'])
            if not editorial.exists():
                return {'ok': False, 'error': 'No existe la editorial indicada'}
        elif data.get('editorial'):
            editorial = request.env['biblioteca.editorial'].sudo().search(
                [('name', '=', data['editorial'])], limit=1
            )
            if not editorial:
                editorial = request.env['biblioteca.editorial'].sudo().create({
                    'name': data['editorial'], 'pais': ''
                })

        libro = request.env['biblioteca.libro'].sudo().create({
            'name': data.get('name'),
            'isbn': data.get('isbn'),
            'descripcion': data.get('descripcion'),
            'genero': data.get('genero', 'ficcion'),
            'autor': autor.id if autor else False,
            'editorial_id': editorial.id if editorial else False,
        })

        return {'ok': True, 'id': libro.id, 'name': libro.name, 'isbn': libro.isbn}