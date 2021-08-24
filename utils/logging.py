_LOGGING = True


def log(*args):
    if _LOGGING:
        print(*args)
