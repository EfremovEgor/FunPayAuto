import bcrypt
import requests
import os


def access_granted() -> bool:
    pwd_file_path = os.path.join(os.getcwd(), "password.txt")
    if not os.path.exists(pwd_file_path):
        return False
    with open(pwd_file_path, "r") as f:
        password = f.readline().strip()
    bytes_password = bytes(
        requests.get("https://pastebin.com/raw/KbUMsSDY").text, "utf-8"
    )
    return bcrypt.checkpw(password.encode("utf-8"), bytes_password)
