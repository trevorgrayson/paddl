from pytest import fixture
from paddl.langs.mysql import table_option, table_options


class TestTableOptions:
    @fixture
    def overdraft(self):
        return "ENGINE=InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci"

    def test_table_option(self):
        result = table_option.parseString("ENGINE = InnoDB")
        assert result[0] == "ENGINE"
        assert result[2] == "InnoDB"

    def test_table_option_keyword(self):
        result = table_option.parseString("DEFAULT")
        assert result[0] == "DEFAULT"

    def test_table_options(self, overdraft):
        result = table_options.parseString(overdraft)
        assert result[0][0] == 'ENGINE'
        assert result[1][0] == 'DEFAULT'
        assert result[3][0] == 'COLLATE'
        assert result[3][2] == 'utf8mb4_0900_ai_ci'

        assert len(result) == 4
