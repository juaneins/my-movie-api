from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse as response


app = FastAPI()
app.title = "My FastAPI application"
app.version = '0.0.1'

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'thriller'
    },
    {
        'id': 2,
        'title': 'Terminator',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2005',
        'rating': 9.8,
        'category': 'scify'
    },
    {
        'id': 3,
        'title': 'The Hobbit',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2019',
        'rating': 8.8,
        'category': 'fantasy'
    }
]


@app.get("/", tags=['home'])
def message():
    return response("""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """)


@app.get("/movies", tags=['movies'])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=['movie'])
def get_movie(id: int):
    for movie in movies:
        # print(movie['title'])
        if movie['id'] == id:
            return movie
    return []


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    # for item in movies:
    #     print(item['category'])
    #     if item['category'] == category:
    #         return item
    return list(filter(lambda movie: movie['category'] == category, movies))


@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })
    return movies


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    for item in movies:
        if item['id'] == id:
            item['title'] = title
            item['overview'] = overview
            item['year'] = year
            item['rating'] = rating
            item['category'] = category
            return movies


@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
