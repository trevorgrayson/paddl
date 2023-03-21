from sys import stdin
from argparse import ArgumentParser

from . import extract_tables

parser = ArgumentParser(description="parse tables out of SQL statements")

sql = stdin.read()

tables = extract_tables(sql)
for table in tables:
    print(table)
