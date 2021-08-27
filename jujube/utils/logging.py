import os
import datetime
from jujube import __title__ as TITLE

LOGGING = True
FOLDER_PATH = './logs/'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def generate_filename():
    return f'{TITLE}_log_{datetime.datetime.now().strftime("%Y%m%d%H%M")}.log'


filename = generate_filename()


def create_directory():
    if os.path.exists(FOLDER_PATH):
        return
    os.mkdir(FOLDER_PATH)


def log(*args):
    if LOGGING:
        print(f'[{datetime.datetime.now().strftime(TIME_FORMAT)}]', *args)
        print(f'[{datetime.datetime.now().strftime(TIME_FORMAT)}]', *args, file=open(os.path.join(FOLDER_PATH, filename), 'a'))


create_directory()
