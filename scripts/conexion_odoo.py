import xmlrpc.client
from dotenv import load_dotenv
import os

load_dotenv()

url=os.getenv('odoo_url')
db=os.getenv('odoo_db')
username=os.getenv('odoo_mail')
password=os.getenv('odoo_pss')


common = xmlrpc.client.ServerProxy(
    f"{url}/xmlrpc/2/common"
)


uid = common.authenticate(
    db,
    username,
    password,
    {}
)



models = xmlrpc.client.ServerProxy(
    f"{url}/xmlrpc/2/object"
)


libros = models.execute_kw(
    db,
    uid,
    password,
    "biblioteca.libro",
    "search_read",
    [
        [
            ('disponible', '=', True)
        ]
    ],
    {
        "fields": [
            "name",
            "isbn",
            "disponible"
        ],
        "limit": 10,
        "order": "name asc"
    }
)

print(f"Conectado a Odoo con el usuario {username} y el ID {uid}")

for libro in libros:
    print(
        libro["name"],
        "|",
        libro["isbn"]
    )
    