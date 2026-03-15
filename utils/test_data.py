VALID_USERNAME = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"

INVALID_LOGIN_CASES = [
    ("wronguser", "SuperSecretPassword!", "Your username is invalid!"),
    ("tomsmith", "wrongpass", "Your password is invalid!"),
]