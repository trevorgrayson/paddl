def size(schema):
    total = 0
    for table in schema:
        for column in table:
            print(column.type)

    return total
