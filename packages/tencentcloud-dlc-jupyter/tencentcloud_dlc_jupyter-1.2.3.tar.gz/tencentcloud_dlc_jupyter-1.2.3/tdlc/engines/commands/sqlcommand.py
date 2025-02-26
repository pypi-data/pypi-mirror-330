from .command import Command
from .storecommand import StoreCommand
from tdlc.utils import constants, common
from tdlc import exceptions
import abc


class SQLCommand(StoreCommand):

    def __init__(
        self,
        query,
        sample_method=None, 
        max_rows=None, 
        sample_fraction=None, 
        coerce=None):
        super().__init__(None, sample_method, sample_fraction, max_rows, coerce)

        self.query = query
    

    def _scala_command(self, output_var_context):

        code = f'{output_var_context}.sql("""{self.query}""").toJSON'

        if self.sample_method == "sample":
            code = f"{code}.sample(false, {self.sample_fraction})"
        if self.max_rows >= 0:
            code = f"{code}.take({self.max_rows})"
        else:
            code = f"{code}.collect"
        return Command("{}.foreach(println)".format(code))
    
    def _pyspark_command(self, output_var_context):

        if self.query.strip().startswith("show"):
            code = f'{output_var_context}.sql(u"""{self.query}""").collect()'

            if self.max_rows >= 0:
                code = f'{code}[:{self.max_rows}]'

        else:
            code = f'{output_var_context}.sql(u"""{self.query}""").toJSON(use_unicode=True)'

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
        # TODP events
        self.output_var = session.spark_or_sql_context_var_name
        return super().execute(session, kind)
