import json
from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

# Инициализация Flask
app = Flask(__name__)

# Роут основной страницы
@app.route('/', methods=['GET', 'POST'])
def main_page():
    films = [
        {
            "title": "Матрица",
            "rating": "9.0",
            "imageUrl": "",
        },
        {
            "title": "Крестный отец",
            "rating": "8.0",
            "imageUrl": "",
        },
        {
            "title": "Онеме",
            "rating": "9.5",
            "imageUrl": "",
        },
        {
            "title": "Онеме",
            "rating": "9.5",
            "imageUrl": "",
        },
        {
            "title": "Онеме",
            "rating": "9.5",
            "imageUrl": "",
        },
        {
            "title": "Онеме",
            "rating": "9.5",
            "imageUrl": "",
        },
    ]
    genres = [
        'вестерн',
        'ужасы',
        'приключения',
        'документальный',
        'аниме',
        'документальный',
        'фэнтези',
        'комедия',
        'музыка',
        'мелодрама',
        'мюзикл',
        'мультфильм',
        'короткометражка',
        'семейный',
        'драма',
        'криминал',
        'детектив',
    ]
    return render_template('index.html', articles=[films, genres])

if __name__ == '__main__':
    app.run(debug=True)