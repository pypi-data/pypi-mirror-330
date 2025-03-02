import pandas as pd
from sqlalchemy import create_engine, Engine, MetaData
from typing_extensions import Literal

from pancham.pancham_configuration import PanchamConfiguration
from pancham.reporter import Reporter

META = MetaData()

class DatabaseEngine:

    def __init__(self, config: PanchamConfiguration, reporter: Reporter):
        self.config = config
        self.reporter = reporter
        self.__engine: Engine|None = None

    @property
    def engine(self) -> Engine:
        """
        Provides a method to initialize and return a database engine instance. If the engine
        does not already exist, it is created using the provided configuration for the
        database connection.

        :return: Database engine instance

        :rtype: Engine
        """
        if self.__engine is None:
            self.__engine = create_engine(self.config.database_connection)

        return self.__engine

    def write_df(self, data: pd.DataFrame, table_name: str, exists: Literal["replace", "append"] = 'append'):
        """
        Writes a pandas DataFrame to a database table using SQLAlchemy engine.

        The method allows for specifying whether the existing table should be replaced
        or appended with new data. The operation uses a connection from the SQLAlchemy
        engine and supports various backends as determined by the engine configuration.

        :param data: A pandas DataFrame containing the data to be written to the table.
        :type data: pd.DataFrame
        :param table_name: The name of the target table in the database.
        :type table_name: str
        :param exists: Specifies the behavior if the table already exists.
                       Possible values are "replace" to overwrite the table or
                       "append" to add data to the existing table.
        :type exists: Literal["replace", "append"]
        :return: None
        """
        if self.reporter:
            self.reporter.report_output(data, table_name)

        with self.engine.connect() as conn:
            data.to_sql(table_name, conn, if_exists=exists, index=False)

db_engine: DatabaseEngine|None = None

def initialize_db_engine(config: PanchamConfiguration, reporter: Reporter):
    """
    Initializes the database engine using the provided configuration and reporter.

    This function sets up the `db_engine` with the given `config` and `reporter`.
    It ensures the global database engine is initialized and ready to interact with
    the configured database.

    :param config: The configuration object used for database setup.
    :type config: PanchamConfiguration
    :param reporter: The reporter instance for logging or reporting database
        initialization details.
    :type reporter: Reporter
    :return: None
    :rtype: NoneType
    """
    global db_engine, META

    db_engine = DatabaseEngine(config, reporter)
    META = MetaData()

def get_db_engine() -> DatabaseEngine:
    """
    Retrieves the initialized database engine instance.

    This function returns a pre-initialized `DatabaseEngine` instance that
    is required for database operations. The function assumes that the
    database engine has already been configured and available; otherwise,
    it raises an error indicating the absence of the initialization.

    :raises ValueError: If the database engine has not been initialized.
    :return: The initialized database engine instance.
    :rtype: DatabaseEngine
    """
    global db_engine
    if db_engine is None:
        raise ValueError("Database engine not initialized")
    return db_engine
