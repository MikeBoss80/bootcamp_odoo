import json

from odoo import http
from odoo.http import request, Response

class BibliotecaAPIController(http.Controller):

    @http.route('/api/v1/crear_libro', type='json', auth='api_key', methods=['POST'])
    def crear_libro(self):
        data = request.get_json_data()

        if not data.get('name') or not data.get('isbn'):
            return {'ok': False, 'error': 'El nombre y el ISBN son obligatorios'}

        autor = False
        if data.get('autor_id'):
            autor = request.env['biblioteca.autor'].browse(data['autor_id'])
            if not autor.exists():
                return {'ok': False, 'error': 'No existe el autor indicado'}
        elif data.get('autor'):
            autor = request.env['biblioteca.autor'].search(
                [('name', '=', data['autor'])], limit=1
            )
            if not autor:
                autor = request.env['biblioteca.autor'].create({
                    'name': data['autor']
                })

        editorial = False
        if data.get('editorial_id'):
            editorial = request.env['biblioteca.editorial'].browse(data['editorial_id'])
            if not editorial.exists():
                return {'ok': False, 'error': 'No existe la editorial indicada'}
        elif data.get('editorial'):
            editorial = request.env['biblioteca.editorial'].search(
                [('name', '=', data['editorial'])], limit=1
            )
            if not editorial:
                editorial = request.env['biblioteca.editorial'].create({
                    'name': data['editorial'], 'pais': ''
                })

        libro = request.env['biblioteca.libro'].create({
            'name': data.get('name'),
            'isbn': data.get('isbn'),
            'descripcion': data.get('descripcion'),
            'genero': data.get('genero', 'ficcion'),
            'autor': autor.id if autor else False,
            'editorial_id': editorial.id if editorial else False,
        })

        return {'ok': True, 'id': libro.id, 'name': libro.name, 'isbn': libro.isbn}



    @http.route('/api/v1/lista_libros', type='http', auth='api_key', methods=['GET'])
    def lista_libros(self):
        libros = request.env['biblioteca.libro'].search([])

        resultado = [{
            'id': libro.id,
            'name': libro.name,
            'isbn': libro.isbn,
            'descripcion': libro.descripcion,
            'genero': libro.genero,
            'autor': libro.autor.name if libro.autor else None,
            'editorial': libro.editorial_id.name if libro.editorial_id else None,
        } for libro in libros] 

        return Response(
            json.dumps({'ok': True, 'libros': resultado, 'total': len(resultado)}),
            content_type='application/json; charset=utf-8',
        )