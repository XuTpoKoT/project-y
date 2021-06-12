def count2int(count):
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

def str2text(s):
    """
    Приводит строку к TEXT

    Если строка равна "—", то вернется None, иначе исходная строка
    """
    return None if s == "—" else s

    
def convert_film_info(data_film):
    """
    Преобразует данные из парсера в данные для записи в базу  
    """

    film_info = []

    temp = 0 if data_film["type"] == "фильм" else 1
    film_info.append(temp)

    temp = (data_film["title"])
    film_info.append(temp)

    temp = str2text(data_film["original_title"])
    film_info.append(temp)

    try:
        temp = int(data_film["year"])
    except:
        temp = None

    film_info.append(temp)

    temp = str2text(data_film["country"])
    film_info.append(temp)

    temp = str2text(data_film["budget"])
    film_info.append(temp)

    temp = runtime2int(data_film["runtime"])
    film_info.append(temp)

    temp = data_film["world_gross"].split("=")[1].strip()
    film_info.append(temp)

    temp = str2text(data_film["age"])
    film_info.append(temp)

    temp = str2text(data_film["description"])
    film_info.append(temp)

    return tuple(film_info)
