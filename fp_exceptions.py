class SiteDoesNotResponseError(BaseException):
    def __init__(self, status_code: None = "Invalid") -> None:
        self.status_code = status_code

    def __str__(self) -> str:
        return f"Site doesn't response.\nError code:{self.status_code}."


class AuthenticationError(BaseException):
    def __str__(self) -> str:
        return "Something went wrong with authentification.\nPlease login or register."


class CookiesFileNotFoundError(BaseException):
    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"Cookies file not found at {self.path}."


class ConfigNotFoundError(BaseException):
    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"Config file not found at {self.path}."
