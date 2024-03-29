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
        response = session.get("https://funpay.com/orders/trade")
        if response.status_code == 302:
            showerror(
                title="Error",
                message=str(ex)
                + "\n\nProbably cookies are old. Try pressing Login button and login into your FP account again.",
            )
        html = session.get("https://funpay.com/orders/").text
        html_objects = BeautifulSoup(html, "lxml")
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
    html_objects = BeautifulSoup(html, "lxml")
    servers = [
        {server.text.strip(): int(server["value"])}
        for server in html_objects.find(
            "select", class_="form-control showcase-filter-input"
        ).find_all("option")
        if server.text.strip().lower() != "сервер"
    ]
    return servers


@essentials_check
def get_prices() -> dict:
    cwd = os.getcwd()

    with open(os.path.join(cwd, "config.json"), "r") as json_file:
        config = json.load(json_file)
    minimal_amount = config.get("gold_damp_threshold")
    session = requests.Session()
    session.headers = {"User-Agent": UserAgent().random}
    session.cookies.update(cookies_worker.read_cookies())
    html = session.get("https://funpay.com/chips/2/").text
    only_online = SoupStrainer(attrs={"data-online": "1"})
    html_objects = BeautifulSoup(html, "lxml", parse_only=only_online)
    items = html_objects.find_all("a")
    data = dict()
    for server in get_servers():
        data[list(server.keys())[0], "Альянс"] = list()
        data[list(server.keys())[0], "Орда"] = list()
    with open(os.path.join(os.getcwd(), "config.json")) as f:
        username = json.load(f).get("username")
    for item in items:
        if item.find("div", "media-user-name").text.strip() == username:
            continue
        server = item.find("div", {"class": "tc-server hidden-xxs"}).text.strip()
        side = item.find("div", {"class": "tc-side hidden-xxs"}).text.strip()
        price = item.find("div", {"class": "tc-price"}).text.strip()
        if (
            int(item.find("div", {"class": "tc-amount"}).text.strip().replace(" ", ""))
            < minimal_amount
            and minimal_amount is not None
        ):
            continue
        if (server, side) not in list(data.keys()):
            data[(server, side)] = list()
        data[(server, side)].append(float(price.split()[0].strip()))
    any_servers_prices_dire = data.pop(("Любой", "Орда"), None)
    any_servers_prices_aliance = data.pop(("Любой", "Альянс"), None)
    any_servers_prices = data.pop(("Любой", "Любая"), None)
    for key in list(data.keys()):
        data[key].extend(any_servers_prices)
        if key[1] == "Орда":
            data[key].extend(any_servers_prices_dire)
        if key[1] == "Альянс":
            data[key].extend(any_servers_prices_aliance)
    return data


# print(get_prices()["Aggramar", "Альянс"])
# print(get_servers())
# data = list(get_prices().keys())
# data.sort(key=lambda x: x[0])
# print(data)


@essentials_check
def get_gold_amount() -> dict:
    session = requests.Session()
    session.headers = {"User-Agent": UserAgent().random}
    cookies = cookies_worker.read_cookies()
    session.cookies.update(cookies)
    phpsessid = session.get("https://funpay.com/chips/saveOffers").cookies.get(
        "PHPSESSID"
    )
    cookies.update({"PHPSESSID": phpsessid})
    session.cookies.update(cookies)
    cwd = os.getcwd()
    with open(os.path.join(cwd, "config.json"), "r") as json_file:
        config = json.load(json_file)
    html = session.get(
        config.get("trades_page_url", "https://funpay.com/chips/2/trade")
    ).text
    html_objects = BeautifulSoup(html, "lxml")
    gold_amounts = dict()
    n_servers = 43
    entries = html_objects.find_all("input", attrs={"class": "form-control amount"})
    for entry in entries:
        gold_amounts[entry["name"].strip()] = entry["value"].strip()
    return gold_amounts


@essentials_check
def get_username() -> str:
    session = requests.Session()
    session.headers = {"User-Agent": UserAgent().random}
    session.cookies.update(cookies_worker.read_cookies())
    cwd = os.getcwd()
    with open(os.path.join(cwd, "config.json"), "r") as json_file:
        config = json.load(json_file)
    html = session.get(
        config.get("trades_page_url", "https://funpay.com/chips/2/trade")
    ).text
    html_objects = BeautifulSoup(html, "lxml")

    return html_objects.find("div", {"class": "user-link-name"}).text


@essentials_check
def check_connection() -> bool:
    pass
