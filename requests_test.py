import requests
import cookies_worker
import json
from bs4 import BeautifulSoup
import cookies_worker
from fake_useragent import UserAgent

session = requests.Session()
session.headers = {"User-Agent": UserAgent().random}
session.cookies.update(cookies_worker.read_cookies())
html = session.get("https://funpay.com/chips/2/trade").text
html_objects = BeautifulSoup(html, "html.parser")
print(json.loads(html_objects.find("body")["data-app-data"])["csrf-token"])
data = dict()
with open("test.txt", "r") as f:
    for row in f.readlines():
        parts = row.split(":")
        data[parts[0].strip()] = parts[1].strip() if parts[1].strip() else ""
data["csrf_token"] = json.loads(html_objects.find("body")["data-app-data"])[
    "csrf-token"
]
print(session.post("https://funpay.com/chips/saveOffers", data=data))
