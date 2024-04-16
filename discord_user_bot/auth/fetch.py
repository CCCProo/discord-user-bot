import requests
import json

from http.client import HTTPSConnection
from urllib.parse import urlparse
from .data import ClientData
from .fingerprint import Fingerprint
from .uuid import UUID
from .cookie import CookieGenerator
from ..util.error import DiscordAPIError

class Requester:
    def __init__(self, proxy=None):
        self.url = "https://discord.com"
        self.api = "v9"
        self.default_data = ClientData("Windows", "Chromium", "109.0", None, None, Fingerprint(self), UUID())
        self.cookie = ""
        self.is_registering = False
        self.proxy = None
        if proxy is not None:
            self.proxy = {"https": f"https://{proxy}"}

    async def build_request(self, body, client_data, method, extra_headers=None):
        if not self.cookie:
            cookie_gen = CookieGenerator(self)
            self.cookie = await cookie_gen.compile()

        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "cookie": self.cookie,
            "Referer": f"{self.url}/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "dnt": "1",
            "origin": self.url,
            **(extra_headers or {}),
        }

        if client_data.fingerprint:
            headers["x-fingerprint"] = client_data.fingerprint.fingerprint

        if client_data.xtrack:
            headers["x-track"] = client_data.xtrack if self.is_registering else client_data.xtrack

        if client_data.ua:
            headers["user-agent"] = client_data.ua

        if client_data.authorization:
            headers["authorization"] = client_data.authorization

        if method in ["POST", "PATCH"]:
            if not isinstance(body, dict):
                raise ValueError("Invalid body")

        fetch_request = {
            "headers": headers,
            "method": method,
        }

        if self.proxy:
            fetch_request["proxies"] = self.proxy

        return fetch_request

    def build_noparse(self):
        fetch_request = {
            "method": "GET",
        }

        if self.proxy:
            fetch_request["proxies"] = self.proxy

        return fetch_request

    async def fetch_request(self, url, body=None, client_data=None, method="POST", extra_headers=None):
        client_data = client_data or self.default_data
        fetch_request = await self.build_request(body, client_data, method, extra_headers)
        
        # Convert MentionsLimiter object to a dictionary
        if body and 'allowed_mentions' in body and hasattr(body['allowed_mentions'], '__dict__'):
            body['allowed_mentions'] = body['allowed_mentions'].__dict__
        
        response = requests.request(
            method,
            url=f"{self.url}/api/{self.api}/{url}",
            headers=fetch_request['headers'],
            json=body,
            proxies=self.proxy if self.proxy else None
        )

        try:
            return response.json()
        except ValueError:
            return response.status_code


    async def fetch_noparse(self, url):
        fetch_request = self.build_noparse()
        print(f"\n\n\n\n\n\n{fetch_request['method']}\n")
        response = requests.get(url)
        return response
