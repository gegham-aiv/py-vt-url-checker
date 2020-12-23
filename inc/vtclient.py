import base64

from inc.config import Config
from requests import request
import time


class VTClient():
    def __init__(self):
        self.api_key = Config.getInstance().get('api-key')
        self.url_base = 'https://www.virustotal.com/api/v3'

    def __make_request(self, method, url, params=None):
        url = f"{self.url_base}/{url}"
        headers = {"x-apikey": self.api_key, "Accept": "application/json"}
        return request(
            method=method,
            url=url,
            headers=headers,
            data=params,
        ).json()

    def get(self, url):
        return self.__make_request('get', url)

    def post(self, url, params):
        return self.__make_request('post', url, params)

    def is_host_secure(self, hostname):
        self.post("urls", {'url': hostname})
        encoded_url = base64.b64encode(hostname.encode())
        url_id = encoded_url.decode().replace('=', '')
        responseData = self.get(f"urls/{url_id}")
        while not responseData['data']['attributes']['last_analysis_results']:
            responseData = self.get(f"urls/{url_id}")
            time.sleep(3)

        results = responseData['data']['attributes']['last_analysis_results']

        score = 0
        for provider in results:
            result = results[provider]
            if 'harmless' == result['category']:
                score += 1
            elif 'harmful' == result['category']:
                score -= 1

        return score
