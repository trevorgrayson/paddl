from pytest import fixture, mark
from paddl import parse, mysql, ColType
from paddl.langs.mysql.definitions import reference_definition, CONSTRAINT_FOREIGN_KEY


class TestMySQL:
    @fixture
    def ddl(self):
        return open('test/fixtures/references.sql').read()  #.replace("\n", ' ')

    @fixture
    def ref_def(self):
        "CONSTRAINT fk_stuff FOREIGN KEY (loan_no) "
        return "REFERENCES LOAN_DETAILS(loan_no)"

    @fixture
    def constraint(self):
        return "CONSTRAINT fk_stuff FOREIGN KEY (loan_no) " +\
            "REFERENCES LOAN_DETAILS(loan_no)"

    # def test_parse(self, ddl):
    #     schema = parse(ddl, engine='mysql')
    #     table = schema.tables[0]
    #     assert table.name == 'bob'
    #     assert len(table.columns) == 3
    #     assert table.columns[0].name == 'id'
    #     assert table.columns[0].type == ColType.INT
    #     assert table.columns[2].name == 'sam_id'

    def test_reference_definition(self, ref_def):
        result = reference_definition.parseString(ref_def)
        assert result.tbl_name == 'LOAN_DETAILS'
        assert result.key_part[0] == 'loan_no'
        assert len(result.key_part) == 1

    def test_constraint(self, constraint):
        result = CONSTRAINT_FOREIGN_KEY.parseString(constraint)
        assert result.symbol == 'fk_stuff'
        assert result.tbl_name == 'LOAN_DETAILS'
        assert result.key_part[0] == 'loan_no'
        assert len(result.key_part) == 1
