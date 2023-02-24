import requests
import json
from bs4 import BeautifulSoup
import cookies_worker
from fake_useragent import UserAgent
import os


def get_necessary_values() -> dict:
    session = requests.Session()
    session.headers = {"User-Agent": UserAgent().random}
    session.cookies.update(cookies_worker.read_cookies())
    html = session.get("https://funpay.com/chips/2/trade").text
    html_objects = BeautifulSoup(html, "html.parser")
    price_objects = html_objects.find_all("input", {"class": "form-control price"})
    amount_objects = html_objects.find_all("input", {"class": "form-control amount"})
    necessary_values = dict()
    for amount, price in list(zip(amount_objects, price_objects)):
        necessary_values[amount["name"]] = amount["value"]
        necessary_values[price["name"]] = price["value"]
    min_sum = html_objects.find("input", {"name": "options[chip_min_sum]"})
    necessary_values[min_sum["name"]] = min_sum["value"]
    return necessary_values


def form_payload(data: dict = None) -> dict:
    path = os.path.join(os.getcwd(), "data", "request_template.json")
    with open(path, "r") as f:
        payload = json.load(f)
    payload.update(get_necessary_values())
    if data is not None:
        payload.update(data)
    return payload


def send_request(payload: dict) -> int:
    session = requests.Session()
    session.headers = {"User-Agent": UserAgent().random}
    session.cookies.update(cookies_worker.read_cookies())
    html = session.get("https://funpay.com/chips/2/trade").text
    html_objects = BeautifulSoup(html, "html.parser")
    payload["csrf_token"] = json.loads(html_objects.find("body")["data-app-data"])[
        "csrf-token"
    ]
    response = session.post("https://funpay.com/chips/saveOffers", data=payload)
    return response.status_code
