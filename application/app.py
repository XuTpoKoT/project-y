from flask import Flask, request, url_for, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
import sqlite3
import random

# Пользовательские модули
sys.path.insert(0, "../films_db")
import films_db
import convert

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
    for i in range(len(film_recommendations)):
        film_recommendations[i]['genres'] = film_recommendations[i]['genres'].split(', ')[0]

    # Работа с листом фильмов
    film_list = [
        films_db.get_data_film(i, cur) for i in range(1, 11)
    ]

    if request.method == 'POST':
        genre = request.form.get('genre')
        film_list = [
            films_db.get_data_film(i, cur) for i in range(50, 70)
        ]

        # print(request)
        # print(request.form)
        # print(genre)

        film_recommendations = [
            films_db.get_data_film(i, cur) for i in range(100, 110)
        ]

        return render_template('index.html', 
        film_recommendations=film_recommendations, 
        film_list = film_list, 
        genres = genres)

    return render_template('index.html', 
        film_recommendations=film_recommendations, 
        film_list = film_list, 
        genres = genres)

if __name__ == '__main__':
    app.run(debug=True)