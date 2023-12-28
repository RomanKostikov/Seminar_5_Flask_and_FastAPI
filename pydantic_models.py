from pydantic import BaseModel


# Создайте класс Task с полями id, title, description и status.
class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: bool = False


# Создайте класс Movie с полями id, title, description и genre.
class Movie(BaseModel):
    id: int
    title: str
    description: str | None = None
    genre: str


# Создайте класс User с полями id, name, email и password.
class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


class Song(BaseModel):
    id: int
    name: str
    author: str
    description: str | None = None
    genre: str
