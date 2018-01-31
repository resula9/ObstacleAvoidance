import json


class User(object):
    name = {}

    def __init__(self, name, username, passw):
        self.name = name
        self.username = username
        self.passw = passw


def object_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'User':
        return User(obj['name'], obj['username'], obj['passw'])
    return obj


x = json.loads('{"__type__": "User", "name": {"name1": "john", "name2": "smith"}, "username": ["j", "s"], "passw": "123"}', object_hook=object_decoder)


print x.name.get("name2")
