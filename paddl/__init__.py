import logging
from pyparsing.exceptions import ParseException
from enum import Enum
from .langs.mysql import definition as mysql
from .models import *
from .docs import plantuml as erd


class PaddlException(Exception):
    pass


class Language(Enum):
    MYSQL = 'mysql'


PARSERS = {
    Language.MYSQL: mysql
}


def clean(ddl):
    return ddl.replace('`', '')


def is_constraint(col):
    col = col.asList()
    return 'FOREIGN KEY' in col or \
           'PRIMARY KEY' in col or \
           'UNIQUE KEY' in col or \
           'KEY' in col


def cast_col_def(col):
    if is_constraint(col):
        return Constraint(*col)
    return Column(*col[0:3])


def table(result):
    """
    :param result: pyparse parseString result
    :return: paddl.Schema
    """
    columns = []
    constraints = []
    for col in result['columns']:
        column = cast_col_def(col)
        if isinstance(column, Column):
            columns.append(column)
        else:
            constraints.append(column)

    return Table(name=result['table_name'],
                 columns=columns,
                 constraints=constraints)


def parse(ddl, engine=Language.MYSQL, strict=False):
    """
    parse SQL DDLs and return Schema objects

    :param ddl: string
    :param engine: db engine, defaults to mysql
    :param strict: should parse strictly or fail
    :return:
    """
    engine = Language(engine)
    ddl = clean(ddl)
    schema = Schema()
    try:
        results = PARSERS[engine].parseString(ddl, parseAll=strict)
        logging.debug(results)
    except ParseException as ex:
        raise PaddlException(ex.args)\
            # (ex.msg, ex.pstr, ex.parser_element)

    schema.tables = [table(result) for result in results]
    return schema
