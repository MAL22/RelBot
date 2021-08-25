import datetime

LOGGING = True
FILE_PATH = './relbot.log'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def clear():
    with open(FILE_PATH, 'w'):
        pass


def log(*args):
    if LOGGING:
        print(f'[{datetime.datetime.now().strftime(TIME_FORMAT)}]', *args)
        print(f'[{datetime.datetime.now().strftime(TIME_FORMAT)}]', *args, file=open(FILE_PATH, 'a'))


clear()
