import requests
from bs4 import BeautifulSoup

import json
from time import sleep
from random import randrange

url = "https://krisha.kz/prodazha/doma/almaty/?areas=&das[cmtn.heating]=2&das[land.square][from]=6&das[land.square][to]=10&das[price][from]=15000000&das[price][to]=25000000"

# https://krisha.kz/prodazha/doma/almaty/?
# areas=&das[cmtn.heating]=2&
# das[land.square][from]=6&
# das[land.square][to]=10&
# das[price][from]=15000000&das[price][to]=25000000&
# page=2

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0",
}
host = "https://krisha.kz"

def start():
    req = requests.get(url, headers=headers)
    src = req.text

    with open("data/index.html", "w") as file:
        file.write(src)

def pages():
    with open("data/index.html") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, "lxml")
    pages_hrefs = soup.find("nav", class_="paginator").find_all(class_="paginator__btn")
    count = pages_hrefs[-2].text.strip()

    return int(count)

def pars_pages(pages_count: int):
    if not pages_count:
        print(f"NOT PAGES {pages_count}")
        return {"message": "NOT PAGES"}        
    
    ads_list = []
    for page in range(1, pages_count + 1):
        page_href = f"{url}&page={page}"
        
        req = requests.get(url, headers=headers)
        src = req.text

        with open(f"data/{page}.html", "w") as file:
            file.write(src)
        
        with open(f"data/{page}.html") as file:
            src = file.read()
        
        soup = BeautifulSoup(src, "lxml")
        card_hrefs = soup.find_all(class_="a-card__title")

        card_list = []
        for item in card_hrefs:
            card_list.append(f"{host}{item.get('href')}")
        ads_list.extend(card_list)
        
        with open(f"data/{page}.json", "w") as file:
            json.dump(card_list, file, indent=4, ensure_ascii=False)
        
        sleep(randrange(2, 4))


def main():
    start()
    pages_count = pages()
    pars_pages(pages_count)


if __name__ == '__main__':
    main()