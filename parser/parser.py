import socks
import socket
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

FOLDER = "img-data"  # название папки для изображений
PAGE_RANGE = [1, 50]  # [начальная страница, конечная страница],

if __name__ == "__main__":
    # подключаем прокси тора
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket

    i = PAGE_RANGE[0]
    # цикл для страниц
    while i <= PAGE_RANGE[1]:
        time_main = time.time()

        link_table = f"https://www.kinopoisk.ru/lists/navigator/?page={i}&sort=popularity&tab=all"
        try:
            response_table = requests.get(link_table, headers={'User-Agent': UserAgent().chrome}, timeout=10)
        except:
            print("Err: нет интернета")

        soup_table = BeautifulSoup(response_table.text, "lxml")

        try:
            # Ищем на странице все фильмы
            all_films = soup_table.find_all("div", class_="selection-list__film")
            # Если на странице нет фильмов, то загружаем ее заново
            if len(all_films) == 0:
                print("Err: страница не загрузилась.")
                continue
            print(f"on page {i} uploaded {len(all_films)} films.")

            # Собираем id и оценку каждого фильма, id нужен для получения ссылки на фильм
            all_ids = []
            all_values = []
            for film in all_films:
                all_ids.append(film.find("a", class_="selection-film-item-meta__link")["href"])
                all_values.append(film.find("span", class_="rating__value").text)

            # Цикл для каждого фильма
            j = 0
            while j < len(all_ids):
                # Если у фильма нет оценки, то мы не заносим его в БД
                if all_values[j] != "—":
                    link_film = "https://www.kinopoisk.ru" + all_ids[j]
                    data_film = {
                        "id": all_ids[j][6:-1],
                        "type": "1",
                        "title": "—",
                        "original_title": "—",
                        "year": "—",
                        "country": "—",
                        "director": "—",
                        "budget": "—",
                        "runtime": "—",
                        "world_gross": "—",
                        "genres": "—",
                        "age": "—",
                        "actors": "—",
                        "description": "—",
                        "image": "—",
                        "image_url": "—",
                        "rating": "—",
                        "count": "—",
                        "rating_imdb": "—",
                        "count_imdb": "—"
                    }

                    response_film = requests.get(link_film, headers={'User-Agent': UserAgent().chrome}, timeout=10)
                    soup_film = BeautifulSoup(response_film.text, "lxml")
                    try:
                        # Название фильма
                        data_film["title"] = soup_film.find("h1", itemprop="name").find("span").text

                        # Original title
                        try:
                            spans = soup_film.find("h1", itemprop="name").parent.find("div").find_all("span")
                            for span in spans:
                                if "originalTitle" in span["class"][0]:
                                    data_film["original_title"] = span.text
                        except:
                            print("War: нет original title")

                        # Информация из поля "О фильме"
                        encyclopedic = soup_film.find("div", attrs={"data-test-id": "encyclopedic-table"})
                        data_tid_encyclopedic = encyclopedic.find("div")["data-tid"]
                        all_rows_encyclopedic = encyclopedic.find_all(attrs={"data-tid": data_tid_encyclopedic})
                        for row in all_rows_encyclopedic:
                            info_row = row.find_all("div")
                            if info_row[0].text == "Год производства":
                                data_film["year"] = info_row[1].text
                            elif info_row[0].text == "Страна":
                                data_film["country"] = info_row[1].text
                            elif info_row[0].text == "Режиссер":
                                data_film["director"] = info_row[1].text
                            elif info_row[0].text == "Бюджет":
                                data_film["budget"] = info_row[1].text.replace("\xa0", "")
                            elif info_row[0].text == "Время":
                                data_film["runtime"] = info_row[1].text
                            elif info_row[0].text == "Сборы в мире":
                                data_film["world_gross"] = info_row[1].text.replace("сборы", "").replace("\xa0", "")
                            elif info_row[0].text == "Жанр":
                                data_film["genres"] = info_row[1].text.replace("слова", "")
                            elif info_row[0].text == "Возраст":
                                data_film["age"] = info_row[1].text

                        # Тип
                        if "сезон" in data_film["year"]:
                            data_film["type"] = "0"

                        # Актеры
                        try:
                            actors = soup_film.find("div", class_="film-crew-block").find("div").find("ul").find_all("li")
                            actors_list = ""
                            for actor in actors:
                                actors_list += actor.text + ", "
                            data_film["actors"] = actors_list[:-2]
                        except:
                            print("War: нет актеров")

                        # О фильме
                        try:
                            data_film["description"] = soup_film.find("p", class_="styles_paragraph__2Otvx").text
                        except:
                            print("War: нет информации о фильме.")

                        # Постер фильма
                        try:
                            image_url = "http:" + soup_film.find("img", class_="film-poster")["src"]
                            image = requests.get(image_url, timeout=10)
                            with open(FOLDER + "/" + all_ids[j][6:-1] + ".jpg", 'bw') as f:
                                f.write(image.content)
                            data_film["image"] = FOLDER + "/" + all_ids[j][6:-1] + ".jpg"
                            data_film["image_url"] = image_url
                        except:
                            print("War: нет постера к фильму.")

                        # Оценка фильма
                        try:
                            rating_stats = soup_film.find("div", class_="film-rating").find_all("span")
                            data_film["rating"] = rating_stats[0].text
                            data_film["count"] = rating_stats[2].text
                        except:
                            print("War: Нет оценки")

                        # Оценка фильма imdb
                        try:
                            rating_imdb_stats = soup_film.find("div", class_="film-sub-rating").find_all("span")
                            data_film["rating_imdb"] = rating_imdb_stats[0].text.replace("IMDb: ", "")
                            data_film["count_imdb"] = rating_imdb_stats[1].text
                        except:
                            print("War: нет оценки imdb")

                        '''
                        !!!
                        Здесь место для заполнения БД.
                        !!!
                        '''

                        print(i, j+1, data_film["title"], "добавлен в БД.")
                        j += 1
                    except:
                        print("Err: ошибка в парсинге фильма.")
                    time.sleep(2)
            i += 1
        except:
            print("Err: ошибка в парсинге страницы.")
        print(f"Total time for {i - 1} page: {round(time.time() - time_main, 2)} sec")
        time.sleep(2)
