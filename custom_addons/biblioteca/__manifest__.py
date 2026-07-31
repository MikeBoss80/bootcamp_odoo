{
    "name": "Biblioteca",
    "version": "17.0.1.0.0",
    "category": "Services",
    "summary": "Gestión básica de biblioteca",
    "description": """
        Módulo para gestionar libros y autores.
    """,
    "author": "Miguel Bolivar",
    "website": "",
    "license": "LGPL-3",

    "depends": [
        "base",
    ],

   "data": [
        "security/biblioteca_security.xml",
        "security/ir.model.access.csv",

        "views/libro_views.xml",
        "views/autor_views.xml",
        "views/editorial_views.xml",
        "views/etiqueta_views.xml",

        "views/menus.xml",
    ],

    "demo": [
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}