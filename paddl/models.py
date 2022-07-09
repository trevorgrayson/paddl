from enum import Enum
from avro.schema import PrimitiveSchema
from pyparsing import ParseResults


class ColType(Enum):
    STRING = "string"
    VARCHAR = "varchar"
    TEXT = 'text'
    CHAR = "char"
    INT = 'int'
    DECIMAL = 'decimal'
    DATETIME = 'datetime'
    DATE = 'date'
    NULL = 'null'
    TIMESTAMP = 'timestamp'
    TIME = 'time'
    BIGINT = 'bigint'
    CURRENT_TIMESTAMP = 'current_timestamp'
    ENUM = 'enum'


class Schema:
    """An analog for a database"""
    def __init__(self, name=None, description=None,
                 **kwargs):
        self.name = name
        self.description = description
        self.tables = [Table(**kw)
                       if isinstance(kw, dict) else kw
                       for kw in kwargs.get('tables', [])]


class Table:
    """A table or collection of records"""
    def __init__(self, name=None, columns=None, description='', **kwargs):
        if columns is None:
            columns = []
        self.name = name
        self.description = description
        self.table_options = kwargs.get('table_options')
        self.columns = [Column(**col)
                        if isinstance(col, dict) else col
                        for col in columns]
        self.constraints = [Constraint(**col)
                            if isinstance(col, dict) else col
                            for col in kwargs.get("constraints", [])]


class Constraint:
    def __init__(self, *args):
        self.symbol = None
        self.index_name = None
        self.key = None
        self.reference = None
        self.ref_table = None
        self.ref_columns = []
        if args[0] == 'CONSTRAINT':  # parse `symbol` if present
            self.symbol = args[1]
            args = args[2:]
        key_type = args[0]

        if key_type in ("PRIMARY KEY", "UNIQUE KEY", "KEY"):
            self.reference=args[-1].asList()
            if len(args) >= 3:
                self.index_name = args[1]
            return
        if args[0] == 'UNIQUE':
            args = args[1:]
        args = args[1:]  # shift 'FOREIGN KEY' off
        if 'REFERENCES' in args:
            refs = args[-3:]
            args = args [:-3]
            self.ref_table = refs[1]
            self.ref_columns = refs[2].asList()
        if len(args) >= 2:
            self.ref_columns = args[1].asList()
        self.key = args[0]  # .asList()

    def __repr__(self):
        return "Constraint: " + " ".join(map(str, (
            self.symbol, self.index_name, self.key,
            self.reference, self.ref_table, self.ref_columns
        )))


class Column:
    """Atomic unit of data."""
    def __init__(self, name=None, type=None, description='', **kwargs):
        self.name = name
        self.description = description
        if isinstance(type, PrimitiveSchema):
            self.type = type.type
        elif isinstance(type, ParseResults):
            self.name = type.col_name
            self.type = type.data_type[0]
        self.type = ColType(type.lower())
