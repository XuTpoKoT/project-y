1. установить библиотеки для питона:
requests
fake_useragent
bs4
PySocks

2. установить браузер Tor

3. в файле "torrc" добавить 3 следующих строки:
'''
CircuitBuildTimeout 10
LearnCircuitBuildTimeout 0
MaxCircuitDirtiness 10
'''

4. запустить браузер Tor

5. в файле parser.py в 9 строке вписать границы парсинга

6. проверить, чтобы в папке с parser_v2.py была папка "img-data", если ее нет - создать.

7. запустить!