from fastapi import FastAPI
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
