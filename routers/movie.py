from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from pydantic import BaseModel, Field
from http import HTTPStatus
from typing import Optional
from config.database import Session
from typing import List
from fastapi.encoders import jsonable_encoder

movie_router = APIRouter()


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
                    "year": 2018,
                    "rating": 8.8,
                    "category": "fantasy"
                }
            ]
        }
    }


@movie_router.get("/movies", tags=['movies'], response_model=List[Movie], status_code=HTTPStatus.OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=HTTPStatus.OK, content=jsonable_encoder(result))


@movie_router.get("/movies/{id}", tags=['movie'], response_model=List[Movie], status_code=HTTPStatus.OK)
def get_movie(id: int = Path(ge=1, le=2000)):
    # for movie in movies:
    #     # print(movie['title'])
    #     if movie['id'] == id:
    #         return JSONResponse(status_code=HTTPStatus.OK, content=movie)
    # return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content=[])
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={'message': "Not found!"})
    return JSONResponse(status_code=HTTPStatus.OK, content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=['movies'], response_model=Movie, status_code=HTTPStatus.OK)
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    # for item in movies:
    #     print(item['category'])
    #     if item['category'] == category:
    #         return item
    # return JSONResponse(status_code=HTTPStatus.OK, content=list(filter(lambda movie: movie['category'] == category, movies)))
    db = Session()
    result = db.query(MovieModel).filter(
        MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Not found!"})
    return JSONResponse(status_code=HTTPStatus.OK, content=jsonable_encoder(result))


@movie_router.post('/movies', tags=['movies'], status_code=HTTPStatus.CREATED)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    # movies.append(movie.model_dump())
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "The movie has been registered"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=HTTPStatus.OK)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={'message': "The movie hasn't been found"})

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=HTTPStatus.OK, content={'message': "The movie has been updated"})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=HTTPStatus.OK)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={'message': "The movie hasn't been found"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "The movie has been deleted"})
