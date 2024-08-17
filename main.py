import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Введите url')
    args = parser.parse_args()
    return args.url


def shorten_link(token, url):
    url_metod = "https://api.vk.ru/method/utils.getShortLink"
    params = {"access_token": token, "v": "5.199", "url": url}
    response = requests.get(url_metod, params=params)
    response.raise_for_status()
    short_link = response.json()['response']['short_url']
    return short_link


def is_shorten_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "vk.cc"


def count_clicks(token, url):
    url_metod = "https://api.vk.ru/method/utils.getLinkStats"
    parsed_url = urlparse(url)
    key = parsed_url.path.replace("/", "")
    params = {
        "access_token": token,
        "v": "5.199",
        "key": key,
        "interval": "forever"
    }
    response = requests.get(url_metod, params=params)
    response.raise_for_status()
    count_click = response.json()['response']['stats'][0]['views']
    return count_click


def main():
    token = os.getenv("VK_TOKEN")
    url = create_parser()
    try:
        if is_shorten_link(url):
            print("Кол-во кликов:", count_clicks(token, url))
        else:
            print("Сокращенная ссылка:", shorten_link(token, url))
    except requests.exceptions.HTTPError:
        print("Ошибка ввода")


if __name__ == "__main__":
    main()
