# Задание №2
# Создать API для получения списка фильмов по жанру. Приложение должно
# иметь возможность получать список фильмов по заданному жанру.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Movie с полями id, title, description и genre.
# Создайте список movies для хранения фильмов.
# Создайте маршрут для получения списка фильмов по жанру (метод GET).
# Реализуйте валидацию данных запроса и ответа.
from fastapi import FastAPI

from pydantic_models import Movie

app = FastAPI()
movies: list[Movie] = []


@app.get('/')
async def index():
    return movies


@app.get('/movies/{genre}')
async def get_movies(genre: str):
    list_movies = [movie for movie in movies if movie.genre == genre.title()]
    return list_movies


@app.post('/movies/')
async def create_movie(movie: Movie):
    movies.append(movie)
    return movie
