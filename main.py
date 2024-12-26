import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def shorten_link(token, url):
    method_url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "access_token": token,
        "url": url,
        "v": "5.199"
    }
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    response_data = response.json()
    return response_data["response"]["short_url"]


def get_count_clicks(token, url):
    method_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "key": urlparse(url).path[1:],
        "v": "5.199",
        "interval": "forever"
    }
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    response_data = response.json()
    return response_data["response"]["stats"][0]["views"]


def is_shorten_link(token, url):
    if urlparse(url).netloc == "vk.cc":
        method_url = "https://api.vk.com/method/utils.getLinkStats"
        params = {
            "access_token": token,
            "key": urlparse(url).path[1:],
            "v": "5.199",
            "interval": "forever"
        }
        response = requests.get(method_url, params=params)
        response.raise_for_status()
        response_data = response.json()
        return "response" in response_data and response_data["response"]
    return False


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    parser = argparse.ArgumentParser(description='Сокращение URL и получение статистики кликов.')
    parser.add_argument('url', type=str, help='URL для сокращения или статистики кликов.')
    args = parser.parse_args()
    url = args.url
    if is_shorten_link(vk_token, url):
        try:
            count_clicks = get_count_clicks(vk_token, url)
        except requests.exceptions.HTTPError as http_err:
            print(f"Произошла ошибка HTTP: {http_err}")
        except KeyError:
            print(f"Ответ не содержит ожидаемых данных.")
        else:
            print(count_clicks)
    else:
        try:
            short_url = shorten_link(vk_token, url)
        except requests.exceptions.HTTPError as http_err:
            print(f"Произошла ошибка HTTP: {http_err}")
        except KeyError:
            print(f"Ответ не содержит ожидаемых данных.")
        else:
            print(short_url)