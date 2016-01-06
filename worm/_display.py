from StringIO import StringIO
from IPython.display import HTML, display, clear_output
from jinja2 import Template
import sys

class Status(StringIO):
     
    def __init__(self, total, line_count, update_interval=.05):
        self.total = float(total)
        self.worker_count = {}
        self._set_interval(update_interval)
        self._set_environment()
        self.data = []
        
    def write(self, name):
        try:
                
            count = self.worker_count.get(name, 0) + 1
            self.worker_count[name] = count
            
            if (count %  self.interval == 0) or (self.total - count < 5):
                self._make_board()
                
                clear_output(True)
                self.flush()
                
                
        except Exception as e:
            self._print_error(e)
            
    
    def _make_board(self):
        string = '<progress value="{prog:2.2f}" max="100"></progress>'
        self.data = []
        for name, count in sorted(self.worker_count.items()):
            progress = {}
            prog = self.worker_count[name] / self.total * 100
            progress['name'] = name
            progress['update'] = string.format(prog=prog)
            progress['progress'] = '{:5.2f}%'.format(prog)
            self.data.append(progress)
        
    def _set_interval(self, update_interval):
        interval = int(update_interval * self.total)
        self.interval = interval if interval > 0 else 1
        
    def _set_environment(self):
        if self._is_notebook():
            self.flush = self._notebook_flush
        else:
            self.flush = self._console_flush
        
            
    def _notebook_flush(self):
        board_template = """
        <table>
            <tr>
                <th></th>
                <th>Update</th>
                <th>Progress</th>
            </tr>
        {% for row in data %}
            <tr>
            <td><b>{{ row["name"] }}</b></td>
            <td>{{ row["update"] }}</td>
            <td>{{ row["progress"] }}</td>
            </tr>
        {% endfor %}
         </table>
        """
        template = Template(board_template)
        display(HTML(template.render(data=self.data)))

    def _console_flush(self):
        data = [[row['name'], row['progress']] for row in self.data]
        stats = ['{}: {}'.format(name, progress) for name, progress in data]
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