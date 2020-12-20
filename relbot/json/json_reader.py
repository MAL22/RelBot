import json
from json import JSONDecodeError


def read(file_name: str):
    try:
        with open('{}'.format(file_name)) as file:
            return json.load(file)
    except JSONDecodeError as e:
        raise e
