import base64
import requests
from datetime import datetime, timedelta

class FlipkartAuth:
    BASE_URL = "https://api.flipkart.net"

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
