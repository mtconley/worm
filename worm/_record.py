from multiprocessing import current_process

class Record(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def update(self, attrs):
        self.__dict__.update(attrs)
        return self

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return None
    def __setitem__(self, name, value):
        self.__dict__[name] = value
        
    def __repr__(self):
        return 'Record({})'.format(repr(self.__dict__))

class RecordHandler(object):
    def __init__(self, funcs):
        self.funcs = funcs

    def __call__(self, data):
        for func in self.funcs:
            data = func(data)
        name = current_process().name
        msg = {'name': name,
               'data': data}
        return msg
