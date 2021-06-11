import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def delay():
    time.sleep(2)


def parsingTable(page):
    while True:
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

        return len_films, ids_films, values_films


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
