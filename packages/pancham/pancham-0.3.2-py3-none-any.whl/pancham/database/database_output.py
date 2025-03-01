import pandas as pd

from .database_engine import get_db_engine
from pancham.output_configuration import OutputConfiguration, OutputWriter

class DatabaseOutput(OutputConfiguration):

    def can_apply(self, configuration: dict):
        """
        Determines whether the provided configuration can be applied.

        This method validates if the configuration contains the necessary output
        settings for a database and ensures that all required fields are present.

        :param configuration: The configuration dictionary to validate.
                              It should include an 'output' key with a list of
                              output configurations.
        :type configuration: dict
        :return: Indicates whether the configuration can be applied.
        :rtype: bool
        :raises ValueError: If the 'database' output type is detected but the
                            required 'table' key is missing.
        """
        if not 'output' in configuration:
            return False

        db_config: dict | None = None

        for output in configuration['output']:
            if output['output_type'] == 'database':
                db_config = output
                break

        if db_config is None:
            return False

        if 'table' not in db_config:
            raise ValueError('table is required in database output configuration')

        return True

    def to_output_configuration(self, configuration: dict) -> dict:
        f"""
        Return the output configuration block for this object
       
        Will return:
            output_type: database
            table: Name of the table to write to
        
        :param configuration: 
        :return: 
        """
        for output in configuration['output']:
            if output['output_type'] == 'database':
                return output

        raise ValueError('Database configuration not set')

class DatabaseOutputWriter(OutputWriter):

    def write(self, data: pd.DataFrame, configuration: dict):
        if 'columns' in configuration:
            data = data[configuration['columns']]
        get_db_engine().write_df(data, configuration['table'])
