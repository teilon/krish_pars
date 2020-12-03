from typing import List, Dict
import requests
from bs4 import BeautifulSoup

import json
import csv
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
params = [
    "Город",
    "Дом",
    "Площадь",
    "Количество уровней",
    "Санузел",
    "Состояние",
    "Покрытие крыши",
    "Участок",
    "Канализация",
    "Как огорожен участок",
    "Вода",
    "Электричество",
    "Отопление",
    "Газ",
    "Телефон",
    "Интернет",
    "Возможен обмен"
    ]

def start() -> None:
    req = requests.get(url, headers=headers)
    src = req.text

    with open("data/index.html", "w") as file:
        file.write(src)

def pages() -> int:
    with open("data/index.html") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, "lxml")
    pages_hrefs = soup.find("nav", class_="paginator").find_all(class_="paginator__btn")
    count = pages_hrefs[-2].text.strip()

    return int(count)

def pars_pages(pages_count: int) -> None:
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
        
        pars_ads(page)

def pars_ads(page: int) -> None:
    with open(f"data/{page}.json") as file:
        urls = json.load(file)
    
    num = 0
    for url in urls:
        req = requests.get(url, headers=headers)
        src = req.text

        with open(f"data/{page}_{num}.html", "w") as file:
            file.write(src)
        
        ad = pars_ad(page, num)
        print_ad(ad)
        num += 1
        
        sleep(randrange(2, 4))

def pars_ad(page: int, num: int) -> Dict:
    with open(f"data/{page}_{num}.html") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, "lxml")
    ad = {
        "Город":"",
        "Дом":"",
        "Площадь":"",
        "Количество уровней":"",
        "Санузел":"",
        "Состояние":"",
        "Покрытие крыши":"",
        "Участок":"",
        "Канализация":"",
        "Как огорожен участок":"",
        "Вода":"",
        "Электричество":"",
        "Отопление":"",
        "Газ":"",
        "Телефон":"",
        "Интернет":"",
        "Возможен обмен":""
        }

    items = soup.find_all(class_="offer__info-item")
    for item in items:
        param = item.find(class_="offer__info-title").text.strip()
        if param in params:
            if item.find(class_="offer__location"):
                info = item.find(class_="offer__location").find("span").text.strip()
                ad[param] = info
                continue
            info = item.find(class_="offer__advert-short-info").text.strip()
            ad[param] = info
    
    dls = soup.find(class_="offer__parameters").find_all("dl")
    for dl in dls:
        param = dl.find("dt").text.strip()
        if param in params:
            info = dl.find("dd").text.strip()
            ad[param] = info
    
    return ad

def print_ad(ad: Dict) -> None:
    with open(f"data/result.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                ad["Город"],
                ad["Дом"],
                ad["Площадь"],
                ad["Количество уровней"],
                ad["Санузел"],
                ad["Состояние"],
                ad["Покрытие крыши"],
                ad["Участок"],
                ad["Канализация"],
                ad["Как огорожен участок"],
                ad["Вода"],
                ad["Электричество"],
                ad["Отопление"],
                ad["Газ"],
                ad["Телефон"],
                ad["Интернет"],
                ad["Возможен обмен"],
            )
        )

def print_title() -> None:
    with open(f"data/result.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Город",
                "Дом",
                "Площадь",
                "Количество уровней",
                "Санузел",
                "Состояние",
                "Покрытие крыши",
                "Участок",
                "Канализация",
                "Как огорожен участок",
                "Вода",
                "Электричество",
                "Отопление",
                "Газ",
                "Телефон",
                "Интернет",
                "Возможен обмен"
            )
        )


def main():
    start()
    pages_count = pages()
    print_title()
    pars_pages(pages_count)

if __name__ == '__main__':
    main()