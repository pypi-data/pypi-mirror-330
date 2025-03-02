from pancham.database.database_search_manager import get_database_search
from pancham.data_frame_field import DataFrameField
from .field_parser import FieldParser

class DatabaseMatchFieldParser(FieldParser):
    """
    Map database fields

    Configuration:

    func:
        database_match:
            table_name: <Name of the table to search>
            search_column: <Name of the column to search>
            value_column: <Name of the column to find the value>
            search_cast: <Optional, str or int, set if we need to cast the search column>
            value_cast: <Optional, str or int, set if we need to cast the value column>

    :ivar FUNCTION_ID: Identifier for the 'database_match' function.
    :type FUNCTION_ID: str
    :ivar TABLE_NAME_KEY: Key used to extract the table name from the field properties.
    :type TABLE_NAME_KEY: str
    :ivar SEARCH_COLUMN_KEY: Key denoting the column in the table used for searching.
    :type SEARCH_COLUMN_KEY: str
    :ivar VALUE_COLUMN_KEY: Key denoting the column in the table used for value retrieval.
    :type VALUE_COLUMN_KEY: str
    :ivar SEARCH_CAST_VALUE_KEY: Key specifying the cast type for search column values.
    :type SEARCH_CAST_VALUE_KEY: str
    :ivar VALUE_CAST_VALUE_KEY: Key specifying the cast type for value column values.
    :type VALUE_CAST_VALUE_KEY: str
    """

    FUNCTION_ID = "database_match"
    TABLE_NAME_KEY = "table_name"
    SEARCH_COLUMN_KEY = "search_column"
    VALUE_COLUMN_KEY = "value_column"
    SEARCH_CAST_VALUE_KEY = "search_cast"
    VALUE_CAST_VALUE_KEY = "value_cast"
    FILTER_KEY = "filter"
    POPULATE_KEY = "populate"

    def can_parse_field(self, field: dict) -> bool:
        return self.has_function_key(field, self.FUNCTION_ID)

    def parse_field(self, field: dict) -> DataFrameField:
        properties = field[self.FUNCTION_KEY][self.FUNCTION_ID]

        if self.TABLE_NAME_KEY not in properties or self.SEARCH_COLUMN_KEY not in properties or self.VALUE_COLUMN_KEY not in properties:
            raise ValueError("Missing required properties for database_match function.")

        search_cast = properties.get(self.SEARCH_CAST_VALUE_KEY, None)
        value_cast = properties.get(self.VALUE_CAST_VALUE_KEY, None)
        filter_value = properties.get(self.FILTER_KEY, None)
        populate = properties.get(self.POPULATE_KEY, False)

        def map_value(data: dict) -> str:
            database_search = get_database_search(
                table_name=properties[self.TABLE_NAME_KEY],
                search_col=properties[self.SEARCH_COLUMN_KEY],
                value_col=properties[self.VALUE_COLUMN_KEY],
                cast_search=search_cast,
                cast_value=value_cast,
                filter=filter_value,
                populate=populate
            )

            search_value = data[properties[self.SOURCE_NAME_KEY]]

            return database_search.get_mapped_id(search_value)

        return self.build_func_field(
            field=field,
            func=map_value
        )

