from .var2spark import VarToSparkCommand
from .command import Command
from tdlc.utils import constants, common, configurations, log
from tdlc import exceptions


LOG = log.getLogger('StoreCommand')


class StoreCommand(VarToSparkCommand):

    def __init__(
        self, 
        output_var, 
        sample_method=None, 
        sample_fraction=None, 
        max_rows=None, 
        coerce=None) -> None:
        super().__init__("")

        self.output_var = output_var
        self.sample_method = sample_method or configurations.RESULT_SAMPLE_METHOD.get()
        self.sample_fraction = sample_fraction or configurations.RESULT_SAMPLE_FRACTION.get()
        self.coerce = coerce
        self.max_rows = max_rows or configurations.RESULT_MAX_ROWS.get()


    def _scala_command(self, output_var_context):

        code = f"{output_var_context}.toJSON"
        
        if self.sample_method == "sample":
            code = f"{code}.sample(false, {self.sample_fraction})"
        if self.max_rows >= 0:
            code = f"{code}.take({self.max_rows})"
        else:
            code = f"{code}.collect"
        return Command("{}.foreach(println)".format(code))

    def _pyspark_command(self, output_var_context):

        code = f'{output_var_context}.toJSON(use_unicode=True)'

        if self.sample_method == "sample":
            code = f'{code}.sample(False, {self.sample_fraction})'
        if self.max_rows >= 0:
            code = f'{code}.take({self.max_rows})'
        else:
            code = "{}.collect()".format(code)

        print_code = constants.LONG_RANDOM_VAR_NAME
        code = "import sys\nfor {} in {}: print({})".format(
            constants.LONG_RANDOM_VAR_NAME, code, print_code
        )
        return Command(code)
    
    def execute(self, session, kind=None):

        (success, ouput, mime_type) = self.to_command(kind or session.kind, self.output_var).execute(session, kind)


        if not success:
            raise exceptions.IllegalInputException(stacks=ouput)
        
        result = common.records_to_dataframe(ouput, session.kind, self.coerce)
        return (True, result, mime_type)
    

    def to_command(self, kind, output_var_context):

        if kind == constants.SESSION_KIND_PYSPARK:
            return self._pyspark_command(output_var_context)
        elif kind == constants.SESSION_KIND_SPARK:
            return self._scala_command(output_var_context)
        elif kind == constants.SESSION_KIND_SPARKR:
            return self._r_command(output_var_context)
        else:
            raise exceptions.UnSupportedException(post=f"The '{kind}' is not supported.")
		