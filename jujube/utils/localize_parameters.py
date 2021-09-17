from inspect import signature
from functools import wraps


def localize_annotations(strings):

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print(self)
            return func(self, *args, **kwargs)

        sig = signature(func)

        new_params = [*list(sig.parameters.values())[0:2]]

        print(list(sig.parameters.values())[2:len(sig.parameters) - 2])

        for idx, param in enumerate(list(sig.parameters.values())[2:len(sig.parameters) - 2]):
            new_param = param.replace(annotation='bob')
            new_params.append(new_param)
        new_params += list(sig.parameters.values())[len(sig.parameters) - 2:]

        sig = sig.replace(parameters=new_params)
        print(sig)
        wrapper.__signature__ = sig

        return wrapper
    return decorator
