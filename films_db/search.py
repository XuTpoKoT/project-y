import convert


def find(string, cur):
    """
    Возвращает результат поиск по подстроке в базе с фильмами

    string - строка, по которой выполняется поиск
    cur - объект курсора sqlite3
    """

    string = string.capitalize()
    # Выполняем поиск фильмов
    # Начинается с string
    cur.execute("SELECT film_id, title, original_title "
                "FROM film_info NATURAL JOIN rating "
                "WHERE title LIKE '{0}%' OR original_title LIKE '{0}%' "
                "ORDER BY kinopoisk DESC "
                "LIMIT 3".format(string))
    films_start_with = cur.fetchall()

    films = films_start_with.copy()
    if len(films) < 3:
        # В составе какого-то слова
        cur.execute("SELECT film_id, title, original_title "
                    "FROM film_info NATURAL JOIN rating "
                    "WHERE title LIKE '_%{0}%' OR original_title LIKE '_%{0}%' "
                    "ORDER BY kinopoisk DESC "
                    "LIMIT 3 ".format(string))
        films_contained_in = cur.fetchall()

        while len(films) < 3 and len(films_contained_in) > 0:
            films.append(films_contained_in.pop())

    string = string.lower()

    # Выполняем поиск актеров
    # Начинается с string
    cur.execute("SELECT actor_id, output_name "
                "FROM actors "
                "WHERE search_name LIKE '{0}%' "
                "LIMIT 3".format(string))
    actors_start_with = cur.fetchall()

    actors = actors_start_with.copy()
    if len(actors) < 3:
        # В составе какого-то слова
        cur.execute("SELECT actor_id, output_name "
                    "FROM actors "
                    "WHERE search_name LIKE '_%{0}%' "
                    "LIMIT 3".format(string))
        actors_contained_in = cur.fetchall()

        while len(actors) < 3 and len(actors_contained_in) > 0:
            actors.append(actors_contained_in.pop())

    # Выполняем поиск режиссеров
    # Начинается с string
    cur.execute("SELECT director_id, output_name "
                "FROM directors "
                "WHERE search_name LIKE '{0}%' "
                "LIMIT 3".format(string))
    directors_start_with = cur.fetchall()

    directors = directors_start_with.copy()
    if len(directors) < 3:
        # В составе какого-то слова
        cur.execute("SELECT director_id, output_name "
                    "FROM directors "
                    "WHERE search_name LIKE '_%{0}%' "
                    "LIMIT 3".format(string))
        directors_contained_in = cur.fetchall()

        while len(directors) < 3 and len(directors_contained_in) > 0:
            directors.append(directors_contained_in.pop())

    return {"films": films, "actors": actors, "directors": directors}


def filter_by_genre(genre, count, offset, cur):
    """
    Возвращает список фильмов заданного жанра отсортированный по возрастанию рейтинга

    genre - название жанра из таблицы с жанрами
    count - количество фильмао для возврата
    offset - смещение поиска
    cur - объект курсора базы sqlite3
    """

    # Получаем genre_id
    cur.execute("SELECT genre_id FROM genres WHERE genre = '{}'".format(genre))
    temp = cur.fetchone()
    if temp is None:
        return None
    else:
        genre_id = temp[0]

    # Получаем список фильмов
    cur.execute("SELECT film_id "
                "FROM film_info NATURAL JOIN rating "
                "WHERE film_id IN "
                "(SELECT film_id FROM genres_films WHERE genre_id = {0}) "
                "ORDER BY kinopoisk DESC "
                "LIMIT {1}, {2}".format(genre_id, offset, count))
    result = []
    for x in cur.fetchall():
        film_id = x[0]
        result.append(get_data_film(film_id, cur))

    return result


def multi_filter(data, count, offset, cur):
    sql_statement = "SELECT film_id FROM film_info NATURAL JOIN rating WHERE "
    need_and = False

    if data.get("year") is not None:
        year = data["year"]
        need_and = True
        sql_statement += " year = {0} ".format(year)

    if data.get("genre") is not None:
        genre = data["genre"]

        cur.execute("SELECT genre_id FROM genres WHERE genre = '{}'".format(genre))
        temp = cur.fetchone()
        if temp is None:
            return None
        else:
            genre_id = temp[0]

        if need_and:
            sql_statement += " AND "
        need_and = True

        sql_statement += " film_id IN (SELECT film_id FROM genres_films WHERE genre_id = {0}) ".format(genre_id)

    if data.get("country") is not None:
        country = data.get("country").lower()

        cur.execute("SELECT country_id "
                    "FROM countries "
                    "WHERE search_country = ?", (country,))

        temp = cur.fetchone()
        if temp is None:
            return None
        else:
            country_id = temp[0]

        if need_and:
            sql_statement += " AND "
        need_and = True

        sql_statement += " film_id IN (SELECT film_id FROM countries_films WHERE country_id = {0}) ".format(
            country_id)

    if not need_and:
        return None
    sql_statement += " ORDER BY kinopoisk DESC LIMIT {0}, {1} ".format(offset, count)

    print(sql_statement)
    result = []
    for row in cur.execute(sql_statement).fetchall():
        result.append(get_data_film(row[0], cur))
    return result


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
    directors = get_directors(film_id, cur)
    data_film["director"] = convert.from_directors(directors)

    # Актеры
    actors = get_actors(film_id, cur)
    data_film["actors"] = convert.from_actors(actors)

    # Жанры
    genres = get_genres(film_id, cur)
    data_film["genres"] = convert.from_genres(genres)

    # Рейтинг
    rating = get_rating(film_id, cur)
    data_film.update(convert.from_rating(rating))

    # Страны
    countries = get_countries(film_id, cur)
    data_film["countries"] = convert.from_countries(countries)

    cur.execute("SELECT img_path "
                "FROM images_films "
                "WHERE film_id = ?", (film_id,))

    data_film["img_path"] = cur.fetchone()[0]

    return data_film


def get_rating(film_id, cur):
    cur.execute("SELECT kinopoisk, kinopoisk_count, imdb, imdb_count "
                "FROM rating "
                "WHERE film_id = ?", (film_id,))
    result = cur.fetchone()
    return result


def get_genres(film_id, cur):
    cur.execute("SELECT genre "
                "FROM genres "
                "WHERE genre_id IN "
                "(select genre_id from genres_films "
                "WHERE film_id = ?)", (film_id,))
    result = cur.fetchall()
    return result


def get_actors(film_id, cur):
    cur.execute("SELECT output_name "
                "FROM actors "
                "WHERE actor_id IN "
                "(select actor_id from actors_films "
                "WHERE film_id = ?)", (film_id,))

    result = cur.fetchall()
    return result


def get_directors(film_id, cur):
    cur.execute("SELECT output_name "
                "FROM directors "
                "WHERE director_id IN "
                "(SELECT director_id from directors_films "
                "WHERE film_id = ?)", (film_id,))

    result = cur.fetchall()
    return result


def get_countries(film_id, cur):
    cur.execute("SELECT country "
                "FROM countries "
                "WHERE country_id IN "
                "(SELECT country_id from countries_films "
                "WHERE film_id = ?)", (film_id,))
    result = cur.fetchall()
    return result


def get_all_genres(cur):
    cur.execute("SELECT country "
                "FROM coutries")
    result = cur.fetchall()
    return result


if __name__ == "__main__":
    pass
