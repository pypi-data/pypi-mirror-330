from .var2spark import VarToSparkCommand
from .command import Command
from tdlc import exceptions



class StringVarToSparkCommand(VarToSparkCommand):
    def __init__(self, input_var_name, input_var_value, output_var_name) -> None:
        super().__init__("")

        self.input_var_name = input_var_name
        self.input_var_value = input_var_value
        self.output_var_name = output_var_name

    def _pyspark_command(self):
        self._assert_input_is_string_type()
        code = f'{self.output_var_name} = {repr(self.input_var_value)}'
        return Command(code)

    def _scala_command(self):
        self._assert_input_is_string_type()
        code = f'var {self.output_var_name} = """{self.input_var_value}"""'
        return Command(code)


    def _assert_input_is_string_type(self):

        if not isinstance(self.input_var_value, str):
            wrong_type =self.input_var_value.__class__.__name__
            raise exceptions.IllegalInputException(
                "{} is not a string! But {} instead".format(
                    self.input_var_name, wrong_type
                )
            )
