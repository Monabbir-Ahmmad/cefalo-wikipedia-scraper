def response(movie) -> dict:
    return {
        **movie,
        "_id": str(movie["_id"]),
        "title": movie["title"],
        "link": movie["link"],
        "year": movie["year"],
        "awards": movie["awards"],
        "nominations": movie["nominations"]
    }

def list_response(movies) -> list:
    return [response(movie) for movie in movies]