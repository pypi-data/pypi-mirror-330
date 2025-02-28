import pandas as pd
import os


def find_derep_tsv_files(folder):
    derep_tsv_files = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('_derep.tsv'):
                full_path = os.path.join(root, file)
                derep_tsv_files.append(full_path)

    return derep_tsv_files


def merge(folder, out_file):

    derep_files = find_derep_tsv_files(folder)

    print(f"Found {len(derep_files)} _derep.tsv files:")

    all_dfs = []
    for file in derep_files:
        dataset_name = file.split('/')[-2]
        this_df = pd.read_csv(file, sep='\t')
        this_df['dataset'] = dataset_name
        all_dfs.append(this_df)

    all_df = pd.concat(all_dfs)
    all_df['inchikey_14'] = all_df['inchikey'].str[:14]

    all_df.to_csv(f'{out_file}.tsv', sep='\t', index=False)

    # sort by matched_score
    all_df.sort_values('matched_score', ascending=False, inplace=True)

    # group by inchikey_14, keep first row
    all_grouped = all_df.groupby('inchikey_14')
    out_df = all_grouped.first().reset_index()
    # add a col for the number of unique datasets
    out_df['num_datasets'] = all_grouped['dataset'].nunique().reset_index()['dataset']

    out_df.to_csv(f'{out_file}_grouped.tsv', sep='\t', index=False)


if __name__ == '__main__':
    # merge('/Users/shipei/Documents/projects/ms1_id/imaging/hepatocytes', 'data/all_hepatocytes_derep')

    merge('/Users/shipei/Documents/projects/ms1_id/imaging/HeLa_NIH3T3', 'data/all_HeLa_NIH3T3_derep')
