import socks
import socket
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def delay():
    time.sleep(2)


def parsingTable(start, end):
    page = start
    while page < end:
        delay()
        response_table = getResponseTable(page)
        if response_table is None:
            print("Err: no internet connection.")
            continue

        soup_table = BeautifulSoup(response_table.text, "lxml")

        films = getFilms(soup_table)
        if films is None:
            print("Err: error in parsing the page.")
            continue

        len_films = len(films)
        if len_films == 0:
            print("Err: the page didn't load.")
            continue

        print(f"on page {page} uploaded {len_films} films.")
        ids_films, values_films = filmsHandler(films)
        parsingFilm(len_films, ids_films, values_films)

        page += 1


def getResponseTable(current_page):
    link_table = f"https://www.kinopoisk.ru/lists/navigator/?page={current_page}&sort=popularity&tab=all"

    try:
        return requests.get(link_table, headers={'User-Agent': UserAgent().chrome}, timeout=10)
    except:
        return None


def getFilms(soup):
    try:
        return soup.find_all("div", class_="selection-list__film")
    except:
        return None


def filmsHandler(list_films):
    all_ids = []
    all_values = []

    for film in list_films:
        all_ids.append(film.find("a", class_="selection-film-item-meta__link")["href"])
        all_values.append(film.find("span", class_="rating__value").text)

    return all_ids, all_values


def parsingFilm(len, ids, values):
    i = 0
    while i < len:
        delay()
        if values[i] == "—":
            i += 1
            continue

        link_film = "https://www.kinopoisk.ru" + ids[i]
        data_film = {
            "id": ids[i][6:-1],
            "type": "1",
            "title": None,
            "original_title": None,
            "year": None,
            "country": None,
            "director": None,
            "budget": None,
            "runtime": None,
            "world_gross": None,
            "genres": None,
            "age": None,
            "actors": None,
            "description": None,
            "image": None,
            "imageUrl": None,
            "rating": None,
            "count": None,
            "rating_imdb": None,
            "count_imdb": None
        }

        response_film = getResponseFilm(link_film)
        if response_film is None:
            print("Err: no internet connection.")
            continue

        soup_film = BeautifulSoup(response_film.text, "lxml")

        title = getTitleFilm(soup_film)
        if title is not None:
            data_film["title"] = title
        else:
            print("Err: the movie didn't load.")
            continue

        original_title = getOriginalTitleFilm(soup_film)
        if original_title is not None:
            data_film["original_title"] = original_title
        else:
            print("War: no original title.")

        encyclopedic_data = getEncyclopedicDataFilm(soup_film)
        if encyclopedic_data is not None:
            for key in encyclopedic_data.keys():
                if encyclopedic_data[key] is not None:
                    data_film[key] = encyclopedic_data[key]
        else:
            print("War: no encyclopedic.")

        if "сезон" in data_film["year"]:
            data_film["type"] = "0"

        actors = getActorsFilm(soup_film)
        if actors is not None:
            data_film["actors"] = actors
        else:
            print("War: no actors.")

        description = getDescriptionFilm(soup_film)
        if description is not None:
            data_film["description"] = description
        else:
            print("War: no description.")

        image, image_url = getImageFilm(soup_film, data_film["id"])
        if image is not None:
            data_film["image"] = image
            data_film["image_url"] = image_url
        else:
            print("War: no image or not found folder img-data.")

        rating, count = getRatingFilm(soup_film)
        if rating is not None:
            data_film["rating"] = rating
            data_film["count"] = count
        else:
            print("War: no rating.")

        rating_imdb, count_imdb = getRatingImdbFilm(soup_film)
        if rating_imdb is not None:
            data_film["rating_imdb"] = rating_imdb
            data_film["count_imdb"] = count_imdb
        else:
            print("War: no imdb rating.")

        print(data_film)
        i += 1


def getResponseFilm(link):
    try:
        return requests.get(link, headers={'User-Agent': UserAgent().chrome}, timeout=10)
    except:
        return None


def getTitleFilm(soup):
    try:
        return soup.find("h1", itemprop="name").find("span").text
    except:
        return None


def getOriginalTitleFilm(soup):
    try:
        spans = soup.find("h1", itemprop="name").parent.find("div").find_all("span")
        for span in spans:
            if "originalTitle" in span["class"][0]:
                return span.text
    except:
        return None


def getEncyclopedicDataFilm(soup):
    data = {
        "year": None,
        "country": None,
        "director": None,
        "budget": None,
        "runtime": None,
        "world_gross": None,
        "genres": None,
        "age": None,
    }
    try:
        encyclopedic = soup.find("div", attrs={"data-test-id": "encyclopedic-table"})
        data_tid_encyclopedic = encyclopedic.find("div")["data-tid"]
        all_rows_encyclopedic = encyclopedic.find_all(attrs={"data-tid": data_tid_encyclopedic})
    except:
        return None

    for row in all_rows_encyclopedic:
        infoRow = row.find_all("div")
        if infoRow[0].text == "Год производства":
            data["year"] = infoRow[1].text
        elif infoRow[0].text == "Страна":
            data["country"] = infoRow[1].text
        elif infoRow[0].text == "Режиссер":
            data["director"] = infoRow[1].text
        elif infoRow[0].text == "Бюджет":
            data["budget"] = infoRow[1].text.replace("\xa0", "")
        elif infoRow[0].text == "Время":
            data["runtime"] = infoRow[1].text
        elif infoRow[0].text == "Сборы в мире":
            data["world_gross"] = infoRow[1].text.replace("сборы", "").replace("\xa0", "")
        elif infoRow[0].text == "Жанр":
            data["genres"] = infoRow[1].text.replace("слова", "")
        elif infoRow[0].text == "Возраст":
            data["age"] = infoRow[1].text

    return data


def getActorsFilm(soup):
    try:
        actors = soup.find("div", class_="film-crew-block").find("div").find("ul").find_all("li")
    except:
        return None

    actors_list = ""
    for actor in actors:
        actors_list += actor.text + ", "
    return actors_list[:-2]


def getDescriptionFilm(soup):
    try:
        return soup.find("p", class_="styles_paragraph__2Otvx").text
    except:
        return None


def getImageFilm(soup, id):
    FOLDER = "img-data"
    try:
        image_url = "http:" + soup.find("img", class_="film-poster")["src"]
        image = requests.get(image_url, timeout=10)
        with open(FOLDER + "/" + id + ".jpg", 'bw') as f:
            f.write(image.content)
    except:
        return None, None

    return FOLDER + "/" + id + ".jpg", image_url


def getRatingFilm(soup):
    try:
        rating_stats = soup.find("div", class_="film-rating").find_all("span")
    except:
        return None, None

    return rating_stats[0].text, rating_stats[2].text


def getRatingImdbFilm(soup):
    try:
        rating_stats = soup.find("div", class_="film-sub-rating").find_all("span")
    except:
        return None, None

    return rating_stats[0].text.replace("IMDb: ", ""), rating_stats[1].text


if __name__ == "__main__":
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket

    parsingTable(1, 3)

