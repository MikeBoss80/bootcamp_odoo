import requests
import json
import re
import logging

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

class GoogleBooksError(Exception):
    """Excepción personalizada para errores relacionados con la API de Google Books."""
    pass


class GoogleBooksService:

    BASE_URL = "https://www.googleapis.com/books/v1/volumes"


    @classmethod
    def buscar_por_isbn(cls, isbn, api_key=None):

        isbn_normalizado = cls._normalizar_isbn(isbn)

        params = {"q": f"isbn:{isbn_normalizado}"}

        if api_key:
            params["key"] = api_key

        try:
            _logger.info(
                "Consultando Google Books ISBN: %s",
                isbn_normalizado
            )
            response = requests.get(
                cls.BASE_URL,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            _logger.info(
                "Respuesta exitosa de Google Books. ISBN: %s | Status: %s",
                isbn_normalizado,
                response.status_code
            )

            return response.json()

        except requests.exceptions.Timeout:
            raise GoogleBooksError(
                "Google Books tardó demasiado en responder. Intente de nuevo."
            )

        except requests.exceptions.ConnectionError:
            raise GoogleBooksError(
                "No se pudo conectar con Google Books. Verifique el acceso a Internet."
            )

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status == 429:
                raise GoogleBooksError(
                    "Límite de cuota de Google Books alcanzado (429). "
                    "Espere a que se restablezca o agregue una API key."
                )
            if status == 403:
                raise GoogleBooksError(
                    "Acceso denegado por Google Books (403). "
                    "Verifique permisos o la API key."
                )
            raise GoogleBooksError(
                f"Google Books respondió con un error HTTP {status}."
            )
        except ValueError:
            raise GoogleBooksError(
                "Google Books devolvió una respuesta inválida."
            )    

    @staticmethod
    def _normalizar_isbn(isbn):
        if not isbn:
            return isbn
        return re.sub(r"[^0-9Xx]", "", isbn)
    

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
    def obtener_libro(cls, isbn, api_key=None):

        data = cls.buscar_por_isbn(isbn, api_key=api_key)

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