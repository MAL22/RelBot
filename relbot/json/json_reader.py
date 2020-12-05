import json


def read(file_name: str):
    with open('{}'.format(file_name)) as file:
        return json.load(file)
