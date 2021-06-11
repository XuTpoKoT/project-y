import socks
import socket
import configparser
from parsingTable import parsingTable
from parsingFilm import parsingFilm

if __name__ == "__main__":
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket

    config = configparser.ConfigParser()
    config.read("settings.ini")

    START = int(config["main"]["start"])
    END = int(config["main"]["end"])

    for i in range(START, END):
        len_films, ids_films, values_films = parsingTable(i)

        for j in range(len_films):
            if values_films[j] != "-":
                data = parsingFilm(ids_films[j])

                print(data)
