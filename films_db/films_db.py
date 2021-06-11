import sqlite3


def create_films_tables():
    conn = sqlite3.connect('films.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS film_info(
        film_id INTEGER PRIMARY KEY,
        type TEXT,
        title TEXT,
        original_title TEXT,
        year INTEGER,
        country TEXT,
        director TEXT,
        budget TEXT,
        runtime INTEGER,
        world_gross TEXT,
        age TEXT,
        description TEXT);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS directors(
        director_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS directors_films(
        director_id INTEGER,
        film_id INTEGER);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS actors(
        actor_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS actors_films(
        actor_id INTEGER,
        film_id INTEGER);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS genres(
        genre_id INTEGER PRIMARY KEY,
        genre TEXT UNIQUE);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS genres_films(
        genre_id INTEGER,
        film_id INTEGER);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS images_films(
        film_id INTEGER, 
        url TEXT);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS rating(
        film_id INTEGER PRIMARY KEY,
        kinopoisk FLOAT,
        kinopoisk_count INTEGER,
        imdb FLOAT,
        imdb_count INTEGER
    );
    """)

    conn.commit()
    conn.close()


def text_count_to_integer(count):
    count = count.replace(" ", "")
    count = count.replace(",", ".")
    pos = count.find("K")
    if not count[:pos].replace(".", "").isdigit():       
        return None
    if pos == -1:
        return int(count)
    return (int(float(count[:pos]) * 1000))


def text_runtime_to_integer(runtime):
    pos = runtime.find(" ")
    if not runtime[:pos].isdigit():       
        return None
    return int(runtime[:pos])


def insert_film_info(data_film):
    film_info_val = (data_film["type"],
                     data_film["title"],
                     data_film["original_title"],
                     int(data_film["year"]),
                     data_film["country"],
                     data_film["director"],
                     data_film["budget"],
                     text_runtime_to_integer(data_film["runtime"]),
                     data_film["world_gross"],
                     data_film["age"],
                     data_film["description"])

    directors_val = [(i.strip(),) for i in data_film["director"].split(sep=',')]
    
    actors_val = [(i.strip(),) for i in data_film["actors"].split(sep=',')]

    genres_val = [(i.strip(),) for i in data_film["genres"].split(sep=',')]

    images_films_val = data_film["image_url"],
    
    conn = sqlite3.connect('films.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO film_info(type, title, original_title, "
        "year, country, director, budget, runtime, world_gross, age, "
        "description) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING film_id;", film_info_val)
    film_id = cur.fetchone()
        
    cur.executemany("INSERT OR IGNORE INTO directors(name) VALUES(?);", directors_val)

    cur.executemany("INSERT OR IGNORE INTO actors(name) VALUES(?);", actors_val)

    cur.executemany("INSERT OR IGNORE INTO genres(genre) VALUES(?);", genres_val)

    cur.execute("INSERT INTO images_films(url) VALUES(?);", images_films_val)

    rating_val = (film_id,
                  float(data_film["rating"]),
                  text_count_to_integer(data_film["count"]),
                  float(data_film["rating_imdb"]),
                  text_count_to_integer(data_film["count_imdb"]))
    cur.execute("INSERT INTO rating(film_id, kinopoisk, kinopoisk_count, "
        "imdb, imdb_count) VALUES(?, ?, ?, ?);", rating_val)

    conn.commit()
    conn.close()


def print_all_films():
    conn = sqlite3.connect('films.db')
    cur = conn.cursor()

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

    conn.close()

