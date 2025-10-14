def login_user(username: str, password: str) -> str:
    if username == "admin" and password == "admin":
        return "fake-jwt-token"
    return ""
    