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
        films_db.get_data_film(i, cur) for i in range(12, 22)
    ]
    if film_recommendations:
        for i in range(len(film_recommendations)):
            film_recommendations[i]['genres'] = film_recommendations[i]['genres'].split(', ')[0]
        for i in range(len(film_recommendations)):
            film_recommendations[i]['img_path'] = url_for('static', filename=film_recommendations[i]['img_path'])

    # Работа с листом фильмов
    film_list = [
        films_db.get_data_film(i, cur) for i in range(1, 11)
    ]
    if film_list:
        for i in range(len(film_list)):
            film_list[i]['genres'] = film_list[i]['genres'].split(', ')[0]
        for i in range(len(film_list)):
            film_list[i]['img_path'] = url_for('static', filename=film_list[i]['img_path'])

    if request.method == 'POST' and not request.form.get('text'):
        # Получение фильмов по жанру (отдел настроек)
        genre = request.form.get('genre')

        film_list = search.filter_by_genre(genre, 30, 0, cur)

        if film_list:
            for i in range(len(film_list)):
                film_list[i]['genres'] = film_list[i]['genres'].split(', ')[0]
            for i in range(len(film_list)):
                film_list[i]['img_path'] = url_for('static', filename=film_list[i]['img_path'])
        
        # print('GENRE :'+ str(genre))
        # print('\nFILM_LIST')
        # print(str(type(film_list)) + '\n')
        # print(film_list)

        return render_template('index.html', 
        film_recommendations=film_recommendations, 
        film_list = film_list, 
        genres = genres)

    print(film_list)
    return render_template('index.html', 
        film_recommendations=film_recommendations, 
        film_list = film_list, 
        genres = genres)

@app.route('/<id>')
def film_page(id):
    conn = sqlite3.connect("../films_db/database/films.sql")
    cur = conn.cursor()

    film = films_db.get_data_film(id, cur)

    all_actors = film['actors'].split(', ')
    film['actors'] = all_actors

    return render_template('page.html', 
        film=film)
if __name__ == '__main__':
    app.run(debug=True)