# coding=utf-8

from os import curdir
from re import split
from flask import Flask, request, url_for, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
import sqlite3
import random

from werkzeug.wrappers import response

# Пользовательские модули
sys.path.insert(0, "../films_db")
import films_db
import convert
import search

def validate_client_data_in_list(film_list):
    upper_limit = 20
    words_limit = 3
    if film_list:
        for i in range(len(film_list)):
            for key in film_list[i].keys():
                if film_list[i][key] == None:
                    film_list[i][key] = "-"
        for i in range(len(film_list)):
            if len(film_list[i]['title']) > upper_limit:
                film_list[i]['title'] = film_list[i]['title'][0:upper_limit] + '...'
        for i in range(len(film_list)):
            if len(film_list[i]['genres'].split()) > 3:
                current = film_list[i]['genres'].split()
                film_list[i]['genres'] = current[0]
                for j in range(2):
                    film_list[i]['genres'] += ', ' + current[j + 1]
        for i in range(len(film_list)):
            if film_list[i]['img_path']:
                film_list[i]['img_path'] = url_for('static', filename=film_list[i]['img_path'])
        for i in range(len(film_list)):
            if len(film_list[i]['countries'].split()) > 3:
                current = film_list[i]['countries'].split()
                film_list[i]['countries'] = current[0]
                for j in range(2):
                    film_list[i]['countries'] += ', ' + current[j + 1]

def validate_client_data_in_recomm(film_list):
    upper_limit = 20
    words_limit = 3
    if film_list:
        for i in range(len(film_list)):
            for key in film_list[i].keys():
                if film_list[i][key] == None:
                    film_list[i][key] = "-"
        for i in range(len(film_list)):
            if len(film_list[i]['title']) > upper_limit:
                film_list[i]['title'] = film_list[i]['title'][0:upper_limit] + '...'
        for i in range(len(film_list)):
            film_list[i]['genres'] = film_list[i]['genres'].split(', ')[0]
        for i in range(len(film_list)):
            if film_list[i]['img_path']:
                film_list[i]['img_path'] = url_for('static', filename=film_list[i]['img_path'])
        for i in range(len(film_list)):
            if len(film_list[i]['countries'].split()) > 3:
                current = film_list[i]['countries'].split()
                film_list[i]['countries'] = current[0]
                for j in range(2):
                    film_list[i]['countries'] += ', ' + current[j + 1]


# Инициализация Flask
app = Flask(__name__)

# Роут основной страницы
@app.route('/', methods=['GET', 'POST'])
def main_page():
    conn = sqlite3.connect("../database/films.sql")
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
    film_recommendations = search.get_recommendations(20, cur)
    validate_client_data_in_recomm(film_recommendations)
    # Работа с листом фильмов 
    film_list = search.multi_filter({}, 40, 0, cur)
    validate_client_data_in_list(film_list)

    print(request.form.get('substr'))
    print(type(request.form.get('substr')))
    if request.method == 'POST' and not request.form.get('substr'):
        # Получение фильмов по жанру (отдел настроек)
        genre = request.form.get('genre')
        year = request.form.get('year')
        if not year:
            film_list = search.filter_by_genre(genre, 30, 0, cur)
        
        if year:
            film_list = search.multi_filter(request.form, 10, 0, cur)

        if film_list:
            validate_client_data_in_list(film_list)
            
        return render_template('index.html', 
            film_recommendations=film_recommendations, 
            film_list = film_list, 
            genres = genres,
            film_menu = [])
        
    if request.method == 'POST' and request.form.get('substr'):
        # Получение фильмов по жанру (отдел настроек)
        substr = request.form.get('substr')
        response = search.find(substr, cur)


        film_menu = []
        film_menu.append([search.get_data_film(film[0], cur) for film in response['films']])
        validate_client_data_in_list(film_menu[0])

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
    conn = sqlite3.connect("../database/films.sql")
    cur = conn.cursor()

    film = search.get_data_film(id, cur)

    all_actors = film['actors'].split(', ')
    film['actors'] = all_actors

    if len(film['genres'].split(', ')) > 2:
        current = [film['genres'].split(', ')[i] for i in range(2)]
        film['genres'] = ', '.join(current)

    if len(film['title']) > 30:
        film['title'] = film['title'][:30] + '...'

    return render_template('page.html', 
        film=film)

if __name__ == '__main__':
    app.run(debug=True)