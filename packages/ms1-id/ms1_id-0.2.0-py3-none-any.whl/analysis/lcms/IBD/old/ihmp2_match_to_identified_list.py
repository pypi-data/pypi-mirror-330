import pandas as pd
from tqdm import tqdm

import json


def load_workbench_df():

    with open('/data/PR000639/metadata/workbench_db/all', 'r') as file:
        data = json.load(file)

    # convert the data to a list of dictionaries
    rows = [value for key, value in data.items()]

    df = pd.DataFrame(rows)

    print(df.head())

    df.to_csv('workbench_db.tsv', sep='\t', index=False)


def add_inchikey_to_workbench_results():

    df = pd.read_csv('/data/PR000639/metadata/workbench_identifications.tsv',
                     sep='\t', low_memory=False)

    meta = pd.read_csv('workbench_db.tsv', sep='\t', low_memory=False)

    # dict from name to inchikey
    name_to_inchikey = dict(zip(meta['name'], meta['inchi_key']))

    # add inchikey to df
    df['inchikey'] = df['refmet_name'].map(name_to_inchikey)

    df.to_csv('workbench_identifications_with_inchikey.tsv', sep='\t', index=False)


def filter_stats_df():
    df = pd.read_csv('all_modes_statistical_analysis.tsv', sep='\t', low_memory=False)
    print(f"Original shape: {df.shape}")

    # remove all cols starting with 'PREF' (pool reference mixture)
    df = df.loc[:, ~df.columns.str.startswith('PREF')]

    # filter out rows with score and matched peaks
    df = df[(df['MS1_similarity'] >= 0.80) & (df['MS1_matched_peak'] >= 6)].reset_index(drop=True)

    # sort by MS1 inchikey, then by MS1_similarity
    df = df.sort_values(['MS1_inchikey', 'MS1_similarity'], ascending=[True, False]).reset_index(drop=True)

    # remove duplicated MS1 inchikey
    df = df.drop_duplicates('MS1_inchikey', keep='first').reset_index(drop=True)

    ########################################################
    # remove rows which show up in the workbench results
    workbench_df = pd.read_csv('workbench_identifications_with_inchikey.tsv', sep='\t', low_memory=False)
    workbench_inchikeys = workbench_df['inchikey'].tolist()
    df = df[~df['MS1_inchikey'].isin(workbench_inchikeys)].reset_index(drop=True)

    ########################################################
    # filter rows by corrected p values
    df = df[(df['nonIBD_vs_CD_p_value_corrected'] <= 0.05) | (df['nonIBD_vs_UC_p_value_corrected'] <= 0.05)].reset_index(drop=True)

    ########################################################
    # filter rows by fill_percentage
    df = df[df['fill_percentage'] >= 0.25].reset_index(drop=True)

    print(f"Filtered shape: {df.shape}")
    df.to_csv('filtered_statistical_analysis.tsv', sep='\t', index=False)


if __name__ == '__main__':
    # load_workbench_df()

    # add_inchikey_to_workbench_results()

    filter_stats_df()

    # manual selection: filtered_statistical_analysis_manual.tsv



