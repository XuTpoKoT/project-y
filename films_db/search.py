from films_db import conn, cur


def find(string):
    """
    Возвращает
    :return:
    """

    if len(string) < 2:
        return None

    # Выход будет разбит на 3 части: фильмы, актеры, режиссеры

    # Выполняем поиск фильмов
    # Полное совпадения
    cur.execute("SELECT film_id, title, original_title FROM film_info WHERE title = ? OR original_title = ?",
                (string, string))
    complete_match = cur.fetchall()

    # Начинается с string
    cur.execute("SELECT film_id, title, original_title"
                "FROM film_info NATURAL JOIN rating"
                "WHERE title LIKE '{0}%' OR original_title LIKE '{0}%'"
                "ORDER BY kinopoisk DESC".format(string))
    start_with = cur.fetchall()

    # В составе какого слова
    cur.execute("SELECT film_id, title, original_title"
                "FROM film_info NATURAL JOIN rating"
                "WHERE title LIKE '%{0}%' OR original_title LIKE '%{0}%'"
                "ORDER BY kinopoisk DESC".format(string))
    contained_in = cur.fetchall()

    films = complete_match.copy()

    for row in start_with + contained_in:
        if row not in films:
            films.append(row)

    # Выполняем поиск актеров
    # Полное совпадения
    cur.execute("SELECT actor_id, output_name"
                "FROM actors"
                "WHERE search_name = ?", (string,))
    complete_match = cur.fetchall()

    # Начинается с string
    cur.execute("SELECT actor_id"
                "FROM film_info NATURAL JOIN rating"
                "WHERE title LIKE '{0}%' OR original_title LIKE '{0}%'"
                "ORDER BY kinopoisk DESC".format(string))
    start_with = cur.fetchall()

    # В составе какого слова
    cur.execute("SELECT actor_id, output_name FROM actors WHERE search_name LIKE '%{0}%'".format(string))
    contained_in = cur.fetchall()

    actors = complete_match.copy()

    for row in start_with + contained_in:
        if row not in actors:
            actors.append(row)
    return {"films": films, "actors": actors}


if __name__ == "__main__":
    find("даг")
