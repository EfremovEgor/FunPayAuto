from bs4 import BeautifulSoup
import requests
import cookies_worker
from fake_useragent import UserAgent
import json
import os
from fp_exceptions import (
    AuthenticationError,
    SiteDoesNotResponseError,
    CookiesFileNotFoundError,
    ConfigNotFoundError,
)


def essentials_check(func):
    def wrapper():
        cwd = os.getcwd()
        if not os.path.exists(os.path.join(cwd, "config.json")):
            raise ConfigNotFoundError(os.path.join(cwd, "config.json"))
        with open(os.path.join(cwd, "config.json"), "r") as json_file:
            config = json.load(json_file)
        cookies_path = config.get(
            "cookies_path", os.path.join(cwd, "data", "cookies.json")
        )
        if not os.path.exists(cookies_path):
            raise CookiesFileNotFoundError(cookies_path)
        session = requests.Session()
        session.cookies.update(cookies_worker.read_cookies())
        html = session.get("https://funpay.com/orders/").text
        html_objects = BeautifulSoup(html, "html.parser")
        title = html_objects.find("title").text.strip().lower()
        if title is None or any(
            item in html_objects.find("title").text.strip().lower()
            for item in ["войти", "log in"]
        ):
            raise AuthenticationError()
        return func()

    return wrapper


def generate_random_useragent():
    return UserAgent().random


@essentials_check
def get_servers() -> list:
    session = requests.Session()
    session.headers = {"User-Agent": generate_random_useragent()}
    cwd = os.getcwd()
    with open(os.path.join(cwd, "config.json"), "r") as json_file:
        config = json.load(json_file)
    html = session.get(config.get("goods_page_url", "https://funpay.com/chips/2/")).text
    html_objects = BeautifulSoup(html, "html.parser")
    servers = [
        server.text.strip()
        for server in html_objects.find(
            "select", class_="form-control showcase-filter-input"
        ).find_all("option")
        if server.text.strip().lower() != "сервер"
    ]

    return servers


@essentials_check
def check_connection() -> bool:
    pass
    session = requests.Session()
    session.headers = {"User-Agent": generate_random_useragent()}
    cwd = os.getcwd()
    with open(os.path.join(cwd, "config.json"), "r") as json_file:
        config = json.load(json_file)
    response = session.get(config.get("base_site_url", "https://funpay.com"))
    if response.status_code != 200:
        raise SiteDoesNotResponseError(response.status_code)
    cookies_path = config.get("cookies_path", os.path.join(cwd, "data", "cookies.json"))
    session.cookies.update(cookies_worker.read_cookies(cookies_path))
    html = session.get("https://funpay.com/orders/").text
    html_objects = BeautifulSoup(html, "html.parser")
    title = html_objects.find("title").text.strip().lower()
    if title is None or any(
        item in html_objects.find("title").text.strip().lower()
        for item in ["войти", "log in"]
    ):
        raise AuthenticationError()
