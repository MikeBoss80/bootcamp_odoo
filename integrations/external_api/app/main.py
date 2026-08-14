from fastapi import FastAPI, HTTPException

from app.data import publishers


app = FastAPI(
    title="External Library API",
    description="API externa simulada para sincronización de catálogos",
    version="1.0.0",
)


@app.get("/publishers")
def get_publishers():
    
    result = []

    for publisher in publishers:
        result.append({
            "id": publisher["id"],
            "name": publisher["name"],
            "books_count": len(publisher["books"]),
            "sample_books": [
                book["title"]
                for book in publisher["books"]
                #if book["isbn"].startswith("978")  # Ejemplo de filtro para libros con ISBN que comienzan con "978
            ],
        })
    return result




@app.get("/publishers/{publisher_id}/books")
def get_publisher_books(publisher_id: str):

    for publisher in publishers:
        if publisher["id"] == publisher_id:
            return {
                "publisher": {
                    "id": publisher["id"],
                    "name": publisher["name"],
                },
                "books": publisher["books"],
            }

    raise HTTPException(
        status_code=404,
        detail="Publisher not found"
    )