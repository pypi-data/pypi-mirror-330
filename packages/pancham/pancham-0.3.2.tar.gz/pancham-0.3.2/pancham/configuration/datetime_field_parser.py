import datetime
import pandas as pd
from .field_parser import FieldParser
from pancham.data_frame_field import DataFrameField

class DateTimeFieldParser(FieldParser):

    FUNCTION_ID = "datetime"

    def can_parse_field(self, field: dict) -> bool:
        return self.has_function_key(field, self.FUNCTION_ID)

    def parse_field(self, field: dict) -> DataFrameField:
        format = '%d/%m/%Y'

        if type(field[self.FUNCTION_KEY][self.FUNCTION_ID]) is dict:
            format = field[self.FUNCTION_KEY][self.FUNCTION_ID].get('format', '%d/%m/%Y')

        return DataFrameField(
            name = field['name'],
            field_type=datetime.datetime,
            nullable=self.is_nullable(field),
            source_name=None,
            func=lambda x: pd.to_datetime(x[self.get_source_name(field)], format=format)
        )