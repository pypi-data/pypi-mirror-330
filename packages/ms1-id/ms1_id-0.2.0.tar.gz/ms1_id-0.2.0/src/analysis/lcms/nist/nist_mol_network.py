"""
compare mol. network w/ or w/o pseudo MS2
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
import networkx as nx


def dda_mn():
    # read feature table
    df = pd.read_csv(f'/data/nist/dda_ms2/aligned_feature_table.tsv',
                     sep='\t', low_memory=False)

    with open(f'data/nist_DDA_MS2.mgf', 'w') as f:
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Writing MGF"):
            if pd.notnull(row['MS2']):

                pms2 = row['MS2'].split('|')
                pms2 = [x.split(';') for x in pms2]
                pms2 = [[float(x) for x in y] for y in pms2]
                pms2 = np.array(pms2, dtype=np.float32)

                # remove ions larger than precursor
                pms2 = pms2[pms2[:, 0] < row['m/z'] + 0.1]

                mzs = pms2[:, 0]
                intensities = pms2[:, 1]

                f.write('BEGIN IONS\n')
                f.write(f'NAME={row["annotation"]}\n')
                f.write(f'PEPMASS={row["m/z"]}\n')
                f.write(f'RTINSECONDS={row["RT"] * 60}\n')
                f.write(f'SCANS={round(row["ID"])}\n')

                for mz, intensity in zip(mzs, intensities):
                    f.write(f'{mz} {intensity}\n')
                f.write('END IONS\n\n')


def pms2_mn(mode='fullscan_0ev'):
    # read feature table
    df = pd.read_csv(f'/Users/shipei/Documents/projects/ms1_id/data/nist/{mode}/aligned_feature_table.tsv',
                     sep='\t', low_memory=False)

    with open(f'data/nist_{mode}_pMS2.mgf', 'w') as f:
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Writing MGF"):
            if pd.notnull(row['pseudo_ms2']):

                pms2 = row['pseudo_ms2'].split(';')
                pms2 = [x.split(' ') for x in pms2][:-1]
                pms2 = [[float(x) for x in y] for y in pms2]
                pms2 = np.array(pms2, dtype=np.float32)

                # remove ions larger than precursor
                pms2 = pms2[pms2[:, 0] < row['m/z'] + 0.1]

                mzs = pms2[:, 0]
                intensities = pms2[:, 1]

                f.write('BEGIN IONS\n')
                f.write(f'NAME={row["MS1_annotation"]}\n')
                f.write(f'PEPMASS={row["m/z"]}\n')
                f.write(f'RTINSECONDS={row["RT"] * 60}\n')
                f.write(f'SCANS={round(row["ID"])}\n')

                for mz, intensity in zip(mzs, intensities):
                    f.write(f'{mz} {intensity}\n')
                f.write('END IONS\n\n')


def add_annotations_to_network_file():
    G = nx.read_graphml('data/mn/fullscan0ev_network.graphml')

    # read feature table
    dda_df = pd.read_csv(f'/data/nist/dda_ms2/aligned_feature_table.tsv',
                         sep='\t', low_memory=False)
    dda_df.loc[dda_df['similarity'] < 0.8, 'annotation'] = None

    ms1_df = pd.read_csv(f'/data/nist/fullscan_0ev/aligned_feature_table.tsv',
                         sep='\t', low_memory=False)
    ms1_df.loc[ms1_df['MS1_similarity'] < 0.8, 'MS1_annotation'] = None

    # Iterate through all nodes in the graph
    for node, data in G.nodes(data=True):
        mz = data['mz']
        rt = data['rt']

        # find in dda_df
        dda_row = dda_df[(dda_df['m/z'].between(mz-0.01, mz+0.01)) & (dda_df['RT'].between(rt-0.05, rt+0.05))]

        if len(dda_row) > 0:
            # sort by matched_score
            dda_row = dda_row.sort_values('similarity', ascending=False).iloc[0]
            data['DDA_feature'] = True

            # if annotated
            if not pd.isnull(dda_row['annotation']):
                data['MS2_annotation'] = dda_row['annotation']
                data['DDA_annotated'] = True
            else:
                data['MS2_annotation'] = ''
                data['DDA_annotated'] = False
        else:
            data['DDA_feature'] = False
            data['MS2_annotation'] = ''
            data['DDA_annotated'] = False

        # find in ms1_df
        ms1_row = ms1_df[(ms1_df['m/z'].between(mz-0.01, mz+0.01)) & (ms1_df['RT'].between(rt-0.05, rt+0.05))]
        if len(ms1_row) > 0:
            # sort by RT difference
            ms1_row['RT_diff'] = np.abs(ms1_row['RT'] - rt)
            ms1_row = ms1_row.sort_values('RT_diff', ascending=True).iloc[0]

            data['MS1_feature'] = True

            # if annotated
            if not pd.isnull(ms1_row['MS1_annotation']):
                data['MS1_annotation'] = ms1_row['MS1_annotation']
                data['MS1_annotated'] = True
            else:
                data['MS1_annotation'] = ''
                data['MS1_annotated'] = False
        else:
            data['MS1_feature'] = False
            data['MS1_annotation'] = ''
            data['MS1_annotated'] = False

    # Save the modified graph to a new GraphML file
    nx.write_graphml(G, 'data/mn/fullscan0ev_network_annotations.graphml')


if __name__ == '__main__':
    #########
    # generate mgf files for mol. network
    # dda_mn()
    # pms2_mn('fullscan_0ev')

    #########
    add_annotations_to_network_file()
