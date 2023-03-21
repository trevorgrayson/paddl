from pytest import fixture
from paddl.extract import extract_tables


class TestExtract:
    @fixture
    def sql(self):
        return """
        WITH bob (
            SELECT *
            FROM     
            APPLICATION.SCHEMA.TABLE
            LEFT JOIN ANOTHER_TABLE
        ),
        alice (
            SELECT * FROM WHATEVER
        ),
        mode (
            SELECT one, two, three
            FROM {{ @experiment }}
        )
        SELECT *
        FROM
            bob
        RIGHT JOIN alice
        """
    def test_extract_tables(self, sql):
        tables = extract_tables(sql)

        assert 'APPLICATION.SCHEMA.TABLE' in tables
        assert 'WHATEVER' in tables
        assert 'BOB' in tables
        assert 'ALICE' in tables
        assert '@EXPERIMENT' in tables

