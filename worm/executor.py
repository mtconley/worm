import sys
from pandas import DataFrame

class Executor(object):
    def __init__(self, func):
        self.func = func
                
    def _is_df(self, data):
        return isinstance(data, DataFrame)
    
    def _relay(self, data):
        if self._is_df(data) and sum(data.shape) > 0:
            return True
        elif self._is_df(data) and sum(data.shape) == 0:
            return False
        elif data:
            return True
        else:
            return False
        
    def print_error(self, e):
        string = '\n\t'.join([
                '{0}', # Exception Type
                'filename: {1}', # filename
                'lineno: {2}\n']) # lineno of error

        fname = sys.exc_info()[2].tb_frame.f_code.co_filename
        tb_lineno = sys.exc_info()[2].tb_lineno

        args = (repr(e), fname, tb_lineno)
        sys.stderr.write(string.format(*args))
        sys.stderr.flush()
        
class ExecutorMap(Executor):
    def __call__(self, data):
        try:
            if self._relay(data):
                return self.func(data)
            else:
                return
        except Exception as e:
            self.print_error(e)
            return 
    
class ExecutorFilter(Executor):

    def __call__(self, data):
        try:
            result = self.func(data)
            if result:
                return data
            else:
                return
        except Exception as e:
            self.print_error(e)
            return
        
class ExecutorQuery(Executor):
    def __call__(self, record):
        try:
            if self._relay(data):
                dataframe = self.func(record)
                for attr in record.__dict__:
                    value = getattr(record, attr)
                    dataframe[attr] = value
                return dataframe
            else:
                return record
        except Exception as e:
            self.print_error(e)
            return