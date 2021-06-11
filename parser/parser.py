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
        responseTable = getResponseTable(page)
        if responseTable is None:
            print("Err: no internet connection.")
            continue

        soupTable = BeautifulSoup(responseTable.text, "lxml")

        films = getFilms(soupTable)
        if films is None:
            print("Err: error in parsing the page.")
            continue

        lenFilms = len(films)
        if lenFilms == 0:
            print("Err: the page didn't load.")
            continue

        print(f"on page {page} uploaded {lenFilms} films.")
        idsFilms, valuesFilms = filmsHandler(films)
        parsingFilm(lenFilms, idsFilms, valuesFilms)

        page += 1


def getResponseTable(currentPage):
    linkTable = f"https://www.kinopoisk.ru/lists/navigator/?page={currentPage}&sort=popularity&tab=all"

    try:
        return requests.get(linkTable, headers={'User-Agent': UserAgent().chrome}, timeout=10)
    except:
        return None


def getFilms(soup):
    try:
        return soup.find_all("div", class_="selection-list__film")
    except:
        return None


def filmsHandler(listFilms):
    allIds = []
    allValues = []

    for film in listFilms:
        allIds.append(film.find("a", class_="selection-film-item-meta__link")["href"])
        allValues.append(film.find("span", class_="rating__value").text)

    return allIds, allValues


def parsingFilm(len, ids, values):
    i = 0
    while i < len:
        delay()
        if values[i] == "—":
            i += 1
            continue

        linkFilm = "https://www.kinopoisk.ru" + ids[i]
        dataFilm = {
            "id": ids[i][6:-1],
            "type": "1",
            "title": None,
            "originalTitle": None,
            "year": None,
            "country": None,
            "director": None,
            "budget": None,
            "runtime": None,
            "worldGross": None,
            "genres": None,
            "age": None,
            "actors": None,
            "description": None,
            "image": None,
            "imageUrl": None,
            "rating": None,
            "count": None,
            "ratingImdb": None,
            "countImdb": None
        }

        responseFilm = getResponseFilm(linkFilm)
        if responseFilm is None:
            print("Err: no internet connection.")
            continue

        soupFilm = BeautifulSoup(responseFilm.text, "lxml")

        title = getTitleFilm(soupFilm)
        if title is not None:
            dataFilm["title"] = title
        else:
            print("Err: the movie didn't load.")
            continue

        originalTitle = getOriginalTitleFilm(soupFilm)
        if originalTitle is not None:
            dataFilm["originalTitle"] = originalTitle
        else:
            print("War: no original title.")

        encyclopedicData = getEncyclopedicDataFilm(soupFilm)
        if encyclopedicData is not None:
            for key in encyclopedicData.keys():
                if encyclopedicData[key] is not None:
                    dataFilm[key] = encyclopedicData[key]
        else:
            print("War: no encyclopedic.")

        if "сезон" in dataFilm["year"]:
            dataFilm["type"] = "0"

        actors = getActorsFilm(soupFilm)
        if actors is not None:
            dataFilm["actors"] = actors
        else:
            print("War: no actors.")

        description = getDescriptionFilm(soupFilm)
        if description is not None:
            dataFilm["description"] = description
        else:
            print("War: no description.")

        image, imageUrl = getImageFilm(soupFilm, dataFilm["id"])
        if image is not None:
            dataFilm["image"] = image
            dataFilm["imageUrl"] = imageUrl
        else:
            print("War: no image or not found folder img-data.")

        rating, count = getRatingFilm(soupFilm)
        if rating is not None:
            dataFilm["rating"] = rating
            dataFilm["count"] = count
        else:
            print("War: no rating.")

        ratingImdb, countImdb = getRatingImdbFilm(soupFilm)
        if ratingImdb is not None:
            dataFilm["ratingImdb"] = ratingImdb
            dataFilm["countImdb"] = countImdb
        else:
            print("War: no imdb rating.")

        print(dataFilm)
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
        "worldGross": None,
        "genres": None,
        "age": None,
    }
    try:
        encyclopedic = soup.find("div", attrs={"data-test-id": "encyclopedic-table"})
        dataTidEncyclopedic = encyclopedic.find("div")["data-tid"]
        allRowsEncyclopedic = encyclopedic.find_all(attrs={"data-tid": dataTidEncyclopedic})
    except:
        return None

    for row in allRowsEncyclopedic:
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
            data["worldGross"] = infoRow[1].text.replace("сборы", "").replace("\xa0", "")
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
        ratingStats = soup.find("div", class_="film-rating").find_all("span")
    except:
        return None, None

    return ratingStats[0].text, ratingStats[2].text


def getRatingImdbFilm(soup):
    try:
        ratingStats = soup.find("div", class_="film-sub-rating").find_all("span")
    except:
        return None, None

    return ratingStats[0].text.replace("IMDb: ", ""), ratingStats[1].text


if __name__ == "__main__":
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket

    parsingTable(1, 3)

