#!/usr/bin/env python
import click as ck
import pandas as pd
import gzip

@ck.command()
def main():
    nodes = {}
    with open('data/nodes.txt') as f:
        for line in f:
            p_id = line.strip()
            nodes[p_id] = 0.0
    df = pd.read_pickle('data/data_E11.pkl')
    patients = df['patients'].values
    for p_id in patients:
        fl = p_id[:2]
        in_file = f'data/scores/{fl}/{p_id}'
        out_file = f'{in_file}.nodes'
        nds = nodes.copy()
        with open(in_file) as f:
            for line in f:
                it = line.strip().split('\t')
                p_id, score = it[0], float(it[1])
                if p_id in nodes:
                    nds[p_id] = score
        with open(out_file, 'w') as f:
            for key, val in nds.items():
                f.write(f'{key}\t{val}\n')

     

if __name__ == '__main__':
    main()
