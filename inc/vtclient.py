from inc.config import Config
# import requests


class VTClient():
    def __init__(self):
        self.apiKey = Config.getInstance().get('api-key')

    def check(self, hostname):
        pass
