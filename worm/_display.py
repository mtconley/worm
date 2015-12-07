from StringIO import StringIO
from pandas import DataFrame, options
from numpy import zeros
from IPython.display import HTML, display, clear_output
import sys

class Status(StringIO):
     
    def __init__(self, total, line_count, update_interval=.05):
        StringIO.__init__(self)
        self.container = {}
        self.counter = {}
        self.total = total
        self.columns = ['name', 'progress', 'update', 'count']
        self._make_board(line_count)

        if self._is_notebook():
            self.fmt = self._notebook_format
            self.flush = self._notebook_flush
        else:
            self.fmt = self._console_format
            self.flush = self._console_flush

        interval = int(update_interval * self.total)
        self.interval = interval if interval > 0 else 1

    def _is_notebook(self):
        try:
            from IPython.core.interactiveshell import InteractiveShell
            from IPython.kernel.zmq.zmqshell import ZMQInteractiveShell as notebook
            from IPython.terminal.interactiveshell import TerminalInteractiveShell as shell
            if InteractiveShell.initialized():
                ip = get_ipython()
                if isinstance(ip, notebook):
                    return True
                elif isinstance(ip, shell):
                    return False
                else:
                    raise Exception('Wrong Shell')
            else:
                return False
        except Exception as e:
            self._print_error(e)
            return False

    def _make_board(self, line_count):
        index = range(line_count)
        data = zeros((line_count, len(self.columns)))
        self.board = DataFrame(data=data, columns=self.columns, index=index)
            
    def _notebook_format(self, prog):
        string = '<progress value="{prog:2.2f}" max="100"></progress>'
        string = string.format(prog=prog)
        return string

    def _console_format(self, prog):
        full = (prog) / 3
        empty = 33 - full
        progress = '#' * full + ' ' * empty
        string = '[' + progress + ']'
        return string

    def _notebook_flush(self):
        try:
            data = self.container
            columns = ['name', 'count']
            df = DataFrame(data).T
            df['progress'] = df['count'].astype(int) / self.total * 100
            df['update'] = df['progress']
            df.sort_index(inplace=True)
            fields = ['name', 'progress', 'update']
            df['update'] = df['update'].apply(self.fmt)
            board = df[fields]

        
            display(HTML(board.to_html(escape=False)))

        except Exception as e:
            self._print_error(e)

    def _console_flush(self):
        pass

    def write(self, name):
        try:
            self.counter[name] = self.counter.get(name, len(self.counter))
            lineno = self.counter[name]

            self.container[lineno] = self.container.get(lineno, {'name': name, 'count': 0})
            self.container[lineno]['count'] += 1

            count = self.container[lineno]['count']

            if (count %  self.interval == 0):
                clear_output(True)
                self.flush()
        except Exception as e:
            self._print_error(e)

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