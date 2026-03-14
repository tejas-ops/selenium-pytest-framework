import os

BASE_URL = "https://the-internet.herokuapp.com"
BROWSER = os.getenv("BROWSER", "safari").lower()
BASE_TIMEOUT = 10