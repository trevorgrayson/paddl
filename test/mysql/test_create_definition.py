from paddl.langs.mysql import create_definition

VALID = """
(
name VARCHAR(255),
email CHAR(256),
CONSTRAINT symbol1 FOREIGN KEY bob (user_id) REFERENCES user (id)
)
"""


class TestCreateDefinition:
    def test_column(self):
        result = create_definition.parseString(VALID)
        assert result.columns[0].col_name == 'name'
        assert result.columns[0].data_type == 'VARCHAR'
        assert result.columns[0].size == '255'

        assert result.columns[1].col_name == 'email'
        assert result.columns[1].data_type == 'CHAR'
        assert result.columns[1].size == '256'

        # assert result.columns[2][1].index_name == 'bob'
        # assert result.columns[2][1].tbl_name == 'user'
        # assert result.columns[2][1].col_names.asList() == ['user_id']
        # assert result.columns[2][1].key_part.asList() == ['id']
