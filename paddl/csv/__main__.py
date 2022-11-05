from argparse import ArgumentParser

from . import render, farm

parser = ArgumentParser('csv2ddl')
parser.add_argument("filenames", nargs="+")

args = parser.parse_args()

for filename in args.filenames:
    table = farm(filename)
    print(render(table))
