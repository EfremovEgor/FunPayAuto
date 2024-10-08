from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager
import selenium
import json
from tkinter.messagebox import showerror, showwarning, showinfo

URL = "https://funpay.com/chips/2/trade"


def get_cookies(url: str = URL, load_from_cfg: bool = False) -> dict:
    options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # chrome_options.add_experimental_option("detach", False)
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)

    driver.get(URL)
    try:
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-link-photo"))
        )
    except selenium.common.exceptions.TimeoutException:
        driver.close()
        ex = selenium.common.exceptions.TimeoutException
        showerror(title="Error", message=str(ex))

        raise ex
    cookies = {}
    for cookie in driver.get_cookies():
        cookies.update({cookie["name"]: cookie["value"]})
    return cookies


def save_cookies(cookies: dict) -> None:
    with open(".\data\cookies.json", "w") as file:
        json.dump(cookies, file, indent=4)


def read_cookies(path: str = ".\data\cookies.json") -> dict:
    with open(".\data\cookies.json", "r") as json_file:
        cookies = json.load(json_file)
    return cookies
