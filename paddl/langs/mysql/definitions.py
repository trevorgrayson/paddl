from pyparsing import (
    ZeroOrMore, alphas, Suppress
)
from .keywords import *


def COMMENT(string):
    return Optional(CaselessKeyword("COMMENT") + string)


reference_definition = (
    REFERENCES + TICK + tbl_name + TICK +
    Suppress("(") + key_part___ + Suppress(")")
    # Optional(MatchFirst([MATCH_FULL, MATCH_PARTIAL, MATCH_SIMPLE]))
    # ON_DELETE reference_option
    # ON_UPDATE reference_option
)
# column_definition: {
column_definition = MatchFirst((
    # data_type [NOT NULL | NULL] [DEFAULT {literal | (expr)} ]
    data_type + (NULLY | DEFAULT),
    # [VISIBLE | INVISIBLE]
    # [AUTO_INCREMENT] [UNIQUE [KEY]] [[PRIMARY] KEY]
    # [COMMENT 'string']
    # [COLLATE collation_name]
    # [COLUMN_FORMAT {FIXED | DYNAMIC | DEFAULT}]
    # [ENGINE_ATTRIBUTE [=] 'string']
    # [SECONDARY_ENGINE_ATTRIBUTE [=] 'string']
    # [STORAGE {DISK | MEMORY}]
    # [reference_definition]
    # [check_constraint_definition]
    # | data_type
    data_type +\
    # [COLLATE collation_name]
    # [GENERATED ALWAYS] AS (expr)
    # [VIRTUAL | STORED] [NOT NULL | NULL]
    # [VISIBLE | INVISIBLE]
    # [UNIQUE [KEY]] [[PRIMARY] KEY]
    # [COMMENT 'string']
    COMMENT(string) +\
    # [reference_definition]
    reference_definition
    # [check_constraint_definition]
    # }
))




# create_definition: {
#     col_name column_definition
#   | {INDEX | KEY} [index_name] [index_type] (key_part,...)
#       [index_option] ...
#   | {FULLTEXT | SPATIAL} [INDEX | KEY] [index_name] (key_part,...)
#       [index_option] ...
#   | [CONSTRAINT [symbol]] PRIMARY KEY
#       [index_type] (key_part,...)
#       [index_option] ...
#   | [CONSTRAINT [symbol]] UNIQUE [INDEX | KEY]
#       [index_name] [index_type] (key_part,...)
#       [index_option] ...
#   | [CONSTRAINT [symbol]] FOREIGN KEY
#       [index_name] (col_name,...)
#       reference_definition

CONSTRAINT_symbol = Optional(CaselessKeyword("CONSTRAINT") +
         TICK + Word(alphanums_)("symbol")) + TICK

index_type = Word(alphanums_)

kbs_value = Word(nums)
parser_name = Word(alphanums_)
KEY_BLOCK_SIZE = CaselessKeyword("KEY_BLOCK_SIZE")
WITH_PARSER = CaselessKeyword("WITH PARSER")
VISIBLE = CaselessKeyword("VISIBLE")
INVISIBLE = CaselessKeyword("INVISIBLE")
ENGINE_ATTRIBUTE = CaselessKeyword("ENGINE_ATTRIBUTE")
SECONDARY_ENGINE_ATTRIBUTE = CaselessKeyword("SECONDARY_ENGINE_ATTRIBUTE")

_string = Word(alphanums_)("_string")
index_option = (
                KEY_BLOCK_SIZE + Optional(Suppress('=')) + kbs_value
                | index_type
                | WITH_PARSER + parser_name
                # | (COMMENT + Suppress("'") + _string + Suppress("'"))
                | VISIBLE | INVISIBLE
                # | ENGINE_ATTRIBUTE + Optional(Suppress('=')) + Suppress("'") + string + Suppress("'")
                # | SECONDARY_ENGINE_ATTRIBUTE + Optional(Suppress('=')) + Suppress("'") + string + Suppress("'")
                )
CONSTRAINT_PRIMARY_KEY = (
   Optional(index_type) + "(" + key_part___ + ")" +
   index_option
)

CONSTRAINT_FOREIGN_KEY = (
    CONSTRAINT_symbol +
    CaselessKeyword("FOREIGN KEY") + Optional(Word(alphanums_))("index_name") +
    Suppress("(") + OneOrMore(Group(TICK + Word(alphanums_) + TICK)) + Suppress(")") +
    reference_definition
)
#   | check_constraint_definition
# }


column_definition = MatchFirst((
    CONSTRAINT_FOREIGN_KEY,  # FK first for specificity
    col_name + data_type + (NULLY & DEFAULT & ON_UPDATE),
))

# should be able to mix up order of rows
create_definition = Suppress('(') + \
                    OneOrMore(Group(
                        column_definition.ignore(',')
                    ))("columns") + \
                    Suppress(')')
# ZeroOrMore(CONSTRAINT_FOREIGN_KEY)("fks") + \

table_option = (
                    Word(alphanums_) + "=" +
                    Word(alphanums_+"'"+"\"") + Optional(",")
               ) | Word(alphanums_)
table_options = ZeroOrMore(Group(table_option)("table_options"))  # Optional(Word(alphanums).ignore("=") + Word(alphanums))

partition_options = Optional(CaselessKeyword("PARITION"))