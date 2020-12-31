import json
import io
from json import JSONDecodeError


def read(filename):
    try:
        with open(filename) as file:
            return json.load(file)
    except JSONDecodeError as error:
        raise error


def write(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except io.UnsupportedOperation as error:
        raise error
