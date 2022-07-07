from pytest import fixture
from paddl.langs.mysql import column_definition


class TestColumnDefinition:
    @fixture
    def valid(self):
        return 'some_name INT(8)'

    @fixture
    def reference(self):
        return "CONSTRAINT fk_stuff FOREIGN KEY (loan_no) " +\
            "REFERENCES LOAN_DETAILS(loan_no)"

    @fixture
    def complex(self):
        return "`created` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)"

    def test_column(self, valid):
        result = column_definition.parseString(valid)
        assert result.data_type == 'INT'
        assert result.size == '8'

    def test_ref(self, reference):
        result = column_definition.parseString(reference)
        assert result

    def test_complex(self, complex):
        result = column_definition.parseString(complex)
        assert result.col_name == 'created'
