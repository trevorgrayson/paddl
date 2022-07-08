from pytest import fixture
from paddl.langs.mysql import CONSTRAINT_PRIMARY_KEY
from paddl import parse


class TestPrimaryKey:
    @fixture
    def const(self):
        return "CONSTRAINT blah PRIMARY KEY(id)"

    @fixture
    def pkey(self):
        return "PRIMARY KEY(`id`)"

    @fixture
    def ddl(self):
        return open("test/fixtures/primary-key.sql").read()

    def test_const(self, const):
        result = CONSTRAINT_PRIMARY_KEY.parseString(const)
        assert result[0] == "CONSTRAINT"

    def test_primary_key(self, pkey):
        result = CONSTRAINT_PRIMARY_KEY.parseString(pkey)
        assert result[0] == "PRIMARY KEY"
        assert result[2].asList() == ['id']

    def test_ddl(self, ddl):
        result = parse(ddl, engine='mysql')
        assert result

