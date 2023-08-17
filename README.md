# my-movie-api

## create virtual env

python -m venv venv

## activate venv

source venv/bin/activate

## Install modules

pip install fastapi

pip install "uvicorn[standard]"

## Execute

app = FastAPI() --> app is the name of the instance

uvicorn main:app

uvicorn main:app --reload --port 5000 --host 0.0.0.0 --> hot changes

# DataBase

pip install sqlalchemy
