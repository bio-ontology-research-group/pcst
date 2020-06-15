#!/usr/bin/env python
import click as ck
import pandas as pd
import gzip

@ck.command()
def main():
    inters = set()
    with gzip.open('data/9606.protein.links.v11.0.txt.gz') as f:
        next()
        for line in f:
            it = line.strip().split('\t')
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
