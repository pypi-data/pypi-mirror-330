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

    df.to_csv('data/workbench_db.tsv', sep='\t', index=False)


def add_inchikey_to_workbench_results():

    df = pd.read_csv('/data/PR000639/metadata/workbench_identifications.tsv',
                     sep='\t', low_memory=False)

    meta = pd.read_csv('data/workbench_db.tsv', sep='\t', low_memory=False)

    # dict from name to inchikey
    name_to_inchikey = dict(zip(meta['name'], meta['inchi_key']))

    # add inchikey to df
    df['inchikey'] = df['refmet_name'].map(name_to_inchikey)

    df.to_csv('data/workbench_identifications_with_inchikey.tsv', sep='\t', index=False)


if __name__ == '__main__':
    load_workbench_df()

    add_inchikey_to_workbench_results()
