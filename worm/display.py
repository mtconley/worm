from StringIO import StringIO
from pandas import DataFrame, options
from IPython.display import HTML, display, clear_output
import sys
options.display.float_format = '{:2.2f}%'.format

class Status(StringIO):
     
    def __init__(self, total, line_count):
        StringIO.__init__(self)
        self.container = {}
        self.counter = {}
        self.total = total
            
    def fmt(self, prog):
        string = '<progress value="{prog:2.2f}" max="100"></progress>'.format(prog=prog)
        return string


    def write(self, name):
        try:
            self.counter[name] = self.counter.get(name, len(self.counter))
            lineno = self.counter[name]
            self.container[lineno] = self.container.get(lineno, {'name': name, 'count': 0})
            self.container[lineno]['count'] += 1
            count = self.container[lineno]['count']
            interval = int(.05 * self.total)
            interval = interval if interval > 0 else 1
            if (count %  interval == 0):
                clear_output(True)
                self.flush()
        except Exception as e:
            self.print_error(e)

    def flush(self):
        try:
            data = self.container
            columns = ['name', 'count']
            df = DataFrame(data).T
            df['progress'] = df['count'].astype(int) / self.total * 100
            df['update'] = df['progress']
            df['update'] = df['update'].apply(self.fmt)
            df.sort_index(inplace=True)
            fields = ['name', 'progress', 'update']
            display(HTML(df[fields].to_html(escape=False)))
        except Exception as e:
            self.print_error(e)

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