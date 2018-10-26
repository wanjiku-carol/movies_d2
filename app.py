import json
from flask import Flask, request, Response
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
                for key in request.args.keys():
                    if key not in ["q", "page", "limit"]:
                        res = {
                            "status": "error",
                            "message": "You must provide q or page or limit in the query params"
                        }
                        return Response(json.dumps(res), status=400,
                                        mimetype="application/json")
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
                        return Response(res, status=400,
                                        mimetype="application/json")
                if page and limit:
                    res = paginate(response, limit=limit, page=page)
            else:
                response = movies
                res = paginate(response)
            return Response(json.dumps(res), status=200, mimetype="application/json")
        except ValueError:
            res = {
                "status": "error",
                "message": "Invalid request"
            }
            return Response(json.dumps(res), status=400,
                            mimetype="application/json")


class Movie(Resource):
    """
    Get a movie by id
    """

    def get(self, id):
        movie_ids = []
        for movie in movies:
            for key, value in movie.items():
                if id == movie["id"]:
                    movie_ids.append(movie)

        if len(movie_ids) < 1:
            response = {
                "status": "error",
                "message": "Id not found"
            }
            return Response(json.dumps(response), status=400,
                            mimetype="application/json")
        else:
            response = {
                "status": "success",
                "data": movie_ids[0]
            }
            return Response(json.dumps(response), status=200,
                            mimetype="application/json")


api.add_resource(Movies, '/movies', endpoint="movies")
api.add_resource(Movie, '/movies/<int:id>', endpoint="movie")


if __name__ == "__main__":
    app.run(debug=True)
