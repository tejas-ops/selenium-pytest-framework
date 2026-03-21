import os

BASE_URL = "https://the-internet.herokuapp.com"
API_BASE_URL = "https://reqres.in/api"
BROWSER = os.getenv("BROWSER", "safari").strip().lower()
BASE_TIMEOUT = int(os.getenv("BASE_TIMEOUT", "10"))
