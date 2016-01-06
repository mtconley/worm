from StringIO import StringIO
from pandas import DataFrame, options
from numpy import zeros
from IPython.display import HTML, display, clear_output
import sys

class Status(StringIO):
     
    def __init__(self, total, line_count, update_interval=.05):
        self.total = float(total)
        self._make_board(line_count)
        self._set_interval(update_interval)
        self._set_environment()
        
    def write(self, name):
        try:
            if name not in self.board.index:
                self.board.loc[name, 'count'] = 0
            count = self.board.loc[name, 'count'] + 1
            self.board.loc[name, 'count'] = count
            self.board.loc[name, 'progress'] = count / self.total * 100
            
            if (count %  self.interval == 0):
                clear_output(True)
                self.flush()
                
        except Exception as e:
            self._print_error(e)
            
            

    def _make_board(self, line_count):
        columns = ['progress', 'update', 'count']
        #data = zeros((line_count, len(columns)))
        self.board = DataFrame(columns=columns)
        
    def _set_interval(self, update_interval):
        interval = int(update_interval * self.total)
        self.interval = interval if interval > 0 else 1
        
    def _set_environment(self):
        if self._is_notebook():
            self.flush = self._notebook_flush
        else:
            self.flush = self._console_flush
        
            
    def _notebook_flush(self):
        string = '<progress value="{prog:2.2f}" max="100"></progress>'
        self.board['update'] = self.board['progress'].apply(lambda x: string.format(prog=x))
        progress = self.board[['update', 'progress']]
        progress.progress = progress.progress.apply(lambda x: '{:5.2f}%'.format(x))
        display(HTML(progress.to_html(escape=False)))

    def _console_flush(self):
        data = self.board['progress'].to_dict().items()
        stats = ['{}: {:05.2f}%'.format(name, progress) for name, progress in data]
        string = '; '.join(stats)
        sys.stdout.write('\r' + string)
        sys.stdout.flush()
   



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