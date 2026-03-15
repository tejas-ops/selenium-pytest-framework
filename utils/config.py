import os

BASE_URL = "https://the-internet.herokuapp.com"
API_BASE_URL = "https://jsonplaceholder.typicode.com"
BROWSER = os.getenv("BROWSER", "safari").strip().lower()
BASE_TIMEOUT = 10