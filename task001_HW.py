# Напишите RESTful API по желанию с методами GET, POST, PUT, DELETE
# Для отображения данных по GET-запросам использовать шаблоны Jinja2
# Вывод информации о песнях через шаблонизатор Jinja

import os
import json
from pathlib import Path
import aiofiles
from pydantic import TypeAdapter
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from pydantic_models import Song


BASE_DIR = Path(__file__).resolve().parent
json_file = os.path.join(BASE_DIR, 'data.json')

if not os.path.exists(json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

with open(json_file, encoding='utf-8') as f:
    json_data = json.load(f)

app = FastAPI()
templates = Jinja2Templates('./templates')
type_adapter = TypeAdapter(Song)
music: list[Song] = [type_adapter.validate_python(song) for song in json_data]


async def commit_changes():
    async with aiofiles.open(json_file, 'w', encoding='utf-8') as f:
        json_music = [song.model_dump(mode='json') for song in music]
        content = json.dumps(json_music, ensure_ascii=False, indent=2)
        await f.write(content)


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        'index.html', {'request': request, 'music': music}
    )


@app.post('/music/')
async def add_song(song: Song):
    music.append(song)
    await commit_changes()
    return song


@app.get('/music/{song_id}', response_class=HTMLResponse)
async def get_song(request: Request, song_id: int):
    filtered_songs = [song for song in music if song.id == song_id]

    if not filtered_songs:
        song = None
    else:
        song = filtered_songs[0]

    return templates.TemplateResponse(
        'song.html', {'request': request, 'song': song}
    )


@app.put('/music/{song_id}')
async def update_song(song_id: int, new_song: Song):
    filtered_songs = [song for song in music if song.id == song_id]

    if not filtered_songs:
        return {'updated': False}

    song = filtered_songs[0]

    song.name = new_song.name
    song.author = new_song.author
    song.description = new_song.description
    song.genre = new_song.genre

    await commit_changes()

    return {'updated': True, 'song': new_song}


@app.delete('/music/{song_id}')
async def delete_song(song_id: int):
    filtered_songs = [song for song in music if song.id == song_id]

    if not filtered_songs:
        return {'deleted': False}

    song = filtered_songs[0]
    music.remove(song)

    await commit_changes()

    return {'deleted': True, 'song': song}