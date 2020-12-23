import json


class Config():
    __instance = None

    @staticmethod
    def getInstance():
        if (Config.__instance == None):
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance != None:
            raise Exception("Use getInstance instead")
        else:
            Config.__instance = self

        configFile = open('config/main.json', mode='r')
        config = configFile.read()
        configFile.close()
        self.data = json.loads(config)

    def get(self, key, defaultValue=None):
        return self.data[key] or defaultValue
