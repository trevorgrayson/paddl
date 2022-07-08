from .definitions import *
from .keywords import *
from .keywords import _

NOT_CREATE_STATEMENT = Word(alphas)


CREATE_STMT = (
    CREATE + TEMPORARY + TABLE + IF_NOT_EXISTS + table_name +
    create_definition +
    table_options +
    partition_options +
    Optional(Suppress(";"))
)

definition = OneOrMore(Group(CREATE_STMT))
