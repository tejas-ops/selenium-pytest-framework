import os

BASE_URL = "https://the-internet.herokuapp.com"
BROWSER = os.getenv("BROWSER", "safari").strip().lower()
BASE_TIMEOUT = 10