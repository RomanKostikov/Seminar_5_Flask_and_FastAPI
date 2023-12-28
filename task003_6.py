# Задание №3
# Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Реализуйте валидацию данных запроса и ответа.
# Задание №6
# Создать веб-страницу для отображения списка пользователей. Приложение
# должно использовать шаблонизатор Jinja для динамического формирования HTML
# страницы.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
# содержать заголовок страницы, таблицу со списком пользователей и кнопку для
# добавления нового пользователя.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from pydantic_models import User


app = FastAPI()
templates = Jinja2Templates(directory='./templates')
users: list[User] = []


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        'users.html', {'request': request, 'users': users}
    )


@app.post('/')
async def add_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    id: int = Form(...),
):
    user = User(
        id=int(id),
        name=name,
        email=email,
        password=password,
    )
    users.append(user)
    return user


@app.post('/users/')
async def create_user(user: User):
    users.append(user)
    return user


@app.put('/users/{user_id}')
async def update_user(user_id: int, new_user: User):
    filtered_users = [user for user in users if user.id == user_id]
    if not filtered_users:
        return {'updated': False}

    user = filtered_users[0]

    user.name = new_user.name
    user.email = new_user.email
    user.password = new_user.password

    return {'updated': True, 'user': new_user}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    filtered_users = [user for user in users if user.id == user_id]
    if not filtered_users:
        return {'deleted': False}

    user = filtered_users[0]

    users.remove(user)

    return {'deleted': True, 'user': user}