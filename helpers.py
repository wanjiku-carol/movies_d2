def search_movie(movie_lst, q):
    """Allows searching for a movie based on genre and name"""
    results = []
    for movie in movie_lst:
        name = movie.get('name')
        genre = movie.get('genre')
        if q.lower() in name.lower() or q.lower() in genre.lower():
            results.append(movie)
    return results


def create_new_list(name):
    """Allows for creation of a new list"""
    name = []
    return name


def get_total_pages(limit, data):
    """Allows to get the total number of pages depending on the data and limit"""
    if len(data) % limit:
        total = len(data) // limit + 1
    else:
        total = len(data) // limit
    return total


def paginate(data, page=1, limit=10):
    """Paginates data"""
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
