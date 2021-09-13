

class Map(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict) or isinstance(arg, list):
                for k, v in arg.items():
                    if isinstance(v, dict):
                        self[k] = Map(v)
                    else:
                        k = k.lower()
                        self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, item):
        # return self.get(item)
        return self[item]

    def __setattr__(self, key, value):
        self.__setitem__(self, key, value)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        dict.__delitem__(key)
        del self.__dict__[key]


"""ab = {'a': 0}
map = Map({'first_name': 'Bob', 'last_name': 'Lennon', 'id': {'test': {'Bananas': 0}}})

print(type(map.id))
print(map.id.test.bananas)
print(map['id'])
print(ab['b'])

del ab, map"""
