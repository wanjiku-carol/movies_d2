import json
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


with open('mock_data.json', "r") as file:
    movies = json.load(file)


def search_movie(movie_lst, q):
    results = []
    for movie in movie_lst:
        name = movie.get('name')
        genre = movie.get('genre')
        if q.lower() in name.lower() or q.lower() in genre.lower():
            results.append(movie)
    return results


def create_new_list(name):
    name = []
    return name


def get_total_pages(limit, data):
    if len(data) % limit:
        total = len(data) // limit + 1
    else:
        total = len(data) // limit
    return total


def paginate(data, page=1, limit=10):
    pages = get_total_pages(limit, data)
    start = 0
    finish = limit
    all_pages = []
    limit_data = data[start: finish]
    for i in range(pages + 1):
        new_page = create_new_list(i)
        all_pages.append(new_page)
    for one_page in all_pages:
        one_page.append(limit_data)
        start = finish
        finish = finish + limit
        limit_data = data[start: finish]
    response = {
        "status": "success",
        "total": pages,
        "per_page": limit,
        "page": page
    }
    if int(page) > len(all_pages):
        response["data"] = []
    else:
        response["data"] = all_pages[page - 1]
    return response


class Movies(Resource):
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
