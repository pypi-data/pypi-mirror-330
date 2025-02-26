from .command import Command
from abc import abstractmethod
from tdlc.utils import constants
from tdlc import exceptions


class VarToSparkCommand(Command):

    def __init__(self, code) -> None:
        super().__init__(code)
    
    def execute(self, session, kind=None):
       return self.to_command(kind or session.kind).execute(session, kind)

    @abstractmethod
    def _scala_command(self) -> Command:
        raise NotImplemented
    
    @abstractmethod
    def _pyspark_command(self) -> Command:
        raise NotImplemented

    @abstractmethod
    def _r_command(self) -> Command:
        raise NotImplemented
    
    def to_command(self, kind):

        if kind == constants.SESSION_KIND_PYSPARK:
            return self._pyspark_command()
        elif kind == constants.SESSION_KIND_SPARK:
            return self._scala_command()
        elif kind == constants.SESSION_KIND_SPARKR:
            return self._r_command()
        else:
            raise exceptions.UnSupportedException(f"The '{kind}' is not supported.")
		