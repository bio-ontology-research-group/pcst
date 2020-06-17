#!/usr/bin/env python
import click as ck
import pandas as pd
import gzip
import os

@ck.command()
def main():
    #edges()
    #return
    mapping = {}
    with open('data/gn_mapping.txt') as f:
        for line in f:
            it = line.strip().split('\t')
            p_id, gn = it[0], it[1]
            if gn not in mapping:
                mapping[gn] = []
            mapping[gn].append(p_id)
    df = pd.read_pickle('data/data_E11.pkl')
    patients = set(df['patients'].values)
    chrs = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
        '21', '22', 'X', 'Y']
    data = {}
    for chrom in chrs:
        with gzip.open(f'data/vars/{chrom}.txt.gz', 'rt') as f:
            for line in f:
                it = line.strip().split('\t')
                gene = it[0]
                if gene not in mapping:
                    continue
                gene = mapping[gene]
                score = 1 - float(it[3])
                pats = set(it[4].split('#')).intersection(patients)
                for p_id in pats:
                    if p_id not in data:
                        data[p_id] = []
                    data[p_id].append((gene, score))
    for p_id, values in data.items():
        fl = p_id[:2]
        if not os.path.exists(f'data/scores/{fl}'):
            os.makedirs(f'data/scores/{fl}')
        with open(f'data/scores/{fl}/{p_id}', 'w') as f:
            for gene, score in values:
                for g_id in gene:
                    f.write(f'{g_id}\t{score:.3f}\n')
        

def edges():
    inters = set()
    with gzip.open('data/9606.protein.links.v11.0.txt.gz', 'rt') as f:
        next(f)
        for line in f:
            it = line.strip().split()
            score = int(it[2])
            if score < 700:
                continue
            p1 = it[0]
            p2 = it[1]
            if p1 > p2:
                t = p1
                p1 = p2
                p2 = t
            inters.add((p1, p2))
    with open('data/edges.txt', 'w') as f:
        for p1, p2 in inters:
            f.write(f'{p1}\t{p2}\n')
    
     

if __name__ == '__main__':
    main()
