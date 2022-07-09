from pytest import fixture
from paddl import parse
from paddl.langs.mysql import CONSTRAINT_UNIQUE_KEY


class TestUniqueKey:
    @fixture
    def unique(self):
        return "UNIQUE KEY `account_dave_user_id_unique`(`dave_user_id`)"

    @fixture
    def ddl(self):
        return open("test/fixtures/unique-key.sql").read()

    def test_unique(self, unique):
        result = CONSTRAINT_UNIQUE_KEY.parseString(unique)
        assert result[2] == 'account_dave_user_id_unique'
        assert result[3][0] == 'dave_user_id'

    def test_ddl(self, ddl):
        schema = parse(ddl)
        table = schema.tables[0]
        assert len(table.constraints) == 3