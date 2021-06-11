import json
from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

# Инициализация Flask
app = Flask(__name__)

# Роут основной страницы
@app.route('/', methods=['GET', 'POST'])
def main_page():

    # Открываем файл DB
    db = open('./database/db1.json', 'r')

    data = json.load(db)
    print(data)

    db.close()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)