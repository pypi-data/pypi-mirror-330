import yaml

from .data_frame_configuration import MergeConfiguration
from .configuration.field_parser import FieldParser
from .data_frame_configuration import DataFrameConfiguration
from .output_configuration import OutputConfiguration

class DataFrameConfigurationLoader:

    def __init__(self, field_parsers: list[FieldParser], output_configuration: list[OutputConfiguration]):
        self.field_parsers = field_parsers
        self.output_configuration = output_configuration

    def load(self, filename: str) -> DataFrameConfiguration:

        data = self.load_file(filename)
        sheet: str|None = None
        key: str|None = None

        if "file_path" not in data or "file_type" not in data:
            raise ValueError(f"file_path and file_type are required fields in {filename}")

        if data["file_type"] == "xlsx" and "sheet" in data:
            sheet = data["sheet"]

        if data['file_type'] == 'yaml' and 'key' in data:
            key = data['key']

        configuration = self.__load_section(data, "main", sheet=sheet, key=key)
        if "pre" in data:
            for d in data["pre"]:
                configuration.pre_run_configuration.append(self.__load_section(d, d['name']))

        if "post" in data:
            for d in data["post"]:
                configuration.post_run_configuration.append(self.__load_section(d, d['name']))

        return configuration

    def load_file(self, filename: str) -> dict:
        """
        Loads the content of a given file and returns the data as a dictionary. The file
        is typically expected to contain structured data in a format such as JSON or YAML.

        :param filename: Name of the file to be loaded. The file should exist at the
            specified path and must be readable.
        :type filename: str

        :return: A dictionary containing the data loaded from the file.
        :rtype: dict
        """
        pass

    def __load_section(self, data: dict, label: str, sheet: str|None = None, key: str|None = None) -> DataFrameConfiguration:
        """
        Dataframes are loaded in sections, allowing the pre and post steps to be their own configuration that
        is loaded using the same methods

        :param data: A dictionary containing configuration data needed for defining the DataFrame
            and its associated fields. Must include a "file_path" and "file_type" for "main" label or
            nested label-specific details when not "main".
        :type data: dict
        :param label: A string indicating the label for the section to process. Allows identifying
            the required part of the input data.
        :type label: str
        :param sheet: Optional sheet identifier for file-based input if relevant (e.g., Excel files).
            Determines a particular sheet to pull data from when parsing input.
        :type sheet: str | None
        :return: A configured `DataFrameConfiguration` object instantiated based on input_data and label,
            populated with fields parsed by supported parsers, and associated output configurations if specified
            and applicable.
        :rtype: DataFrameConfiguration
        :raises ValueError: If a field in the input data cannot be parsed by any available field parser.
        """
        configuration = self.__load_base_configuration(data, label, sheet=sheet, key=key)

        for f in data['fields']:
            has_parsed = False
            for parser in self.field_parsers:
                if parser.can_parse_field(f):
                    field = parser.parse_field(f)
                    configuration.add_field(data_frame_field=field)
                    has_parsed = True
                    break

            if not has_parsed:
                raise ValueError(f"Could not parse field {f}")

        if 'output' in data:
            for c in self.output_configuration:
                if c.can_apply(data):
                    configuration.add_output(c.to_output_configuration(data))

        return configuration

    def __load_base_configuration(self, data: dict, label: str, sheet: str|None = None, key: str|None = None) -> DataFrameConfiguration:
        """
        Load the base configuration for a DataFrame. Depending on the label, it initializes
        the appropriate DataFrameConfiguration object using the passed parameters. When
        the label is 'main', it utilizes the file-related data for configuration; for other
        labels, it evaluates additional merge configurations if provided.

        :param data: A dictionary containing input data configuration. It may include keys
                     like 'file_path', 'file_type', 'name', and 'depends_on' for defining
                     the DataFrame structure, as well as an optional 'merge' key which must
                     contain sub-keys if merge configuration is required.
        :param label: A string identifying the label of the configuration. It dictates
                      the configuration behavior, particularly whether merge configurations
                      are applicable or not.
        :param sheet: An optional string denoting the sheet name for configurations related
                      to spreadsheet files.
        :param key: An optional string representing the unique key identifier relevant to
                    the configuration.
        :return: A DataFrameConfiguration object initialized based on the provided
                 configuration data and label.
        """
        if label == 'main':
            return DataFrameConfiguration(data["file_path"], data["file_type"], name=data['name'], sheet=sheet, key=key, depends_on=data.get('depends_on', None))

        merge_configuration = None
        if 'merge' in data:
            merge_dict = data['merge']
            merge_configuration = MergeConfiguration(merge_dict.get('type', 'processed'), merge_dict.get('source_key', None), merge_dict.get('processed_key', None))
        return DataFrameConfiguration(label, label, name=data['name'], merge_configuration=merge_configuration)


class YamlDataFrameConfigurationLoader(DataFrameConfigurationLoader):

    def load_file(self, filename: str) -> dict:
        """
        Loads data from a YAML file and returns it as a dictionary.

        The method attempts to open the specified file in read mode and parse its
        content using the YAML-safe loader. The retrieved data is then returned to
        the caller as a dictionary.

        :param filename: The name of the YAML file to load.
        :type filename: str

        :return: A dictionary containing the parsed YAML file data.
        :rtype: dict
        """
        with open(filename, 'r') as file:
            return yaml.safe_load(file)