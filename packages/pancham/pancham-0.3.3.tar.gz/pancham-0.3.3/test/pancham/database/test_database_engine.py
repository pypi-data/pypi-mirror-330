import pandas as pd
import pytest

from sqlalchemy import MetaData, Table, Column, String

from database.database_engine import DatabaseEngine, get_db_engine, initialize_db_engine
from pancham.pancham_configuration import PanchamConfiguration
from pancham.reporter import PrintReporter


class MockConfig(PanchamConfiguration):

    @property
    def database_connection(self) -> str:
        return "sqlite:///:memory:"

class TestDatabaseEngine:

    def test_engine(self):
        config = MockConfig()
        db_engine = DatabaseEngine(config, PrintReporter())

        assert db_engine.engine is not None

    def test_engine_write_df(self):
        config = MockConfig()
        db_engine = DatabaseEngine(config, PrintReporter())
        meta = MetaData()
        customer = Table('customer', meta, Column("email", String))

        meta.create_all(db_engine.engine)

        data = pd.DataFrame({'email': ['a@example.com', 'b@example.com']})

        db_engine.write_df(data, 'customer')

    def test_get_db_engine(self):
        with pytest.raises(ValueError):
            get_db_engine()

    def test_db_init(self):
        initialize_db_engine(MockConfig(), PrintReporter())

        assert get_db_engine() is not None