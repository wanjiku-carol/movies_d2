import json
from flask import Flask, request
from flask_restful import Api, Resource
from helpers import search_movie, paginate

app = Flask(__name__)
api = Api(app)


with open('mock_data.json', "r") as file:
    movies = json.load(file)


class Movies(Resource):
    """
    Get a list of movies. Search using a search term. Allows pagination
    """

    def get(self):
        try:
            if request.args:
                if "q" or "page" or "limit" not in request.args.keys():
                    res = {
                        "status": "error",
                        "message": "You must provide q or page or limit in the query params"
                    }
                q = request.args.get('q')
                page = request.args.get('page')
                limit = request.args.get('limit')
                response = movies
                if q:
                    response = search_movie(movies, q)
                    if len(response) > 10:
                        res = paginate(response)
                        if q and page:
                            res = paginate(data=response, page=int(page))
                        if q and limit:
                            res = paginate(data=response, limit=int(limit))
                        if q and page and limit:
                            res = paginate(data=response, page=int(page),
                                           limit=int(limit))
                    else:
                        res = {
                            "status": "success",
                            "data": response,
                            "total": len(response)
                        }
                    return (res)
                if page:
                    page = int(page)
                    res = paginate(response, page=page)
                if limit:
                    limit = int(limit)
                    res = paginate(response, limit=limit)
                    if len(response) < limit:
                        res = {
                            "status": "error",
                            "message": "Limit provided is too large"
                        }
                if page and limit:
                    res = paginate(response, limit=limit, page=page)
            else:
                response = movies
                res = paginate(response)
            return (res)
        except ValueError:
            res = {
                "status": "error",
                "message": "Invalid request"
            }
            return res


class Movie(Resource):
    """
    Get a movie by id
    """

    def get(self, id):
        for movie in movies:
            for key, value in movie.items():
                if id == movie["id"]:
                    response = {
                        "status": "success",
                        "data": movie
                    }
                else:
                    response = {
                        "status": "error",
                        "message": "Movie not found"
                    }
        return response


api.add_resource(Movies, '/movies', endpoint="movies")
api.add_resource(Movie, '/movies/<int:id>', endpoint="movie")


if __name__ == "__main__":
    app.run(debug=True)
