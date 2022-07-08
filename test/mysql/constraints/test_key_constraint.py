from pytest import fixture
from paddl.langs.mysql import CONSTRAINT_KEY as SUBJECT
from paddl import parse


class TestKeyConstraint:
    @fixture
    def index(self):
        return "KEY `source_id_foreign`(`source_id`)"

    @fixture
    def ddl(self):
        return open('test/fixtures/key.sql').read()

    def test_key(self, index):
        result = SUBJECT.parseString(index)
        type, name, cols = result.asList()

        assert type == 'KEY'
        assert name == 'source_id_foreign'
        assert cols == ['source_id']

    def test_ddl(self, ddl):
        result = parse(ddl)
        table = result.tables[0]
        constraint1 = table.constraints[0]

        assert len(table.constraints) == 4

        assert constraint1.reference == ['overdraft_id']
