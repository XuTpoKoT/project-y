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


if __name__ == "__main__":
    pass
