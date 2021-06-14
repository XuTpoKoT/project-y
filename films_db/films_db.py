import sqlite3

import convert

conn = sqlite3.connect("films.sql")
cur = conn.cursor()


def init():
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
        runtime TEXT,
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

    cur.execute("""CREATE TABLE IF NOT EXISTS images_films(
        film_id INTEGER, 
        img_path TEXT,
        url TEXT);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS rating(
        film_id INTEGER PRIMARY KEY ASC,
        kinopoisk REAL,
        kinopoisk_count INT,
        imdb REAL,
        imdb_count INT,
        FOREIGN KEY (film_id) REFERENCES film_info(film_id))
    """)

    conn.commit()


def insert_film(data_film):
    """
    Помещает данные о фильме в таблицу
    """

    film_info = convert.to_film_info(data_film)

    if data_film["director"] is None:
        directors = tuple()
    else:
        directors = [(i.strip().lower(), i.strip()) for i in data_film["director"].split(",")]

    if data_film["actors"] is None:
        actors = tuple()
    else:
        actors = [(i.strip().lower(), i.strip()) for i in data_film["actors"].split(",")]

    if data_film["genres"] is None:
        genres = tuple()
    else:
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
    cur.execute(
        "INSERT OR IGNORE INTO directors(search_name, output_name) SELECT search_name, output_name FROM temp_directors")
    cur.execute(
        "INSERT OR IGNORE INTO actors(search_name, output_name) SELECT search_name, output_name FROM temp_actors")
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
    director_ids = cur.execute("SELECT director_id "
                               "FROM directors "
                               "WHERE search_name IN "
                               "(SELECT search_name FROM temp_directors)")
    directors_films = [(director_id, film_id) for (director_id,) in director_ids]
    cur.executemany("INSERT INTO directors_films VALUES(?, ?)", directors_films)

    actor_ids = cur.execute("SELECT actor_id "
                            "FROM actors "
                            "WHERE search_name IN "
                            "(SELECT search_name FROM temp_actors)")
    actors_films = [(actor_id, film_id) for (actor_id,) in actor_ids]
    cur.executemany("INSERT INTO actors_films VALUES(?, ?)", actors_films)

    genre_ids = cur.execute("SELECT genre_id FROM genres WHERE genre IN temp_genres")
    genres_films = [(genre_id, film_id) for (genre_id,) in genre_ids]
    cur.executemany("INSERT INTO genres_films VALUES(?, ?)", genres_films)

    # Очищаем временные таблицы
    cur.execute("DELETE FROM temp_directors")
    cur.execute("DELETE FROM temp_actors")
    cur.execute("DELETE FROM temp_genres")

    images_films_val = (film_id, data_film.get("image"), data_film.get("image_url"))

    rating = (film_id, *convert.to_rating(data_film))

    # Сохраняем ссылку на постер фильма
    cur.execute("INSERT INTO images_films VALUES(?, ?, ?)", images_films_val)

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


def get_data_film(film_id, cur):
    data_film = {"film_id": film_id}

    # Информация о фильме
    cur.execute("SELECT * "
                "FROM film_info "
                "WHERE film_id = ?", (film_id,))
    film_info = cur.fetchone()

    data_film.update(convert.from_film_info(film_info))

    cur.execute("SELECT name "
                "FROM film_types "
                "WHERE type = ?", (film_info[1],))

    data_film["type"] = cur.fetchone()[0]

    # Режиссеры
    cur.execute("SELECT output_name "
                "FROM directors "
                "WHERE director_id IN "
                "(select director_id from directors_films "
                "WHERE film_id = ?)", (film_id,))

    directors = cur.fetchall()
    if len(directors) == 0:
        directors = "—"
    else:
        directors = [director for (director,) in directors]

    data_film["director"] = ", ".join(directors)

    # Актеры
    cur.execute("SELECT output_name "
                "FROM actors "
                "WHERE actor_id IN "
                "(select actor_id from actors_films "
                "WHERE film_id = ?)", (film_id,))

    actors = cur.fetchall()
    if len(actors) == 0:
        actors = "—"
    else:
        actors = [actor for (actor,) in actors]

    data_film["actors"] = ", ".join(actors)

    # Жанры
    cur.execute("SELECT genre "
                "FROM genres "
                "WHERE genre_id IN "
                "(select genre_id from genres_films "
                "WHERE film_id = ?)", (film_id,))

    genres = cur.fetchall()
    if len(genres) == 0:
        genres = "—"
    else:
        genres = [genre for (genre,) in genres]

    data_film["genres"] = ", ".join(genres)

    # Рейтинг
    cur.execute("SELECT kinopoisk, kinopoisk_count, imdb, imdb_count "
                "FROM rating "
                "WHERE film_id = ?", (film_id,))
    rating = cur.fetchone()

    data_film.update(convert.from_rating(rating))

    cur.execute("SELECT img_path "
                "FROM images_films "
                "WHERE film_id = ?", (film_id,))

    data_film["img_path"] = cur.fetchone()[0]

    return data_film


if __name__ == "__main__":
    init()
