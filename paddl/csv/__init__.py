import csv
from os.path import basename
from paddl.models import Table, Schema, Column


def guess_type(string):
    if string.isdigit():
        return "INTEGER"
    try:
        float(string)
        return "DOUBLE"
    except Exception:
        pass
    return "STRING"


def cast(string):
    if string.isdigit():
        return int(string)
    try:
        return float(string)
    except Exception:
        pass
    return string


def farm(filename):
    table = Table(name=basename(filename).split(".")[0].upper())

    with open(filename, 'r') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            for k, v in row.items():
                k = k.replace(" ", "_")
                table.columns.append(
                    Column(name=k, type=guess_type(v))
                )
            break

    return table


def render(table: Table):
    out = f"CREATE TABLE {table.name} (\n"

    for col in table.columns:
        out += "\t" + "\t".join((col.name, col.type.value)) + ",\n"

    return out[:-2] + ");"


