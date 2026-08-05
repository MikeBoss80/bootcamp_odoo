import requests
import json


class GoogleBooksService:

    BASE_URL = "https://www.googleapis.com/books/v1/volumes"


    @classmethod
    def buscar_por_isbn(cls, isbn):

        try:

            response = requests.get(
                cls.BASE_URL,
                params={
                    "q": f"isbn:{isbn}"
                },
                timeout=10
            )

            response.raise_for_status()

            return response.json()


        except requests.exceptions.RequestException:
            return {}


    @staticmethod
    def normalizar_fecha(fecha):

        if not fecha:
            return None

        partes = fecha.split("-")

        if len(partes) == 1:
            # Solo viene el año
            return f"{fecha}-01-01"

        if len(partes) == 2:
            # Año y mes
            return f"{fecha}-01"

        return fecha


    @classmethod
    def obtener_libro(cls, isbn):

        data = cls.buscar_por_isbn(isbn)

        items = data.get("items", [])

        if not items:
            return None


        info = items[0].get(
            "volumeInfo",
            {}
        )


        return {

            "name": info.get(
                "title"
            ),

            "descripcion": info.get(
                "description"
            ),

            "autor": info.get(
                "authors",
                [None]
            )[0],

            "genero": cls.normalizar_genero(
                info.get("categories")
            ),

            "editorial": info.get(
                "publisher"
            ),

            "fecha_publicacion": cls.normalizar_fecha(
                info.get(
                    "publishedDate"
                )
            ),

            "api_response": json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ),
        }

    
    @staticmethod
    def normalizar_genero(categorias):

        if not categorias:
            return "ficcion"


        categoria = categorias[0].lower()


        if "fantasy" in categoria:
            return "fantasia"

        if "science fiction" in categoria:
            return "ciencia_ficcion"

        if "romance" in categoria:
            return "romance"

        if "mystery" in categoria:
            return "misterio"

        if "horror" in categoria:
            return "terror"


        return "ficcion"