from paddl.langs.mysql.definitions import CONSTRAINT_FOREIGN_KEY

VALID = """
CONSTRAINT symbol1 FOREIGN KEY bob (user_id) REFERENCES user (id)
"""


class TestConstraintForeignKey:
    def test_fk(self):
        result = CONSTRAINT_FOREIGN_KEY.parseString(VALID)
        # assert result.symbol == 'fk_bob'
        # assert result.index_name == 'index_namers'
        # assert result.col_names.asList[0] == 'user_id'
