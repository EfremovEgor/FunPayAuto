from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium
import json

URL = "https://funpay.com/account/login"


def get_cookies(url: str = URL, load_from_cfg: bool = False) -> dict:
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option("detach", False)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(URL)
    try:
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-link-photo"))
        )
    except selenium.common.exceptions.TimeoutException:
        driver.close()
        raise selenium.common.exceptions.TimeoutException
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
