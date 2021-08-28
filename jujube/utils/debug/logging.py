import os
import pathlib
from .timer import measure_exec_time
from datetime import datetime, timedelta
from jujube import __title__ as TITLE

LOGGING = True
FOLDER_PATH = './logs/'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TIMEDELTA_FILE_DELETION = timedelta(weeks=0, days=1, hours=0, minutes=0, seconds=0)
TIMEDELTA_LOG_OBSOLESCENCE = timedelta(weeks=0, days=0, hours=0, minutes=30, seconds=0)


def generate_filename():
    log_file = None
    for dirpath, dirnames, filenames in os.walk(os.path.realpath(FOLDER_PATH)):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_ctime = datetime.fromtimestamp(os.path.getctime(file_path))
            print(f'{file_ctime} < {datetime.now() - TIMEDELTA_LOG_OBSOLESCENCE}')
            if file_ctime < datetime.now() - TIMEDELTA_LOG_OBSOLESCENCE:
                continue
            if log_file and file_ctime < datetime.fromtimestamp(os.path.getctime(log_file)):
                continue
            log_file = file_path

    if log_file is None:
        return f'{TITLE}_log_{datetime.now().strftime("%Y.%m.%d-%H.%M.%S")}.log'
    return log_file


filename = generate_filename()


def _create_directory():
    if os.path.exists(FOLDER_PATH):
        return
    os.mkdir(FOLDER_PATH)


def _remove_expired_logs():
    for dirpath, dirnames, filenames in os.walk(os.path.realpath(FOLDER_PATH)):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if datetime.now() - TIMEDELTA_FILE_DELETION > datetime.fromtimestamp(os.path.getctime(file_path)):
                try:
                    os.remove(file_path)
                except IOError as e:
                    log(e)


def log(*args, **kwargs):
    omit_file = kwargs.pop('omit_file', False)
    if LOGGING:
        print(f'[{datetime.now().strftime(TIME_FORMAT)}]', *args)
        if omit_file:
            return
        print(f'[{datetime.now().strftime(TIME_FORMAT)}]', *args, file=open(os.path.join(FOLDER_PATH, filename), 'a'))


_create_directory()
_remove_expired_logs()