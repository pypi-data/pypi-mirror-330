
from ipykernel.ipkernel import IPythonKernel
from tdlc.utils import render, log
from tdlc import exceptions
import asyncio
import inspect

LOG = log.getLogger('Kernel')

# NOTE: This is a (hopefully) temporary workaround to accommodate async do_execute in ipykernel>=6
import nest_asyncio


# NOTE: This is a (hopefully) temporary workaround to accommodate async do_execute in ipykernel>=6
# Taken from: https://github.com/jupyter/notebook/blob/eb3a1c24839205afcef0ba65ace2309d38300a2b/notebook/utils.py#L332
def run_sync(maybe_async):
    """If async, runs maybe_async and blocks until it has executed,
    possibly creating an event loop.
    If not async, just returns maybe_async as it is the result of something
    that has already executed.
    Parameters
    ----------
    maybe_async : async or non-async object
        The object to be executed, if it is async.
    Returns
    -------
    result :
        Whatever the async object returns, or the object itself.
    """
    if not inspect.isawaitable(maybe_async):
        # that was not something async, just return it
        return maybe_async
    # it is async, we need to run it in an event loop

    def wrapped():
        create_new_event_loop = False
        result = None
        loop = None
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            create_new_event_loop = True
        else:
            if loop.is_closed():
                create_new_event_loop = True
        if create_new_event_loop:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(maybe_async)
        except RuntimeError as e:
            if str(e) == "This event loop is already running":
                # just return a Future, hoping that it will be awaited
                result = asyncio.ensure_future(maybe_async)
        return result

    return wrapped()


class Kernelbase(IPythonKernel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        LOG.debug(f"Create '{self.implementation}' kernel with language={self.language}")

        self._fatal_error = None
        
        # NOTE: This is a (hopefully) temporary workaround to accommodate async do_execute in ipykernel>=6
        # Patch loop.run_until_complete as early as possible
        try:
            nest_asyncio.apply()
        except RuntimeError:
            # nest_asyncio requires a running loop in order to patch.
            # In tests the loop may not have been created yet.
            pass
        
        self._load_magics_extension()


    def _load_magics_extension(self):
        code = "%load_ext tdlc.kernels"
        LOG.info('Auto loading magics.')
        self._do_execute_cell(
            code,
            True,
            False,
            shutdown_if_error=True,
            log_if_error="Failed to load the Spark kernels magics library.",
        )


    def _code_parser(self, code:str):

        if code.startswith("%%local") or code.startswith("%local"):
            try:
                line = code.split(None, 1)[1]
            except IndexError:
                line = ""
            return line
        elif code.startswith(('%start', '%stop', '%session', '%attach', '%detach', '%logs', '%send')):
            return '%_spark ' + code.lstrip('%')
        elif code.startswith(('%%sql', '%%config')):
            return '%%_spark ' + code.lstrip('%%')
        elif code.startswith(('%', '%%')):
            return code
        else:
            return f'%%_spark\n{code}'

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False, *, cell_id=None):

        LOG.debug(f"Executing code:\n{code}")

        statement = self._code_parser(code)

        def f(self):
            if self._fatal_error is not None:
                return self._repeat_fatal_error()

            return self._do_execute_cell(
                statement, silent, store_history, user_expressions, allow_stdin
            )

        wrapped = exceptions.wrap_ipython_exceptions(f, self._complete_cell)
        return wrapped(self)
    

    def _do_execute_cell(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
        shutdown_if_error=False,
        log_if_error=None,
    ):

        task = super().do_execute(code, silent, store_history, user_expressions, allow_stdin)

        # In ipykernel 6, this returns native asyncio coroutine
        if asyncio.iscoroutine(task):
            result = run_sync(task)
        # In ipykernel 5, this returns gen.coroutine
        elif asyncio.asyncio.isfuture(task):
            result = task.result()
        # In ipykernel 4, this func is synchronous
        else:
            result = task

        if shutdown_if_error and result["status"] == "error":
            error_from_reply = result["evalue"]
            if log_if_error is not None:
                message = '{}\nException details:\n\t"{}"'.format(
                    log_if_error, error_from_reply
                )
                return self._abort_with_fatal_error(message)

        return result
    

    def _complete_cell(self):
        return self._do_execute_cell("None", False, True, None, False)

    def _display_fatal_error(self):
        error = f"""The code failed because of a fatal error:\t{self._fatal_error}.
Some things to try:
a) Make sure Spark cluster has enough available resources to create a Spark context.
b) Make sure your TDLC is configured correctly.
c) Restart the kernel."""

        LOG.error(error)
        render.toStderr(error)

        return self._complete_cell()
