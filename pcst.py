#!/usr/bin/env python
import click as ck
import pandas as pd
import gzip
from pcst_fast import pcst_fast

@ck.command()
@ck.option('--in-file', '-i', help='Input scores file for patient')
def main(in_file):
    prizes = []
    nodes_to_ix = {}
    with open(in_file) as f:
        for line in f:
            it = line.strip().split('\t')
            prizes.append(float(it[1]))
            nodes_to_ix[it[0]] = len(nodes_to_ix)
    edges = []
    with open('data/edges.txt') as f:
        for line in f:
            it = line.strip().split('\t')
            edges.append((nodes_to_ix[it[0]], nodes_to_ix[it[1]]))
                         
    costs = [0.5] * len(edges)

    vertices, edges = pcst_fast(edges, prizes, costs, -1, 1, 'strong', 1)
    print(len(vertices))
     

if __name__ == '__main__':
    main()
