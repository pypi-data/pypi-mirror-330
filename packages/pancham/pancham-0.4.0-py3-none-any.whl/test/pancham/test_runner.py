import datetime
import os

import pytest
from sqlalchemy import Table, MetaData, select, Integer, Column, DateTime, Boolean

from pancham.database.database_engine import get_db_engine, initialize_db_engine
from pancham.pancham_configuration import PanchamConfiguration
from pancham.runner import PanchamRunner
from pancham.reporter import PrintReporter


class Config(PanchamConfiguration):

    @property
    def database_connection(self) -> str:
        env_val = os.environ.get("PC_DB")
        print(f"Connection: {env_val}")
        if env_val is None:
            return "sqlite:///:memory:"

        return env_val

    @property
    def source_dir(self) -> str:
        return os.path.dirname(os.path.realpath(__file__)) + "/.."


class TestRunner:

    config_file = os.path.dirname(os.path.realpath(__file__)) + "/../example/order_configuration.yml"

    def test_runner(self):
        initialize_db_engine(Config(), PrintReporter())
        metadata = MetaData()
        Table('order', metadata, Column('Order', Integer), Column('Date', DateTime), Column('Sent', Boolean))
        metadata.create_all(get_db_engine().engine)

        runner = PanchamRunner(Config())
        runner.load_and_run(configuration_file=self.config_file)

        with get_db_engine().engine.connect() as conn:
            table = Table('order', MetaData(), autoload_with=conn)

            query = select(table.c['Order', 'Date', 'Sent'])
            result = conn.execute(query).fetchall()

            assert result[0][0] == 1
            assert result[0][1] == datetime.datetime(2024, 12, 22)
            assert result[0][2] is True

            assert result[1][0] == 2
            assert result[1][1] == datetime.datetime(2024, 12, 23)
            assert result[1][2] is False

