class Dictionary(dict):

    def __missing__(self, key):
        return str(key)