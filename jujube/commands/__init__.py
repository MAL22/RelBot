import shlex
from jujube.app_config import GlobalAppConfig


def split_arguments(message):
    command, *args = shlex.split(message)
    contains_prefix = command.startswith(GlobalAppConfig().prefix)
    if contains_prefix:
        command = command.strip(GlobalAppConfig().prefix)
    return contains_prefix, command, args
