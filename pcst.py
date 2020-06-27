#!/usr/bin/env python
import click as ck
import pandas as pd
import gzip
from pcst_fast import pcst_fast

@ck.command()
@ck.option('--in-file', '-i', help='Input scores file for patient')
@ck.option('--edge-cost', '-ec', default=0.9, help='Edge cost')
def main(in_file, edge_cost):
    nodes_to_ix = {}
    with open('data/nodes.txt') as f:
        for line in f:
            p_id = line.strip()
            nodes_to_ix[p_id] = len(nodes_to_ix)
    edges = []
    with open('data/edges.txt') as f:
        for line in f:
            it = line.strip().split('\t')
            edges.append((nodes_to_ix[it[0]], nodes_to_ix[it[1]]))
                         
    costs = [edge_cost] * len(edges)

    df = pd.read_pickle('data/data_E11.pkl')
    patients = df['patients'].values
    patient_vertices = []
    for p_id in patients:
        prizes = []
        in_file = f'data/scores/{p_id[:2]}/{p_id}.nodes'
        with open(in_file) as f:
            for line in f:
                it = line.strip().split('\t')
                prizes.append(float(it[1]))

        vertices, _ = pcst_fast(edges, prizes, costs, -1, 1, 'strong', 1)
        patient_vertices.append(vertices)
        print(len(vertices))
    df['pcst'] = patient_vertices
    df.to_pickle('data/data_E11_pcst.pkl')

if __name__ == '__main__':
    main()
