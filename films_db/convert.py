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


def value2str(text):
    if text is None:
        text = "—"
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
              "country": value2str(film_info[5]),
              "budget": value2str(film_info[6]),
              "runtime": value2str(film_info[7]),
              "world_gross": value2str(film_info[8]),
              "age": value2str(film_info[9]),
              "description": value2str(film_info[10])}
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
    result = {"kinopoisk": value2str(rating[0]),
              "kinopoisk_count": value2str(rating[1]),
              "imdb": value2str(rating[2]),
              "imdb_count": value2str(rating[3])}
    return result
