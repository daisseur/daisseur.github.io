import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

def shorten(url):
    return requests.get(f'https://is.gd/create.php?format=simple&url={url}').text

def replace_number(text):
    dict_number = {
        "1": "un",
        "2": "deux",
        "3": "trois",
        "4": "quatre",
        "5": "cinq",
        "6": "six",
        "7": "sept",
        "8": "huit",
        "9": "neuf",
        "10": "dix"
    }
    for key, value in dict_number.items():
        text = text.replace(key, value + " ")
    return text

def remove_(text):
    return text.replace("'", '')

class LibrairyOfBabel:
    def __init__(self, search, mode, replace_number=False):
        self.search = search
        self.mode = mode
        self.replace_number = replace_number
        self.dict_mode = {"alone": 0, "random": 1, "english": 2, "title": 3}

    def getbook(self, hexagon, wall, shelf, volume, page):
        return f"https://libraryofbabel.info/book.cgi?{hexagon}-w{wall}-s{shelf}-v{volume}:{page}"

    def research(self):

        url = "https://libraryofbabel.info/search.cgi"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
        if self.replace_number:
            body = f"find={unidecode(replace_number(self.search))}&method=x".encode("utf-8")
        else:
            body = f"find={unidecode(self.search)}&method=x".encode("utf-8")

        results = []

        response = requests.post(url,
                                 headers=headers,
                                 data=body)

        soup = BeautifulSoup(response.text, "html.parser")
        for location in soup.find_all(attrs={"class": "location"}):
            results.append(location.a["onclick"])
        books = []
        result = [i.replace("postform(", '').replace(")", '') for i in results]
        for i in result:
            args = [remove_(e) for e in i.split(",")]
            args[0] = args[0].replace("\n", "")
            if len(args) > 6:
                args = args[:5]
            books.append(self.getbook(*args))
        return books[self.dict_mode[self.mode]]

if __name__ == "__main__":
    search = input("Rechercher un texte dans la bibliothèque (jusqu'à 3200 caractères)\n>>> ")
    if search == '':
        search = "Wow incroyable Non"
    lob = LibrairyOfBabel(search, "title")
    url = lob.research()
    print(shorten(url))