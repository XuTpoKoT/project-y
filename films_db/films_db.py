import json
import sqlite3

import convert

conn = sqlite3.connect("films.sql")
cur = conn.cursor()

def init_db():
    """
    Инициализация базы данных
    """

    cur.execute("""CREATE TABLE IF NOT EXISTS film_types(
        type INTEGER PRIMARY KEY ASC ON CONFLICT IGNORE,
        name TEXT NOT NULL);
    """)

    film_types = [(0, "фильм"), (1, "сериал")]

    cur.executemany("INSERT INTO film_types(type, name) VALUES (?, ?)", film_types)

    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS film_info(
        film_id INTEGER PRIMARY KEY ASC,
        type INT NOT NULL,
        title TEXT NOT NULL UNIQUE,
        original_title TEXT NOT NULL UNIQUE,
        year INT NOT NULL CHECK (year > 1888),
        country TEXT,
        budget TEXT,
        runtime INT, -- В минутах --
        world_gross TEXT,
        age TEXT,
        description TEXT,
        FOREIGN KEY (type) REFERENCES film_types(type))
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS directors(
        director_id INTEGER PRIMARY KEY ASC,
        search_name TEXT NOT NULL UNIQUE,
        output_name TEXT NOT NULL);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS directors_films(
        director_id INTEGER NOT NULL,
        film_id INTEGER NOT NULL,
        PRIMARY KEY (director_id, film_id) 
        FOREIGN KEY (director_id) REFERENCES directors(director_id),
        FOREIGN KEY (film_id) REFERENCES film_info(film_id))
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS actors(
        actor_id INTEGER PRIMARY KEY ASC,
        search_name TEXT NOT NULL UNIQUE,
        output_name TEXT NOT NULL);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS actors_films(
        actor_id INTEGER NOT NULL,
        film_id INTEGER NOT NULL,
        PRIMARY KEY (actor_id, film_id) 
        FOREIGN KEY (actor_id) REFERENCES actors(actor_id),
        FOREIGN KEY (film_id) REFERENCES film_info(film_id))
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS genres(
        genre_id INTEGER PRIMARY KEY ASC,
        genre TEXT NOT NULL UNIQUE);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS genres_films(
        genre_id INTEGER NOT NULL,
        film_id INTEGER NOT NULL,
        PRIMARY KEY (genre_id, film_id) 
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id),
        FOREIGN KEY (film_id) REFERENCES film_info(film_id))
    """)

    # url же TEXT?
    cur.execute("""CREATE TABLE IF NOT EXISTS images_films(
        film_id INTEGER, 
        url TEXT);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS rating(
        film_id INTEGER PRIMARY KEY ASC,
        kinopoisk REAL NOT NULL,
        kinopoisk_count INT NOT NULL,
        imdb REAL NOT NULL,
        imdb_count INT NOT NULL,
        FOREIGN KEY (film_id) REFERENCES film_info(film_id))
    """)

    conn.commit()


def insert_film(data_film):
    """
    Помещает данные о фильме в таблицу
    """

    film_info = convert.convert_film_info(data_film)

    directors = [(i.strip(), i.strip().lower()) for i in data_film["director"].split(",")]
    actors = [(i.strip(), i.strip().lower()) for i in data_film["actors"].split(",")]
    genres = [(i.strip(),) for i in data_film["genres"].split(",")]

    # Создаем временные таблицы для хранения режиссеров, актеров и жанров фильма
    cur.execute("CREATE TEMP TABLE IF NOT EXISTS temp_directors(search_name, output_name)")
    cur.execute("CREATE TEMP TABLE IF NOT EXISTS temp_actors(search_name, output_name)")
    cur.execute("CREATE TEMP TABLE IF NOT EXISTS temp_genres(genre)")

    # Записываем соответствующие данные во временные таблицы
    cur.executemany("INSERT INTO temp_directors VALUES(?, ?)", directors)
    cur.executemany("INSERT INTO temp_actors VALUES(?, ?)", actors)
    cur.executemany("INSERT INTO temp_genres(genre) VALUES(?)", genres)

    # Записываем данные из верменных таблиц в основные таблицы
    cur.execute("INSERT OR IGNORE INTO directors(search_name, output_name) SELECT search_name, output_name FROM temp_directors")
    cur.execute("INSERT OR IGNORE INTO actors(search_name, output_name) SELECT search_name, output_name FROM temp_actors")
    cur.execute("INSERT OR IGNORE INTO genres(genre) SELECT genre FROM temp_genres")

    # Записываем онсовную информацию о фильме в таблицу filM_info
    try:
        film_id = cur.execute("""INSERT INTO film_info(
            type,
            title,
            original_title,
            year,
            country,
            budget,
            runtime,
            world_gross,
            age,
            description) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, film_info).lastrowid
    except sqlite3.IntegrityError as e:
        print(e)

        cur.execute("DELETE FROM temp_directors")
        cur.execute("DELETE FROM temp_actors")
        cur.execute("DELETE FROM temp_genres")
        conn.commit()

        return False

    # Записываем данные в таблицы соответствий для фильма и соответственно режиссеров, актеров и жанров
    director_ids = cur.execute("SELECT director_id FROM directors WHERE search_name IN temp_directors")
    directors_films = [(director_id, film_id) for (director_id,) in director_ids]
    cur.executemany("INSERT INTO directors_films VALUES(?, ?)", directors_films)

    actor_ids = cur.execute("SELECT actor_id FROM actors WHERE search_name IN temp_actors")
    actors_films = [(actor_id, film_id) for (actor_id,) in actor_ids]
    cur.executemany("INSERT INTO actors_films VALUES(?, ?)", actors_films)

    genre_ids = cur.execute("SELECT genre_id FROM genres WHERE genre IN temp_genres")
    genres_films = [(genre_id, film_id) for (genre_id,) in genre_ids]
    cur.executemany("INSERT INTO genres_films VALUES(?, ?)", genres_films)

    # Очищаем временные таблицы
    cur.execute("DELETE FROM temp_directors")
    cur.execute("DELETE FROM temp_actors")
    cur.execute("DELETE FROM temp_genres")

    images_films_val = (film_id, convert.str2text(data_film["image_url"]))

    rating = (
        film_id,
        float(data_film["rating"]),
        convert.count2int(data_film["count"]),
        float(data_film["rating_imdb"]),
        convert.count2int(data_film["count_imdb"])
    )

    # Сохраняем ссылку на постер фильма
    cur.execute("INSERT INTO images_films VALUES(?, ?)", images_films_val)

    # Сохраняем рейтинг фильма
    cur.execute("INSERT INTO rating VALUES(?, ?, ?, ?, ?);", rating)

    conn.commit()

    return True


def print_all_films():
    cur.execute("SELECT * FROM film_info")
    all_results = cur.fetchall()
    for i in all_results:
        print(i)
    print()

    cur.execute("SELECT * FROM directors")
    all_results = cur.fetchall()
    for i in all_results:
        print(i)
    print()

    cur.execute("SELECT * FROM actors")
    all_results = cur.fetchall()
    for i in all_results:
        print(i)
    print()

    cur.execute("SELECT * FROM genres")
    all_results = cur.fetchall()
    for i in all_results:
        print(i)
    print()

    cur.execute("SELECT * FROM rating")
    all_results = cur.fetchall()
    for i in all_results:
        print(i)
    print()


if __name__ == "__main__":
    init_db()

    print_all_films()


    def test_insert():

        with open("../test_data_film/1.json") as f:
            films = json.load(f)

        for film in films:
            insert_film(film)

    test_insert()
    print_all_films()
