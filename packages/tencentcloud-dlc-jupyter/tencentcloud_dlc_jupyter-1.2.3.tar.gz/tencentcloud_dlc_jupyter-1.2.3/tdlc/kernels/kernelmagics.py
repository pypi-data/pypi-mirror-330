import imp
from IPython.core.magic import Magics, magics_class, line_magic, line_cell_magic, cell_magic, needs_local_scope
from IPython.core import magic_arguments

from tdlc.utils import constants
from tdlc.magics import remotemagics
from tdlc import exceptions
from tdlc.utils import render

@magics_class
class KernelMagics(remotemagics.RemoteMagics):

    def __init__(self, mode, shell=None, **kwargs):
        super().__init__( mode, shell, **kwargs)

        self.session = None

    @line_magic
    @exceptions.wrap_magic_exceptions
    def help(self, line, cell=None):

        _headers = ["Magic", "Usage", "Description"]
        magic_config = ["config", "%%config", "Config current kernel."]
        magic_start = ["start", "%start --engine <ENGINE>", "Start a new session."]
        magic_stop = ["stop", "%stop", "Stop current session."]
        magic_session = ["session", "%session [--remote]", "Show current session or remote sessions."]
        magic_attach = ["attach", "%attach --session-id <SESSIONID>", "Attach to session provided with --session-id."]
        magic_detach = ["detach", "%detach", "Detach from current session."]
        magic_logs = ["logs", "%logs", "Show logs for current session"]
        magic_sql = ["sql", "%%sql --quiet --sample-method take", "Executes a SQL query."]
        magic_send = ["send", "%send --var-input var1 --var-type str --var-output var2", "Send local var to spark."]

        render.asHTMLTable(_headers, [magic_config, magic_start, magic_stop, magic_session, magic_attach, magic_detach, magic_logs, magic_sql, magic_send])
        
        
    @line_cell_magic
    @exceptions.wrap_magic_exceptions
    def sql(self, line):
        pass

    @needs_local_scope
    @line_magic
    @exceptions.wrap_magic_exceptions
    def info(self, line, local_ns=None):
        pass

    @line_magic
    @exceptions.wrap_magic_exceptions
    def logs(self, line):
        pass
    
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "--quiet",
        type=bool,
        nargs="?",
        default=False,
        const=True,
        help="",
    )
    @needs_local_scope
    @line_magic
    @exceptions.wrap_magic_exceptions
    def start(self, line, local_ns=None):
        pass

    @needs_local_scope
    @line_magic
    @exceptions.wrap_magic_exceptions
    def stop(self, line, cell=None, local_ns=None):
        pass

    @needs_local_scope
    @line_magic
    @exceptions.wrap_magic_exceptions
    def local(self, line, cell=None, local_ns=None):
        pass

    @needs_local_scope
    @line_magic
    @exceptions.wrap_magic_exceptions
    def send(self, line, cell=None, local_ns=None):
        pass

    @needs_local_scope
    @line_magic
    @exceptions.wrap_magic_exceptions
    def config(self, line, cell=None, local_ns=None):
        pass

    '''  hidden magic, not exposed to user'''
    @needs_local_scope
    @line_cell_magic
    @exceptions.wrap_magic_exceptions
    def _spark(self, line, cell=None, local_ns=None):
        return super().spark(line, cell, local_ns)

def load_ipython_extension(ip):
    ip.register_magics(KernelMagics(constants.KERNEL_MODE_SPARK, ip))