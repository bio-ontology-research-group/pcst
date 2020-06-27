#!/usr/bin/env python
import click as ck
import pandas as pd
import gzip
from pcst_fast import pcst_fast

@ck.command()
@ck.option('--data-file', '-df', help='PCST result for a disease')
@ck.option('--genes-file', '-gf', help='list of genes associated with the disease')
def main(data_file, genes_file):
    df = pd.read_pickle(data_file)
    print(df['phenos'])
    print(df['pcst'])
    genes = set()
    with open(genes_file) as f:
        for line in f:
            genes.add(line.strip())
    with open('data/nodes.txt') as f:
        proteins = f.read().splitlines()
    gn_map = {}
    with open('data/gn_mapping.txt') as f:
        for line in f:
            it = line.strip().split('\t')
            gn_map[it[0]] = it[1]
    pos = 0
    neg = 0
    t_pos = 0
    t_neg = 0
    for row in df.itertuples():
        if 'E11' in row.phenos:
            t_pos += 1
            for it in row.pcst:
                p_id = proteins[it]
                if p_id in gn_map and gn_map[p_id] in genes:
                    pos+=1
                    break
        else:
            t_neg += 1
            for it in row.pcst:
                p_id = proteins[it]
                if p_id in gn_map and gn_map[p_id] in genes:
                    neg+=1
                    break
    print(f'{pos}/{t_pos} {neg}/{t_neg}')
            

if __name__ == '__main__':
    main()
