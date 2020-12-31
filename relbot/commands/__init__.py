import shlex
from relbot.app_config import GlobalAppConfig


def split_arguments(input_: str):
    command, *args = shlex.split(input_)
    contains_prefix = command.startswith(GlobalAppConfig().prefix)
    if contains_prefix:
        command = command.strip(GlobalAppConfig().prefix)
    return contains_prefix, command, args
