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
    def __init__(self, symbol=None, reference=None,
                 ref_table=None, ref_columns=None, *args):
        if ref_columns == None:
            ref_columns = []

        self.symbol = symbol
        self.reference = reference
        self.ref_table= ref_table
        self.ref_columns = ref_columns


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
