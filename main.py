from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse as response
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()
app.title = "My FastAPI application"
app.version = '0.0.1'


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(
        min_length=15, max_length=50)
    year: int = Field(le=2024)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 99,
                    "title": "The Hyper Human",
                    "overview": "movie description ....",
                    "year": "2018",
                    "rating": 8.8,
                    "category": "fantasy"
                }
            ]
        }
    }


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
def get_movie(id: int = Path(ge=1, le=2000)):
    for movie in movies:
        # print(movie['title'])
        if movie['id'] == id:
            return movie
    return []


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    # for item in movies:
    #     print(item['category'])
    #     if item['category'] == category:
    #         return item
    return list(filter(lambda movie: movie['category'] == category, movies))


@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie.model_dump())
    return movies


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies


@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
