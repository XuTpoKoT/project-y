# coding=utf-8

from flask import Flask, request, url_for, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
import sqlite3
import random

# Пользовательские модули
sys.path.insert(0, "../films_db")
import films_db
import convert
import search

def validate_client_data(film_list):
    upper_limit = 20
    if film_list:
        for i in range(len(film_list)):
            if len(film_list[i]['title']) > upper_limit:
                film_list[i]['title'] = film_list[i]['title'][0:upper_limit] + '...'
        for i in range(len(film_list)):
            film_list[i]['genres'] = film_list[i]['genres'].split(', ')[0]
        for i in range(len(film_list)):
            if (film_list[i]['img_path']):
                film_list[i]['img_path'] = url_for('static', filename=film_list[i]['img_path'])
# Инициализация Flask
app = Flask(__name__)

# Роут основной страницы
@app.route('/', methods=['GET', 'POST'])
def main_page():
    conn = sqlite3.connect("../films_db/database/films.sql")
    cur = conn.cursor()

    # Жанры
    genres = [
        'документальный'.capitalize(),
        'фэнтези'.capitalize(),
        'комедия'.capitalize(),
        'музыка'.capitalize(),
        'мелодрама'.capitalize(),
        'мюзикл'.capitalize(),
        'мультфильм'.capitalize(),
        'короткометражка'.capitalize(),
        'семейный'.capitalize(),
        'драма'.capitalize(),
        'криминал'.capitalize(),
        'детектив'.capitalize(),
        'биография'.capitalize(),
        'спорт'.capitalize(),
        'боевик'.capitalize(),
        'детский'.capitalize(),
        'приключения'.capitalize(),
        'ток-шоу'.capitalize(),
        'концерт'.capitalize(),
        'история'.capitalize(),
        'фантастика'.capitalize(),
        'военный'.capitalize(),
        'игра'.capitalize(),
        'триллер'.capitalize(),
        'реальное ТВ'.capitalize(),
        'ужасы'.capitalize(),
        'аниме'.capitalize(),
    ]

    # Работа с рекомендациями
    film_recommendations = [
        films_db.get_data_film(random.randint(1, 100), cur) for i in range(12, 22)
    ]
    validate_client_data(film_recommendations)
    # Работа с листом фильмов
    film_list = [films_db.get_data_film(i, cur) for i in range(1, 11)]
    validate_client_data(film_list)

    if request.method == 'POST' and not request.form.get('substr'):
        # Получение фильмов по жанру (отдел настроек)
        genre = request.form.get('genre')

        film_list = search.filter_by_genre(genre, 30, 0, cur)

        validate_client_data(film_list)

        return render_template('index.html', 
            film_recommendations=film_recommendations, 
            film_list = film_list, 
            genres = genres,
            film_menu = [])
        
    if request.method == 'POST' and request.form.get('substr'):
        # Получение фильмов по жанру (отдел настроек)
        substr = request.form.get('substr')
        response = search.find(substr, cur)
        print(response)
        film_menu = response['films']

        return render_template('index.html', 
            film_recommendations=film_recommendations, 
            film_list = film_list, 
            genres = genres,
            film_menu = film_menu)

    return render_template('index.html', 
        film_recommendations=film_recommendations, 
        film_list = film_list, 
        genres = genres,
        film_menu = [])

@app.route('/<id>')
def film_page(id):
    conn = sqlite3.connect("../films_db/database/films.sql")
    cur = conn.cursor()

    film = films_db.get_data_film(id, cur)

    all_actors = film['actors'].split(', ')
    film['actors'] = all_actors

    if len(film['genres'].split(', ')) > 2:
        current = [film['genres'].split(', ')[i] for i in range(2)]
        film['genres'] = ', '.join(current)

    if len(film['title']) > 30:
        film['title'] = film['title'][:33] + '...'

    film['img_path'] = url_for('static', filename=film['img_path'])

    return render_template('page.html', 
        film=film)
if __name__ == '__main__':
    app.run(debug=True)