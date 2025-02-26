from tdlc.utils import render, log
from tdlc.tencentcloud.common import exception

LOG = log.getLogger('TDLC')


def wrap_magic_exceptions(f):

    def wrapper(self, *args, **kwargs):

        try:
            r = f(self, *args, **kwargs)
        except tdlcException as e:
            render.toStderr(e)
            LOG.error(e)
        except exception.TencentCloudSDKException as e:
            render.toStderr(e)
            LOG.error(e)
        except Exception as e:
            LOG.error(e)
            raise
        else:
            return r
    
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    return wrapper


def wrap_ipython_exceptions(f, execute_if_error=None):

    def handle_exception(self, e):
        # TODP
        render.toStderr(e)
        return None if execute_if_error is None else execute_if_error()

    def wrapped(self, *args, **kwargs):
        try:
            out = f(self, *args, **kwargs)
        except Exception as e:
            raise e
            return handle_exception(self, err)
        else:
            return out

    wrapped.__name__ = f.__name__
    wrapped.__doc__ = f.__doc__
    return wrapped
    

'''
ErrorType : Error Message.

Error stacks.

'''

class tdlcException(Exception):

    _pre = ''
    message = ''
    _post = ''
    stack_message = ''

    def __init__(self, pre='', message=None, post='', stacks='', *args, **kwargs):
        super().__init__()

        self._post = pre
        self._post = post
        self.stack_message = stacks
        if message is not None:
            self.message = message

        self._args = args

    def stacks(self, message):
        self.stack_message = message
    
    def __str__(self) -> str:

        message = self.message
        if self.args:
            message = message.format(*self.args)

        if self._pre:
            message = self._pre + message
        if self._post:
            message = message + self._post

        
        msg = f'[{self.__class__.__name__}] {message}'
        if self.stack_message:
            msg += '\n\n' + self.stack_message
        return msg

class ImageNotExistsException(tdlcException):
    message = "The image is not exists."

class EngineNotReadyException(tdlcException):
    message = "The engine is not ready, please check engines in DLC console. "

class EngineNotExistException(tdlcException):
    message = "The engine is not found, please check engines in DLC console. "

class EngineInsufficientException(tdlcException):
    message = "The engine resource is insufficient. "

class RoleArnNotFoundException(tdlcException):
    message = "The roleArn is not found in CAM. "

class SessionExistException(tdlcException):
    message = "The session name is alreay exists local. "

class SessionNotFoundException(tdlcException):
    message = "The session is not found. please use '%spark sessions [--remote]' to see all sessions. "

class SessionContextException(tdlcException):
    message = "SparkSesstion/HiveContext/SqlContext is not available. "

class SessionAttachedException(tdlcException):
    message = "The session is already attached. "

class SessionNotAvailableException(tdlcException):
    message = "There is no available session, please create or attach a session first. "

class SessionTimeoutException(tdlcException):
    message = "The session is timeout. "

class SessionIsLimitedException(tdlcException):
    message ='The session is limited in current mode.'

class SessionTerminated(tdlcException):
    message = "The session is terminated. "

class ValidationException(tdlcException):
    message = "The validation fails. "

class UnSupportedException(tdlcException):
    message = "The operation is not supported. "


class CommandNotFoundException(tdlcException):
    message = "The subcommand is not found, please use '%spark?' to see usage. "


class InterruptException(tdlcException):
    message = "The operation is interrupted by users. "

class NotFound(tdlcException):
    message = "Not found. "

class UnknownStatusException(tdlcException):
    pass

class UnexpectedStatusException(tdlcException):
    message = "The status is unexpected. "

class StatementCancelFailedException(tdlcException):
    message = "The statement cancel failed. "

class StatementCancelledException(tdlcException):
    message = "The statement has been cancelled. "

class IllegalInputException(tdlcException):
    message = "The input is illigal. "

class DataframeParseException(tdlcException):
    message = 'Parse dataframe error.'

class InternalErrorException(tdlcException):
    message = "Internal Error. "




