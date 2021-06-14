import socks
import socket
import configparser
from parsingTable import parsingTable
from parsingFilm import parsingFilm

import sys
sys.path.insert(0, "../films_db")
import films_db

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("settings.ini")
    
    START = int(config["main"]["start"])
    END = int(config["main"]["end"])
    PORT = int(config["main"]["port"])

    socks.set_default_proxy(socks.SOCKS5, "localhost", PORT)
    socket.socket = socks.socksocket
    
    films_db.init()

    for i in range(START, END):
        len_films, ids_films, values_films = parsingTable(i)

        for j in range(len_films):
            if values_films[j] != "-":
                data = parsingFilm(ids_films[j])

                print(data)
                films_db.insert_film(data)
