from .output_manager import OutputManager
from .configuration.database_match_field_parser import DatabaseMatchFieldParser
from .configuration.datetime_field_parser import DateTimeFieldParser
from .configuration.remove_field_parser import RemoveFieldParser
from .configuration.database_fixed_field_parser import DatabaseFixedFieldParser
from .configuration.part_text_extractor_parser import PartTextExtractorParser
from .configuration.explode_field_parser import ExplodeFieldParser
from .configuration.split_field_parser import SplitFieldParser
from .configuration.database_multi_field_search_parser import DatabaseMultiFieldSearchParser
from .configuration.static_field_parser import StaticFieldParser
from .configuration.to_int_field_parser import ToIntFieldParser
from .configuration.field_parser import FieldParser
from .configuration.match_field_parser import MatchFieldParser
from .configuration.concat_field_parser import ConcatFieldParser
from .configuration.text_field_parser import TextFieldParser
from .data_frame_configuration import DataFrameConfiguration
from .data_frame_loader import DataFrameLoader
from .data_frame_configuration_loader import YamlDataFrameConfigurationLoader
from .database.database_engine import initialize_db_engine
from .database.sql_file_loader import SqlFileLoader
from .database.database_output import DatabaseOutput
from .file_loader import FileLoader, ExcelFileLoader, YamlFileLoader, CsvFileLoader
from .output_configuration import OutputWriter, OutputConfiguration
from .pancham_configuration import PanchamConfiguration
from .reporter import Reporter, PrintReporter

DEFAULT_LOADERS = {
    'xlsx': ExcelFileLoader(),
    'sql_file': SqlFileLoader(),
    'yaml': YamlFileLoader(),
    'csv': CsvFileLoader()
}
DEFAULT_REPORTER = PrintReporter()

DEFAULT_FIELD_PARSERS = [
    TextFieldParser(),
    MatchFieldParser(),
    DateTimeFieldParser(),
    ToIntFieldParser(),
    PartTextExtractorParser(),
    StaticFieldParser(),
    DatabaseMatchFieldParser(),
    DatabaseFixedFieldParser(),
    SplitFieldParser(),
    ExplodeFieldParser(),
    ConcatFieldParser(),
    DatabaseMultiFieldSearchParser(),
    RemoveFieldParser()
]
DEFAULT_OUTPUTS = [
    DatabaseOutput()
]

class PanchamRunner:

    def __init__(self,
                 pancham_configuration: PanchamConfiguration,
                 file_loaders: dict[str, FileLoader] | None = None,
                 outputs: dict[str, OutputWriter]|None = None,
                 reporter: Reporter | None = None,
                 field_parsers: list[FieldParser] | None = None,
                 outputs_configuration: list[OutputConfiguration] | None = None
                ):
        self.pancham_configuration = pancham_configuration
        self.loaded_outputs: dict[str, OutputWriter] = {}

        if outputs is None:
            self.outputs = OutputManager(pancham_configuration, {}, reporter)
        else:
            self.outputs = OutputManager(pancham_configuration, outputs, reporter)

        if file_loaders is None:
            self.file_loaders = DEFAULT_LOADERS
        else:
            self.file_loaders = file_loaders

        if reporter is None:
            self.reporter = DEFAULT_REPORTER
        else:
            self.reporter = reporter

        if field_parsers is None:
            self.field_parsers = DEFAULT_FIELD_PARSERS
        else:
            self.field_parsers = field_parsers

        if outputs_configuration is None:
            self.outputs_configuration = DEFAULT_OUTPUTS
        else:
            self.outputs_configuration = outputs_configuration

    def run_all(self):
        """
        Executes the primary function for processing all specified configurations.

        Summary:
        This method orchestrates the loading of configuration files, reporting their
        details, and executing an operation based on the loaded configuration. The
        process leverages a `YamlDataFrameConfigurationLoader` to parse and transform
        YAML-based configurations into usable formats. Each configuration file is
        subsequently passed to a reporter for documentation purposes, and then
        handled via the `run()` method.

        :param self: Represents the instance of the class.
        :raises Exception: An error raised if any configuration file fails to load
            or process accordingly.
        :return: None
        """
        configuration_loader = YamlDataFrameConfigurationLoader(field_parsers=self.field_parsers, output_configuration=self.outputs_configuration)
        loaders = list(map(lambda f: configuration_loader.load(f), self.pancham_configuration.mapping_files))

        for l in loaders:
            self.reporter.report_configuration(l)
            self.run(l)

            # completed = []
            #
            # def start_migration(configuration_file: DataFrameConfiguration):
            #     for dep in configuration_file.depends_on:
            #         dep_completed = False
            #
            #         while not dep_completed:
            #             if dep in completed:
            #                 dep_completed = True
            #             else:
            #                 asyncio.sleep(20)
            #
            #     self.run(configuration_file)
            #     completed.append(configuration_file.name)
            #
            # configuration_loader = YamlDataFrameConfigurationLoader(field_parsers=self.field_parsers, output_configuration=self.outputs_configuration)
            # loaders = list(map(lambda f: configuration_loader.load(f), self.pancham_configuration.mapping_files))
            #
            # asyncio.gather(*list(map(lambda f: start_migration(f), loaders)))


    def load_and_run(self, configuration_file: str):
        configuration_loader = YamlDataFrameConfigurationLoader(field_parsers=self.field_parsers, output_configuration=self.outputs_configuration)
        configuration = configuration_loader.load(configuration_file)

        self.reporter.report_configuration(configuration)

        self.run(configuration)

    def run(self, configuration: DataFrameConfiguration):
        """
        Executes the data loading and writing process based on the provided configuration.

        The method initializes a DataFrameLoader with the given file loaders and
        reporter, then uses it to load data as specified in the input configuration.
        Once the data is loaded, it iterates over the output specifications defined
        in the configuration and writes the data to each output destination by obtaining
        the appropriate writer.

        :param configuration: Configuration object defining how the data will be
            loaded and written. This includes input details for loading the data
            and output specifications for writing the data.
        :type configuration: DataFrameConfiguration

        :return: None
        """
        initialize_db_engine(self.pancham_configuration, self.reporter)
        loader = DataFrameLoader(self.file_loaders, self.reporter, self.pancham_configuration)
        data = loader.load(configuration)

        self.outputs.write_output(data.processed, configuration)

        for post_run_configuration in configuration.post_run_configuration:
            input_data = data.get_required_dataframe(post_run_configuration.merge_configuration)
            post_run_data = loader.process_dataframe(input_data, post_run_configuration)

            self.outputs.write_output(post_run_data, post_run_configuration)

