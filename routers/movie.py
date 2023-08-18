from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from http import HTTPStatus
from config.database import Session
from typing import List
from fastapi.encoders import jsonable_encoder
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get("/movies", tags=['movies'], response_model=List[Movie], status_code=HTTPStatus.OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=HTTPStatus.OK, content=jsonable_encoder(result))


@movie_router.get("/movies/{id}", tags=['movie'], response_model=List[Movie], status_code=HTTPStatus.OK)
def get_movie(id: int = Path(ge=1, le=2000)):
    db = Session()
    result = MovieService(db).get_movie(id)
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
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Not found!"})
    return JSONResponse(status_code=HTTPStatus.OK, content=jsonable_encoder(result))


@movie_router.post('/movies', tags=['movies'], status_code=HTTPStatus.CREATED)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    # movies.append(movie.model_dump())
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"message": "The movie has been registered"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=HTTPStatus.OK)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={'message': "The movie hasn't been found"})

    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=HTTPStatus.OK, content={'message': "The movie has been updated"})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=HTTPStatus.OK)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={'message': "The movie hasn't been found"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "The movie has been deleted"})
