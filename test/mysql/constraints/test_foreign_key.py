from pytest import fixture
from paddl import parse
from paddl.langs.mysql.definitions import CONSTRAINT_FOREIGN_KEY

VALID = """
CONSTRAINT symbol1 FOREIGN KEY bob (user_id) REFERENCES user (id)
"""


class TestConstraintForeignKey:
    @fixture
    def long(self):
        return open('test/fixtures/long-key.sql').read()

    def test_fk(self):
        result = CONSTRAINT_FOREIGN_KEY.parseString(VALID)
        # assert result.symbol == 'fk_bob'
        # assert result.index_name == 'index_namers'
        # assert result.col_names.asList[0] == 'user_id'

    def test_long(self, long):
        schema = parse(long)
        table = schema.tables[0]
        constraint = table.constraints[0]

        assert constraint.symbol == 'adjustment_adjustment_source_id_foreign'
        assert constraint.key[0] == 'adjustment_source_id'
        assert constraint.ref_table == 'adjustment_source'
        assert constraint.ref_columns == ['id']
        #   CONSTRAINT `adjustment_adjustment_source_id_foreign` FOREIGN KEY (`adjustment_source_id`) REFERENCES `adjustment_source` (`id`)
