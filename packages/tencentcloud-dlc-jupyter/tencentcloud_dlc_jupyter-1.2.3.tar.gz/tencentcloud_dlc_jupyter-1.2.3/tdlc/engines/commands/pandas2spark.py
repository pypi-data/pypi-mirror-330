from .var2spark import VarToSparkCommand
from .command import Command
from tdlc import exceptions
import pandas as pd

class PandasVarToSparkCommand(VarToSparkCommand):
    def __init__(self, input_var_name, input_var_value, output_var_name, max_rows) -> None:
        super().__init__("")

        self.input_var_name = input_var_name
        self.input_var_value = input_var_value
        self.output_var_name = output_var_name
        self.max_rows = max_rows


    def _scala_command(self):
        self._assert_input_is_pandas_dataframe()

        pandas_json = self._get_dataframe_as_json(self.input_var_value)

        code = '''
        val rdd_json_array = spark.sparkContext.makeRDD("""{}""" :: Nil)
        val {} = spark.read.json(rdd_json_array)'''.format(
            pandas_json, self.output_var_name
        )

        return Command(code)

    def _pyspark_command(self):
        self._assert_input_is_pandas_dataframe()

        ''' 注意缩进 '''
        code = """
import sys
import json

def json_loads_byteified(json_text):
    return json.loads(json_text)

def _byteify(data, ignore_dicts = False):
    if isinstance(data, unicode):
        return data.encode('utf-8')
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    return data
        """

        pandas_json = self._get_dataframe_as_json(self.input_var_value)

        ''' 注意缩进 '''
        code += """
json_array = json_loads_byteified('{}')
rdd_json_array = spark.sparkContext.parallelize(json_array)
{} = spark.read.json(rdd_json_array)""".format(pandas_json, self.output_var_name)

        return Command(code)


    def _get_dataframe_as_json(self, pandas_df):
        return pandas_df.head(self.max_rows).to_json(orient="records")

    def _assert_input_is_pandas_dataframe(self):
        if not isinstance(self.input_var_value, pd.DataFrame):
            wrong_type =self.input_var_value.__class__.__name__
            raise exceptions.IllegalInputException(
                "{} is not a Pandas DataFrame! But {} instead.".format(
                    self.input_var_name, wrong_type
                )
            )


    
