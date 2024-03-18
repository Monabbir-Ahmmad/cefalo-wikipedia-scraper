def response(movie) -> dict:
    return {
        **movie,
        "_id": str(movie["_id"]),
    }

def list_response(movies) -> list:
    return [response(movie) for movie in movies]