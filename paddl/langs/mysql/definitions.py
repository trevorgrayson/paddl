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


CONSTRAINT_symbol = Optional(CaselessKeyword("CONSTRAINT") +
                             TICK + Word(alphanums_)("symbol") + TICK
                             )  # TODO TICKS to symbol

index_option = ZeroOrMore(
        KEY_BLOCK_SIZE + Optional(Suppress('=')) + kbs_value
        # | Optional(index_type)
        # | WITH_PARSER + parser_name
        # | (COMMENT + Suppress("'") + _string + Suppress("'"))
        | VISIBLE | INVISIBLE
    # | ENGINE_ATTRIBUTE + Optional(Suppress('=')) + Suppress("'") + string + Suppress("'")
    # | SECONDARY_ENGINE_ATTRIBUTE + Optional(Suppress('=')) + Suppress("'") + string + Suppress("'")
)

# create_definition: {
#     col_name column_definition
#   | {INDEX | KEY} [index_name] [index_type] (key_part,...)
#       [index_option] ...
CONSTRAINT_KEY = ((INDEX | KEY) + Optional(index_name) +
                  Optional(index_type) + Suppress("(") + key_part___ + Suppress(")") +
                  index_option
                  )
#   | {FULLTEXT | SPATIAL} [INDEX | KEY] [index_name] (key_part,...)
#       [index_option] ...
#   | [CONSTRAINT [symbol]] PRIMARY KEY
#       [index_type] (key_part,...)
#       [index_option] ...
CONSTRAINT_PRIMARY_KEY = (
        CONSTRAINT_symbol + PRIMARY_KEY +
        Optional(index_type) + Suppress("(") + key_part___ + Suppress(")") +
        index_option
)
#   | [CONSTRAINT [symbol]] UNIQUE [INDEX | KEY]
#       [index_name] [index_type] (key_part,...)
#       [index_option] ...
CONSTRAINT_UNIQUE_KEY = (
    CONSTRAINT_symbol + UNIQUE + CONSTRAINT_KEY
)
#   | [CONSTRAINT [symbol]] FOREIGN KEY
#       [index_name] (col_name,...)
#       reference_definition
CONSTRAINT_FOREIGN_KEY = (
    CONSTRAINT_symbol +
    CaselessKeyword("FOREIGN KEY") + TICK + Optional(Word(alphanums_))("index_name") + TICK +
    Suppress("(") + OneOrMore(Group(TICK + Word(alphanums_) + TICK)) + Suppress(")") +
    reference_definition
)
#   | check_constraint_definition
# }


column_definition = MatchFirst((
    CONSTRAINT_FOREIGN_KEY,
    CONSTRAINT_PRIMARY_KEY,
    CONSTRAINT_UNIQUE_KEY,
    CONSTRAINT_KEY,
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
                    Word(alphanums_) + Optional("=" + Word(alphanums_+"'"+"\""))
                    # + Optional(",")
               )
table_options = ZeroOrMore(Group(table_option)("table_options"))  # Optional(Word(alphanums).ignore("=") + Word(alphanums))

partition_options = Optional(CaselessKeyword("PARITION"))