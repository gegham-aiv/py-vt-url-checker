import base64

from inc.config import Config
from requests import request
import time


class VTClient():
    def __init__(self):
        self.api_key = Config.getInstance().get('api-key')
        self.url_base = Config.getInstance().get('url-base')
        self.headers = {"x-apikey": self.api_key, "Accept": "application/json"}

    def __make_request(self, method, url, params=None):
        url = f"{self.url_base}/{url}"
        response = request(
            method=method,
            url=url,
            headers=self.headers,
            data=params,
        )
        response.raise_for_status()
        return response.json()

    def get(self, url):
        return self.__make_request('get', url)

    def post(self, url, params):
        return self.__make_request('post', url, params)

    def check_host(self, hostname):
        self.post("urls", {'url': hostname})
        encoded_url = base64.b64encode(hostname.encode())
        url_id = encoded_url.decode().replace('=', '')
        response_data = self.get(f"urls/{url_id}")
        while not response_data.get('data', {}).get('attributes', {}).get('last_analysis_results'):
            response_data = self.get(f"urls/{url_id}")
            time.sleep(3)

        return response_data.get('data', {}).get('attributes', {}).get('last_analysis_stats')
