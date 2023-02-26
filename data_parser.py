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
from tkinter.messagebox import showerror, showwarning, showinfo
from bs4 import SoupStrainer


def essentials_check(func):
    def wrapper():
        cwd = os.getcwd()
        if not os.path.exists(os.path.join(cwd, "config.json")):
            ex = ConfigNotFoundError(os.path.join(cwd, "config.json"))
            showerror(title="Error", message=str(ex))
            raise ex

        with open(os.path.join(cwd, "config.json"), "r") as json_file:
            config = json.load(json_file)
        cookies_path = config.get(
            "cookies_path", os.path.join(cwd, "data", "cookies.json")
        )
        if not os.path.exists(cookies_path):
            ex = CookiesFileNotFoundError(cookies_path)
            showerror(
                title="Error",
                message=str(ex)
                + "\n\nTry pressing Login button and login into your FP account.",
            )
            raise ex
        session = requests.Session()
        try:
            response = session.get(config.get("base_site_url", "https://funp1ay.com/"))
        except requests.exceptions.ConnectionError as ex:
            ex = SiteDoesNotResponseError()
            showerror(
                title="Error",
                message=str(ex)
                + "\n\nMight be a problem with the site or error in url. Try checking URL.",
            )
            raise ex
            return
        if response.status_code != 200:
            ex = SiteDoesNotResponseError(response.status_code)
            showerror(
                title="Error",
                message=str(ex)
                + "\n\nMight be a problem with the site or error in url. Try checking URL.",
            )
            raise ex
        session.cookies.update(cookies_worker.read_cookies())
        html = session.get("https://funpay.com/orders/").text
        html_objects = BeautifulSoup(html, "html.parser")
        title = html_objects.find("title").text.strip().lower()
        if title is None or any(
            item in html_objects.find("title").text.strip().lower()
            for item in ["войти", "log in"]
        ):
            ex = AuthenticationError()
            showerror(
                title="Error",
                message=str(ex)
                + "\n\nProbably cookies are old. Try pressing Login button and login into your FP account again.",
            )
            raise ex
        return func()

    return wrapper


def generate_random_useragent() -> str:
    return UserAgent().random


@essentials_check
def get_servers() -> list[dict]:
    session = requests.Session()
    session.headers = {"User-Agent": generate_random_useragent()}
    cwd = os.getcwd()
    with open(os.path.join(cwd, "config.json"), "r") as json_file:
        config = json.load(json_file)
    html = session.get(config.get("goods_page_url", "https://funpay.com/chips/2/")).text
    html_objects = BeautifulSoup(html, "html.parser")
    servers = [
        {server.text.strip(): int(server["value"])}
        for server in html_objects.find(
            "select", class_="form-control showcase-filter-input"
        ).find_all("option")
        if server.text.strip().lower() != "сервер"
    ]
    return servers[:20]


@essentials_check
def get_prices() -> dict:
    session = requests.Session()
    session.headers = {"User-Agent": UserAgent().random}
    session.cookies.update(cookies_worker.read_cookies())
    html = session.get("https://funpay.com/chips/2/").text
    only_online = SoupStrainer(attrs={"data-online": "1"})
    html_objects = BeautifulSoup(html, "lxml", parse_only=only_online)
    items = html_objects.find_all("a")
    data = dict()
    for item in items:
        server = item.find("div", {"class": "tc-server hidden-xxs"}).text.strip()
        side = item.find("div", {"class": "tc-side hidden-xxs"}).text.strip()
        price = item.find("div", {"class": "tc-price"}).text.strip()
        if (server, side) not in list(data.keys()):
            data[(server, side)] = list()
        data[(server, side)].append(float(price.split()[0].strip()))
    return data


@essentials_check
def get_gold_amount() -> dict:
    session = requests.Session()
    session.headers = {"User-Agent": UserAgent().random}
    session.cookies.update(cookies_worker.read_cookies())
    cwd = os.getcwd()
    with open(os.path.join(cwd, "config.json"), "r") as json_file:
        config = json.load(json_file)
    html = session.get(
        config.get("trades_page_url", "https://funpay.com/chips/2/trade")
    ).text
    html_objects = BeautifulSoup(html, "html.parser")
    gold_amounts = dict()
    n_servers = 43
    entries = html_objects.find_all("input", attrs={"class": "form-control amount"})[
        :n_servers
    ]
    for entry in entries:
        gold_amounts[entry["name"].strip()] = entry["value"].strip()
    return gold_amounts


@essentials_check
def check_connection() -> bool:
    pass
