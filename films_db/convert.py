import films_db

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
    return (int(float(count[:pos]) * 1000))


def runtime2int(runtime):
    try:
        return int(runtime.split()[0])
    except:
        return None


def convert_film_info(data_film):
    """
    Преобразует данные из парсера в данные для записи в базу  
    """

    film_info = []

    temp = 0 if data_film["type"] == "фильм" else 1
    film_info.append(temp)

    temp = (data_film["title"])
    film_info.append(temp)

    temp = data_film["original_title"]
    if temp is not None:
        film_info.append(temp)
    else:
        film_info.append(data_film["title"])

    try:
        temp = int(data_film["year"].split()[0])
    except:
        temp = None

    film_info.append(temp)

    temp = data_film["country"]
    film_info.append(temp)

    temp = data_film["budget"]
    film_info.append(temp)

    temp = runtime2int(data_film["runtime"])
    film_info.append(temp)

    temp = data_film["world_gross"]
    if temp is not None:
        if temp.find("=") != -1:
            temp = temp.split("=")[1].strip()
    film_info.append(temp)

    temp = data_film["age"]
    film_info.append(temp)

    temp = data_film["description"]
    film_info.append(temp)

    return tuple(film_info)


def convert_rating(data_film):
    rating = []

    temp = data_film["rating"]
    if temp is not None:
        temp = float(temp)
    rating.append(temp)

    rating.append(count2int(data_film["count"]))

    temp = data_film["rating_imdb"]
    if temp is not None:
        temp = float(temp)
    rating.append(temp)

    rating.append(count2int(data_film["count_imdb"]))

    return rating

def value2str(text):
    if text is None:
        text = "—"
    return text