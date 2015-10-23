import sys
import multiprocessing as mp

from itertools import izip
from pandas import DataFrame

from numpy.random import choice as npchoice
import pickle as pkl
from itertools import groupby

from .record import Record, RecordHandler
from .executor import ExecutorQuery, ExecutorMap, ExecutorFilter
from .display import Status

class CollectionObject(object):
    def __init__(self, df, **kwargs):
        self.data = self._orm(df, **kwargs)
        
        self._count = len(self.data)
        self._funcs = []
            
    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__class__(self.data[item])
        else:
            return self.data[item]
        
    def __len__(self):
        return self._count
    
    def __repr__(self):
        data = '[' + ',\n'.join(map(str, self.data[:5]))
        elipses = ',\n...' if self._count > 5 else ''
        data = data + elipses + ']'
        info = '{0} Record Objects'.format(self._count)
        return data + '\n\nCollection Object with\n' + info
    
    def __str__(self):
        return repr(self.data[:5])
        
    def _is_df(self, data):
        return isinstance(data, DataFrame)
    
    def _is_record(self, data):
        return isinstance(data, Record)
    
    def _is_collection(self, data):
        return isinstance(data, list) and isinstance(data[0], Record)
    
    def _relay(self, data):
        if self._is_df(data) and sum(data.shape) > 0:
            return True
        elif self._is_df(data) and sum(data.shape) == 0:
            return False
        elif data:
            return True
        else:
            return False
    
    def _orm(self, data, **kwargs):
        if self._is_df(data):
            fields = ['index_record'] + data.columns.tolist()
            return [Record().update(dict(izip(fields, row))).update(kwargs) 
                    for row in data.itertuples()]
        
        elif self._is_record(data):
            return [data]
        
        elif self._is_collection(data):
            return data
        
        elif isinstance(data, list):
            return data
        
        else:
            return [data]
    
    def _make_list(self, item):
        flag = type(item) in (list, tuple)
        return item if flag else list(item)
    
    def to_df(self):
        return DataFrame(x.__dict__ for x in self.data).reset_index(drop=True)
        
    def _print_error(self, e):
        string = '\n\t'.join([
                '{0}', # Exception Type
                'filename: {1}', # filename
                'lineno: {2}\n']) # lineno of error

        fname = sys.exc_info()[2].tb_frame.f_code.co_filename
        tb_lineno = sys.exc_info()[2].tb_lineno

        args = (repr(e), fname, tb_lineno)
        sys.stderr.write(string.format(*args))
        sys.stderr.flush()

class SparkAPI(object):
    
    def count(self):
        return self._count

    def take(self, n):
        return self.data[:n]

    def first(self):
        return self.take(1)

    def takeSample(self, withReplacement, num):
        return npchoice(self.data, num, replace=withReplacement).tolist()

    def takeOrdered(self, n, ordering=None):
        raise NotImplementedError

    def saveAsTextFile(self, path):
        self.to_df().to_csv(path, index=False)

    def saveAsSequenceFile(self, path):
        raise NotImplementedError

    def saveAsObjectFile(self, path):
        with open(path, 'wb') as pklfile:
            pkl.dump(self, pklfile)

    def countByKey(self, key):
        grp = groupby(self.data, key=lambda x: getattr(x, key))
        return {k: len(list(v)) for k, v in grp}

    def foreach(self, func):
        self.data = map(func, self)


class Collection(CollectionObject, SparkAPI):
    
    def query(self, func):
        execute = ExecutorQuery(func)
        self._funcs.append(execute)
        return self        
    
    def map(self, func):
        execute = ExecutorMap(func)
        self._funcs.append(execute)
        return self
        
    def filter(self, func):
        execute = ExecutorFilter(func)
        self._funcs.append(execute)
        return self
        
    def reduce(self, func):
        execute = ExecutorReduce(func)
        self._funcs.append(execute)
        return self
        
    def collect(self):
        cpu_count = min(mp.cpu_count(), 20)
        pool = mp.Pool(cpu_count)

        chunksize = ((self._count - 1) + cpu_count) / cpu_count
        status = Status(chunksize, cpu_count)
        try:
            result = []
            rh = RecordHandler(self._funcs)    
            amr = pool.imap_unordered(rh, self.data, chunksize)
            for ix, msg in enumerate(amr):
                name = msg['name']
                data = msg['data']
                status.write(name)
                if self._relay(data):
                    data = self._orm(data)
                    result.extend(data)
            self._funcs = []
            self.data = result
            
        except Exception as e:
            self._print_error(e)
            
        finally:
            pool.close()
            pool.join()


def run(dataframe, query=None, mappers=None, **kwargs):
    mappers = mappers or []

    c = Collection(dataframe)
    
    if query:
        c.query(query)
     
    for mapper in mappers:        
        c = c.map(mapper)
        
    if 'funcs' in kwargs:
        funcs = kwargs['funcs']
        
        command = {
        'query': c.query,
        'map': c.map,
        'filter': c.filter,
        'reduce': c.reduce}
        
        for iterfunc, func in funcs:
            c = command[iterfunc](func)
        
    c.collect()
    return c.to_df()