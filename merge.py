#!/usr/bin/env python
import click as ck
import pandas as pd
import gzip

@ck.command()
@ck.option('--in-file', '-i', help='Input scores file for patient')
def main(in_file):
    nodes = {}
    with open('data/nodes.txt') as f:
        for line in f:
            p_id = line.strip()
            nodes[p_id] = 0.0
    with open(in_file) as f:
        for line in f:
            it = line.strip().split('\t')
            p_id, score = it[0], float(it[1])
            if p_id in nodes:
                nodes[p_id] = score
    with open(in_file + '.nodes', 'w') as f:
        for key, val in nodes.items():
            f.write(f'{key}\t{val}\n')
            
     

if __name__ == '__main__':
    main()
