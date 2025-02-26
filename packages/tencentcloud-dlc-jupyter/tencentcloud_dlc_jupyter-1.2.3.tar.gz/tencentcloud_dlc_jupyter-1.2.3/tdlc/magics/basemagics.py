from IPython.core.magic import Magics, magics_class
from tdlc.engines import controllers, commands
from tdlc.utils import constants, render, configurations, log, validators
from tdlc import exceptions
from six import string_types

LOG = log.getLogger('BaseMagics')


@magics_class
class BaseMagics(Magics):
    _VAR_TYPE_STRING = 'str'
    _VAR_TYPE_PANDAS_DATAFRAME = 'df'

    def __init__(self, mode, shell=None, **kwargs):
        super().__init__(shell, **kwargs)

        self.controller = controllers.EngineSessionController(mode)

    def var_to_spark(self,
                     name,
                     input_var_name,
                     var_type,
                     output_var_name,
                     max_rows):

        validators.required(input_var_name, "The input var is required.")
        validators.required(var_type, "The var type is required.")
        validators.required(output_var_name, "The ouput var is required.")

        if input_var_name not in self.shell.user_ns:
            raise exceptions.IllegalInputException(post=f"Variable '{input_var_name}' is not found.")

        input_var_value = self.shell.user_ns[input_var_name]
        if input_var_value is None:
            raise exceptions.IllegalInputException(post=f"Value of '{input_var_name}' is none.")

        if not output_var_name:
            output_var_name = input_var_name

        if not max_rows:
            max_rows = configurations.RESULT_MAX_ROWS.get()

        input_var_type = var_type.lower()

        if input_var_type == self._VAR_TYPE_STRING:
            command = commands.StringVarToSparkCommand(input_var_name, input_var_value, output_var_name)
        elif input_var_type == self._VAR_TYPE_PANDAS_DATAFRAME:
            command = commands.PandasVarToSparkCommand(input_var_name, input_var_value, output_var_name, max_rows)
        else:
            raise exceptions.IllegalInputException(
                post=f"Illegal variable -t type. Available are [{self._VAR_TYPE_STRING, self._VAR_TYPE_PANDAS_DATAFRAME}]")

        (success, out, mimetype) = self.controller.run_command(command, name)
        if not success:
            render.toStderr(out)
        else:
            render.render(f"Successfully passed '{input_var_name}' as '{output_var_name}' to Spark kernal.")

    def execute_spark(self,
                      name,
                      cell,
                      output_var,
                      sample_method,
                      sample_fraction,
                      max_rows,
                      coerce,
                      language=None):

        kind = None
        if language:
            kind = constants.LANGUAGE_TO_KIND[language]
        (success, out, mimetype) = self.controller.run_command(commands.Command(cell), name, kind)

        if not success:
            render.toStderr(out)
        else:

            if isinstance(out, string_types):
                if mimetype == constants.MIMETYPE_TEXT_HTML:
                    render.asHTML(out)
                else:
                    render.toStdout(out)
            else:
                render.render(out)

            if output_var is not None:
                command = commands.StoreCommand(output_var, sample_method, max_rows, sample_fraction, coerce)
                (success, out, mimetype) = self.controller.run_command(command, name, kind)
                self.shell.user_ns[output_var] = out

    def execute_sqlquery(self,
                         name,
                         cell,
                         output_var,
                         sample_method,
                         sample_fraction,
                         max_rows,
                         coerce,
                         quiet,
                         kind=None
                         ):
        command = commands.SQLCommand(cell, sample_method, max_rows, sample_fraction, coerce)

        (success, out, mimetype) = self.controller.run_command(command, name, kind)
        LOG.info(out)
        if output_var is not None:
            self.shell.user_ns[output_var] = out
        if quiet:
            return None
        else:
            return out
