import os

USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "password123")
LOGIN_PATH = "/auth"
BASE_URL = "https://restful-booker.herokuapp.com"
