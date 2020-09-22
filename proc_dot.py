#!/bin/python

import pydot
import sys


def proc_dot(dot_file: str, png_file: str):
    (graph,) = pydot.graph_from_dot_file(dot_file)
    graph.write_png(png_file)
    return


if __name__ == '__main__':
    dot_file = sys.argv[1]
    png_file = sys.argv[2]
    proc_dot(dot_file, png_file)
