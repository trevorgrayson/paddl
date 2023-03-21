PRE_TABLE_TOKENS = (
    'FROM', 'JOIN'
)


def extract_tables(sql: str):
    """
    Return table names in a SQL statement.

    Will find first token after `FROM` and `JOIN`

    :param sql:
    :return:
    """
    tables = []

    # remove comment lines
    sql = " ".join(filter(lambda line: not line.startswith('--'),
                          sql.split('\n')))
    tokens = sql.upper().split()

    for ii in range(len(tokens)):
        if tokens[ii] in PRE_TABLE_TOKENS:
            nxt = tokens[ii+1]
            if nxt == '{{':
                tables.append(tokens[ii + 2])
            elif nxt.startswith('{{'):
                tables.append(tokens[ii + 1])
            else:
                tables.append(tokens[ii + 1])

    return tables
