import requests
import json
from random import randint

from bs4 import BeautifulSoup


def parse_image(req) -> list:
    response = requests.get('https://yandex.ru/images/search', params={"text": req})
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find('div', {"class": "serp-list"})

    image_link_list = []

    try:
        items = items.find_all("div", {"class": "serp-item"})
    except AttributeError:
        return image_link_list

    for item in items:
        image_link = json.loads(item.get("data-bem"))['serp-item']['img_href']
        image_link_list.append(image_link)

    return image_link_list[randint(0, len(image_link_list) - 1)]


if __name__ == '__main__':
    pass
