EMPTY_SYMBOL = "—"

def count2int(count):
    if count is None:
        return None
    count = count.replace(" ", "")
    count = count.replace(",", ".")
    pos = count.find("K")
    if not count[:pos].replace(".", "").isdigit():
        return None
    if pos == -1:
        return int(count)
    return int(float(count[:pos]) * 1000)


def int2count(number):
    if number is None:
        return None
    result = ""
    while number % 1000 == 0:
        result += "K"
        number //= 1000
    number = str(number)
    if len(number) > 3:
        number = number[:-3] + " " + number[-3:]
    result = number + result
    return result


def value2str(text):
    if text is None:
        text = EMPTY_SYMBOL
    return text


def to_film_info(data_film):
    """
    Преобразует данные из парсера в данные для записи в базу  
    """
    film_info = [data_film["type"], data_film["title"]]

    if data_film["original_title"] is not None:
        film_info.append(data_film["original_title"])
    else:
        film_info.append(data_film["title"])

    try:
        temp = int(data_film["year"].split()[0])
    except ValueError:
        temp = None
    film_info.append(temp)

    film_info.append(data_film["country"])
    film_info.append(data_film["budget"])
    film_info.append(data_film["runtime"])

    temp = data_film["world_gross"]
    if temp is not None:
        if temp.find("=") != -1:
            temp = temp.split("=")[1].strip()
    film_info.append(temp)

    film_info.append(data_film["age"])
    film_info.append(data_film["description"])

    return tuple(film_info)


def from_film_info(film_info):
    result = {"title": value2str(film_info[2]),
              "original_title": value2str(film_info[3]),
              "year": value2str(film_info[4]),
              "budget": value2str(film_info[5]),
              "runtime": value2str(film_info[6]),
              "world_gross": value2str(film_info[7]),
              "age": value2str(film_info[8]),
              "description": value2str(film_info[9])}
    return result


def to_rating(data_film):
    result = []

    temp = data_film["rating"]
    if temp is not None:
        temp = float(temp)
    result.append(temp)

    result.append(count2int(data_film["count"]))

    temp = data_film["rating_imdb"]
    if temp is not None:
        temp = float(temp)
    result.append(temp)

    result.append(count2int(data_film["count_imdb"]))

    return tuple(result)


def from_rating(rating):
    if rating is None:
        return None

    result = {"kinopoisk": value2str(rating[0]),
              "kinopoisk_count": value2str(int2count(rating[1])),
              "imdb": value2str(rating[2]),
              "imdb_count": value2str(int2count(rating[3]))}
    return result


def from_genres(genres):
    if genres is None:
        return None

    if len(genres) == 0:
        genres = EMPTY_SYMBOL
    else:
        genres = ', '.join([genre for (genre,) in genres])
    return genres


def from_actors(actors):
    if actors is None:
        return None

    if len(actors) == 0:
        actors = EMPTY_SYMBOL
    else:
        actors = ', '.join([actor for (actor,) in actors])
    return actors


def from_directors(directors):
    if directors is None:
        return None

    if len(directors) == 0:
        directors = EMPTY_SYMBOL
    else:
        directors = ', '.join([director for (director,) in directors])
    return directors


def from_countries(countries):
    if countries is None:
        return None

    if len(countries) == 0:
        countries = EMPTY_SYMBOL
    else:
        countries = ', '.join([country for (country,) in countries])
    return countries