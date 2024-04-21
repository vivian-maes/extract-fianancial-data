import json


def load():
    with open("config/application.json", "r") as config_file:
        config = json.load(config_file)
    return config
