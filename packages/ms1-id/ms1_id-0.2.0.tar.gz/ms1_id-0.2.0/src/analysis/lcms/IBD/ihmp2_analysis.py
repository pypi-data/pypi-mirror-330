import pandas as pd
import pickle


def four_mode_annotation():
    df1 = pd.read_csv(
        '/data/PR000639/output/hilic_pos_aligned_feature_table.tsv',
        sep='\t', low_memory=False)
    df2 = pd.read_csv(
        '/data/PR000639/output/hilic_neg_aligned_feature_table.tsv',
        sep='\t', low_memory=False)
    df3 = pd.read_csv(
        '/data/PR000639/output/c8_pos_aligned_feature_table.tsv',
        sep='\t', low_memory=False)
    df4 = pd.read_csv(
        '/data/PR000639/output/c18_neg_aligned_feature_table.tsv',
        sep='\t', low_memory=False)

    print('Total features in each mode:')
    print(f'HILIC pos: {df1.shape[0]}')
    print(f'HILIC neg: {df2.shape[0]}')
    print(f'C8 pos: {df3.shape[0]}')
    print(f'C18 neg: {df4.shape[0]}')

    df1 = df1[df1['MS1_similarity'].notnull()].reset_index(drop=True)
    df2 = df2[df2['MS1_similarity'].notnull()].reset_index(drop=True)
    df3 = df3[df3['MS1_similarity'].notnull()].reset_index(drop=True)
    df4 = df4[df4['MS1_similarity'].notnull()].reset_index(drop=True)

    df1 = df1[(df1['MS1_similarity'] >= 0.7) & (df1['MS1_matched_peak'] >= 4) & (df1['MS1_spectral_usage'] >= 0.20)].reset_index(drop=True)
    df2 = df2[(df2['MS1_similarity'] >= 0.7) & (df2['MS1_matched_peak'] >= 4) & (df2['MS1_spectral_usage'] >= 0.20)].reset_index(drop=True)
    df3 = df3[(df3['MS1_similarity'] >= 0.7) & (df3['MS1_matched_peak'] >= 4) & (df3['MS1_spectral_usage'] >= 0.20)].reset_index(drop=True)
    df4 = df4[(df4['MS1_similarity'] >= 0.7) & (df4['MS1_matched_peak'] >= 4) & (df4['MS1_spectral_usage'] >= 0.20)].reset_index(drop=True)

    df1_inchikey = df1['MS1_inchikey'].unique().tolist()
    df2_inchikey = df2['MS1_inchikey'].unique().tolist()
    df3_inchikey = df3['MS1_inchikey'].unique().tolist()
    df4_inchikey = df4['MS1_inchikey'].unique().tolist()

    # remove nan inchikey
    df1_inchikey = [i for i in df1_inchikey if not pd.isnull(i)]
    df2_inchikey = [i for i in df2_inchikey if not pd.isnull(i)]
    df3_inchikey = [i for i in df3_inchikey if not pd.isnull(i)]
    df4_inchikey = [i for i in df4_inchikey if not pd.isnull(i)]

    print('Number of MS1 inchikey in each mode:')
    print(f'HILIC pos: {len(df1_inchikey)}')
    print(f'HILIC neg: {len(df2_inchikey)}')
    print(f'C8 pos: {len(df3_inchikey)}')
    print(f'C18 neg: {len(df4_inchikey)}')

    # total unique inchikey
    total_inchikey = set(df1_inchikey).union(set(df2_inchikey)).union(set(df3_inchikey)).union(set(df4_inchikey))
    print(f'Total unique inchikey: {len(total_inchikey)}')

    # save
    pickle.dump(df1_inchikey, open('data/hilic_pos_inchikey.pkl', 'wb'))
    pickle.dump(df2_inchikey, open('data/hilic_neg_inchikey.pkl', 'wb'))
    pickle.dump(df3_inchikey, open('data/c8_pos_inchikey.pkl', 'wb'))
    pickle.dump(df4_inchikey, open('data/c18_neg_inchikey.pkl', 'wb'))


def add_metadata():
    modes = ['hilic_pos', 'hilic_neg', 'c8_pos', 'c18_neg']

    metadata = pd.read_csv('/data/PR000639/metadata/metadata.csv')
    # dictionary from local_sample_id to Diagnosis and sex
    sample_id_to_diagnosis = dict(zip(metadata['local_sample_id'], metadata['Diagnosis']))
    sample_id_to_sex = dict(zip(metadata['local_sample_id'], metadata['sex']))

    for mode in modes:
        df = pd.read_csv(
            f'/Users/shipei/Documents/projects/ms1_id/data/PR000639/output/{mode}_aligned_feature_table.tsv',
            sep='\t', low_memory=False)

        meta_df = pd.read_csv(f'/Users/shipei/Documents/projects/ms1_id/data/PR000639/metadata/{mode}.csv')
        meta_df['raw_name'] = meta_df['Raw file name'].apply(lambda x: x.split('.')[0])
        # dictionary from raw_name to 'Sample ID'
        raw_name_to_sample_id = dict(zip(meta_df['raw_name'], meta_df['Sample ID']))

        # change df column names
        col_diagnosis = []
        col_sex = []
        new_columns = []
        for col in df.columns:
            if col in raw_name_to_sample_id.keys():
                sample_id = raw_name_to_sample_id[col]
                new_columns.append(sample_id)

                # pooled ref. mixture
                if sample_id.startswith('PREF'):
                    col_diagnosis.append(None)
                    col_sex.append(None)
                else:
                    col_diagnosis.append(sample_id_to_diagnosis[sample_id])
                    col_sex.append(sample_id_to_sex[sample_id])
            else:
                new_columns.append(col)
                col_diagnosis.append(None)
                col_sex.append(None)

        # Rename columns
        df.columns = new_columns

        # Add two rows for diagnosis and sex
        diagnosis_row = pd.Series(col_diagnosis, index=df.columns, name='diagnosis')
        sex_row = pd.Series(col_sex, index=df.columns, name='sex')

        # Concatenate the new rows with the existing DataFrame
        df = pd.concat([diagnosis_row.to_frame().T, sex_row.to_frame().T, df], axis=0)

        # Reset the index
        df = df.reset_index(drop=True)

        # Save the updated DataFrame
        df.to_csv(
            f'/Users/shipei/Documents/projects/ms1_id/data/PR000639/{mode}_aligned_feature_table_with_metadata.tsv',
            sep='\t', index=False)


if __name__ == '__main__':
    ################
    four_mode_annotation()
    '''
Total features in each mode:
HILIC pos: 20401
HILIC neg: 5807
C8 pos: 9502
C18 neg: 9079

Number of MS1 inchikey in each mode:
HILIC pos: 3010
HILIC neg: 293
C8 pos: 227
C18 neg: 636
Total unique inchikey: 3802
    '''

    # add_metadata()
