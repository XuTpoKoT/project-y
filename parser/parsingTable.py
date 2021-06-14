import time
import requests
import configparser
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def delay(sec):
    time.sleep(sec)


def parsingTable(page):
    config = configparser.ConfigParser()
    config.read("settings.ini")

    link_table = config["parsingTable"]["link"].replace('"', '').format(page)
    DELAY = int(config["main"]["delay"])
    TIMEOUT = int(config["main"]["timeout"])

    while True:
        delay(DELAY)

        response_table = getResponseTable(link_table, TIMEOUT)
        if response_table is None:
            print("\033[31mErr:\033[37m no internet connection.")
            continue

        soup_table = BeautifulSoup(response_table.text, "lxml")

        films = getFilms(soup_table)
        if films is None:
            print("\033[31mErr:\033[37m error in parsing the page.")
            continue

        len_films = len(films)
        if len_films == 0:
            print("\033[31mErr:\033[37m the page didn't load.")
            continue

        print(f"\033[32mInf:\033[37m on page {page} uploaded {len_films} films.")
        ids_films, values_films = filmsHandler(films)

        return len_films, ids_films, values_films


def getResponseTable(link, timeout):
    try:
        return requests.get(link, headers={'User-Agent': UserAgent().chrome}, timeout=timeout)
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
