import json


class User(object):
    def __init__(self, name, username, passw):
        self.name = name
        self.username = username
        self.passw = passw


def object_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'User':
        return User(obj['name'], obj['username'], obj['passw'])
    return obj


x = json.loads('{"__type__": "User", "name": "John Smith", "username": "jsmith", "passw": "123"}', object_hook=object_decoder)
#x = json.loads('{"obstacles": { "latitude": 38.141826869853645, "longitude": -76.43199876559223}}', object_hook=object_decoder)

print(x.name)
