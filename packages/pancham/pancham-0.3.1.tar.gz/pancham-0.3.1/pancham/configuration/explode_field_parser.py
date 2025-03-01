from pancham.data_frame_field import DataFrameField
from .field_parser import FieldParser

class ExplodeFieldParser(FieldParser):
    """
    This class is a specialized FieldParser implementation for processing fields that
    contain an "explode" function. Its primary purpose is to handle and parse field definitions
    where the data transformation involves the "explode" functionality, extracting nested
    information into individual rows.

    This class can determine if a field can be processed based on the presence of the
    "explode" function key and provides the ability to parse these fields into `DataFrameField`
    objects with the required transformation logic.

    :ivar FUNCTION_ID: The unique identifier for the "explode" function.
    :type FUNCTION_ID: str
    """

    FUNCTION_ID = "explode"

    def can_parse_field(self, field: dict) -> bool:
        return self.has_function_key(field, self.FUNCTION_ID)

    def parse_field(self, field: dict) -> DataFrameField:
        properties = field[self.FUNCTION_KEY][self.FUNCTION_ID]

        return DataFrameField(
            name = field['name'],
            field_type=field[self.FIELD_TYPE_KEY],
            nullable=self.is_nullable(field),
            source_name=self.get_source_name(field),
            df_func=lambda d: d.explode(properties[self.SOURCE_NAME_KEY]),
        )