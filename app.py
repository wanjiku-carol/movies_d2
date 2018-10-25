import json
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


with open('mock_data.json', "r") as file:
    movies = json.load(file)


def search_movie_by_name(movie_lst, name):
    for movie in movie_lst:
        for key, value in movie.items():
            if name == movie["name"]:
                return movie


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
        "per_page": limit
    }
    if int(page) > len(all_pages):
        response["data"] = []
    else:
        response["data"] = all_pages[page - 1]
    return response


class Movies(Resource):
    def get(self):
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
                res = {
                    "status": "success",
                    "data": response,
                    "total": len(response)
                }
                return (res)
            if page:
                page = abs(int(page))
                res = paginate(response, page=page)
            if limit:
                limit = abs(int(limit))
                res = paginate(response, limit=limit)
                if len(response) < limit:
                    res = {
                        "status": "error",
                        "message": "Please remove the limit or page"
                    }
            if page and limit:
                res = paginate(response, limit=limit, page=page)
        else:
            response = movies
            res = paginate(response)
        return (res)


class Movie(Resource):
    def get(self, id):
        for movie in movies:
            for key, value in movie.items():
                if id == movie["id"]:
                    response = {
                        "status": "success",
                        "data": movie
                    }
        return response


api.add_resource(Movies, '/movies', endpoint="movies")
api.add_resource(Movie, '/movies/<int:id>', endpoint="movie")


if __name__ == "__main__":
    app.run(debug=True)
