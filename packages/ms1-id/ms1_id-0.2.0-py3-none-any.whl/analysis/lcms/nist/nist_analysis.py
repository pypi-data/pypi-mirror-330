import pickle

import pandas as pd


def print_annotation_stats(score_threshold=0.7, usage_threshold=0.20):
    # DDA MS2
    ms2_dda_df = pd.read_csv('../../../../data/nist/dda_ms2/aligned_feature_table.tsv', sep='\t', low_memory=False)

    # DDA MS1
    ms1_dda_df = pd.read_csv('../../../../data/nist/dda_ms1/aligned_feature_table.tsv', sep='\t', low_memory=False)

    # Full scan MS1
    ms1_0ev_df = pd.read_csv('../../../../data/nist/fullscan_0ev/aligned_feature_table.tsv', sep='\t', low_memory=False)
    ms1_10ev_df = pd.read_csv('../../../../data/nist/fullscan_10ev/aligned_feature_table.tsv', sep='\t',
                              low_memory=False)
    ms1_20ev_df = pd.read_csv('../../../../data/nist/fullscan_20ev/aligned_feature_table.tsv', sep='\t',
                              low_memory=False)

    print('Total features in each mode:')
    print(f'DDA MS2: {ms2_dda_df.shape[0]}')
    print(f'DDA MS1: {ms1_dda_df.shape[0]}')
    print(f'Full scan MS1 0 eV: {ms1_0ev_df.shape[0]}')
    print(f'Full scan MS1 10 eV: {ms1_10ev_df.shape[0]}')
    print(f'Full scan MS1 20 eV: {ms1_20ev_df.shape[0]}')

    print('DDA MS2 collected features:', ms2_dda_df[ms2_dda_df['MS2'].notnull()].shape[0])
    print('DDA MS2 not collected features:', ms2_dda_df[ms2_dda_df['MS2'].isnull()].shape[0])

    ms2_dda_df = ms2_dda_df[ms2_dda_df['similarity'].notnull()].reset_index(drop=True)
    ms1_dda_df = ms1_dda_df[ms1_dda_df['MS1_similarity'].notnull()].reset_index(drop=True)
    ms1_0ev_df = ms1_0ev_df[ms1_0ev_df['MS1_similarity'].notnull()].reset_index(drop=True)
    ms1_10ev_df = ms1_10ev_df[ms1_10ev_df['MS1_similarity'].notnull()].reset_index(drop=True)
    ms1_20ev_df = ms1_20ev_df[ms1_20ev_df['MS1_similarity'].notnull()].reset_index(drop=True)

    ms2_dda_df = ms2_dda_df[ms2_dda_df['similarity'] >= score_threshold].reset_index(drop=True)
    ms1_dda_df = ms1_dda_df[(ms1_dda_df['MS1_similarity'] >= score_threshold) &
                            (ms1_dda_df['MS1_spectral_usage'] >= usage_threshold)].reset_index(drop=True)
    ms1_0ev_df = ms1_0ev_df[(ms1_0ev_df['MS1_similarity'] >= score_threshold) &
                            (ms1_0ev_df['MS1_spectral_usage'] >= usage_threshold)].reset_index(drop=True)
    ms1_10ev_df = ms1_10ev_df[(ms1_10ev_df['MS1_similarity'] >= score_threshold) &
                              (ms1_10ev_df['MS1_spectral_usage'] >= usage_threshold)].reset_index(drop=True)
    ms1_20ev_df = ms1_20ev_df[(ms1_20ev_df['MS1_similarity'] >= score_threshold) &
                              (ms1_20ev_df['MS1_spectral_usage'] >= usage_threshold)].reset_index(drop=True)

    print('Number of annotated features in each mode:')
    print(f'DDA MS2: {ms2_dda_df.shape[0]}')
    print(f'DDA MS1: {ms1_dda_df.shape[0]}')
    print(f'Full scan MS1 0 eV: {ms1_0ev_df.shape[0]}')
    print(f'Full scan MS1 10 eV: {ms1_10ev_df.shape[0]}')
    print(f'Full scan MS1 20 eV: {ms1_20ev_df.shape[0]}')

    ms2_dda_inchikey = ms2_dda_df['InChIKey'].unique().tolist()
    ms1_dda_inchikey = ms1_dda_df['MS1_inchikey'].unique().tolist()
    ms1_0ev_inchikey = ms1_0ev_df['MS1_inchikey'].unique().tolist()
    ms1_10ev_inchikey = ms1_10ev_df['MS1_inchikey'].unique().tolist()
    ms1_20ev_inchikey = ms1_20ev_df['MS1_inchikey'].unique().tolist()

    # remove nan inchikey
    ms2_dda_inchikey = [i for i in ms2_dda_inchikey if not pd.isnull(i)]
    ms1_dda_inchikey = [i for i in ms1_dda_inchikey if not pd.isnull(i)]
    ms1_0ev_inchikey = [i for i in ms1_0ev_inchikey if not pd.isnull(i)]
    ms1_10ev_inchikey = [i for i in ms1_10ev_inchikey if not pd.isnull(i)]
    ms1_20ev_inchikey = [i for i in ms1_20ev_inchikey if not pd.isnull(i)]

    print('Number of unique inchikey (3D) in each mode:')
    print(f'DDA MS2: {len(ms2_dda_inchikey)}')
    print(f'DDA MS1: {len(ms1_dda_inchikey)}')
    print(f'Full scan MS1 0 eV: {len(ms1_0ev_inchikey)}')
    print(f'Full scan MS1 10 eV: {len(ms1_10ev_inchikey)}')
    print(f'Full scan MS1 20 eV: {len(ms1_20ev_inchikey)}')

    # 2D inchikey
    ms2_dda_inchikey_2d = [i[:14] for i in ms2_dda_inchikey]
    ms1_dda_inchikey_2d = [i[:14] for i in ms1_dda_inchikey]
    ms1_0ev_inchikey_2d = [i[:14] for i in ms1_0ev_inchikey]
    ms1_10ev_inchikey_2d = [i[:14] for i in ms1_10ev_inchikey]
    ms1_20ev_inchikey_2d = [i[:14] for i in ms1_20ev_inchikey]

    print('Number of unique inchikey (2D) in each mode:')
    print(f'DDA MS2: {len(set(ms2_dda_inchikey_2d))}')
    print(f'DDA MS1: {len(set(ms1_dda_inchikey_2d))}')
    print(f'Full scan MS1 0 eV: {len(set(ms1_0ev_inchikey_2d))}')
    print(f'Full scan MS1 10 eV: {len(set(ms1_10ev_inchikey_2d))}')
    print(f'Full scan MS1 20 eV: {len(set(ms1_20ev_inchikey_2d))}')

    # # save
    # pickle.dump(ms2_dda_inchikey_2d, open('data/ms2_dda_inchikey.pkl', 'wb'))
    # pickle.dump(ms1_dda_inchikey_2d, open('data/ms1_dda_inchikey.pkl', 'wb'))
    # pickle.dump(ms1_0ev_inchikey_2d, open('data/ms1_0ev_inchikey.pkl', 'wb'))
    # pickle.dump(ms1_10ev_inchikey_2d, open('data/ms1_10ev_inchikey.pkl', 'wb'))
    # pickle.dump(ms1_20ev_inchikey_2d, open('data/ms1_20ev_inchikey.pkl', 'wb'))


def align_feature_tables(score_threshold=0.7, usage_threshold=0.20):
    """
    based on feature table from DDA MS2 analysis, align results from DDA MS1, Full scan MS1 0, 10, 20 eV
    """
    # read feature tables
    ms2_dda_df = pd.read_csv('../../../../data/nist/dda_ms2/aligned_feature_table.tsv', sep='\t', low_memory=False)
    ms1_dda_df = pd.read_csv('../../../../data/nist/dda_ms1/aligned_feature_table.tsv', sep='\t', low_memory=False)
    ms1_0ev_df = pd.read_csv('../../../../data/nist/fullscan_0ev/aligned_feature_table.tsv', sep='\t', low_memory=False)
    ms1_10ev_df = pd.read_csv('../../../../data/nist/fullscan_10ev/aligned_feature_table.tsv', sep='\t',
                              low_memory=False)
    ms1_20ev_df = pd.read_csv('../../../../data/nist/fullscan_20ev/aligned_feature_table.tsv', sep='\t',
                              low_memory=False)

    ms1_dda_df = ms1_dda_df[ms1_dda_df['MS1_similarity'].notnull()].reset_index(drop=True)
    ms1_0ev_df = ms1_0ev_df[ms1_0ev_df['MS1_similarity'].notnull()].reset_index(drop=True)
    ms1_10ev_df = ms1_10ev_df[ms1_10ev_df['MS1_similarity'].notnull()].reset_index(drop=True)
    ms1_20ev_df = ms1_20ev_df[ms1_20ev_df['MS1_similarity'].notnull()].reset_index(drop=True)

    ms1_dda_df = ms1_dda_df[(ms1_dda_df['MS1_similarity'] >= score_threshold) &
                            (ms1_dda_df['MS1_spectral_usage'] >= usage_threshold)].reset_index(drop=True)
    ms1_0ev_df = ms1_0ev_df[(ms1_0ev_df['MS1_similarity'] >= score_threshold) &
                            (ms1_0ev_df['MS1_spectral_usage'] >= usage_threshold)].reset_index(drop=True)
    ms1_10ev_df = ms1_10ev_df[(ms1_10ev_df['MS1_similarity'] >= score_threshold) &
                              (ms1_10ev_df['MS1_spectral_usage'] >= usage_threshold)].reset_index(drop=True)
    ms1_20ev_df = ms1_20ev_df[(ms1_20ev_df['MS1_similarity'] >= score_threshold) &
                              (ms1_20ev_df['MS1_spectral_usage'] >= usage_threshold)].reset_index(drop=True)

    # align to DDA MS2
    ms2_dda_df['ms1_dda_inchikeys'] = [None] * ms2_dda_df.shape[0]
    ms2_dda_df['ms1_0ev_inchikeys'] = [None] * ms2_dda_df.shape[0]
    ms2_dda_df['ms1_10ev_inchikeys'] = [None] * ms2_dda_df.shape[0]
    ms2_dda_df['ms1_20ev_inchikeys'] = [None] * ms2_dda_df.shape[0]

    for df, col_name in zip([ms1_dda_df, ms1_0ev_df, ms1_10ev_df, ms1_20ev_df],
                            ['ms1_dda_inchikeys', 'ms1_0ev_inchikeys', 'ms1_10ev_inchikeys', 'ms1_20ev_inchikeys']):
        print(f'Aligning {col_name}...')

        df['used'] = [False] * df.shape[0]

        for i, row in ms2_dda_df.iterrows():
            prec_mz = row['m/z']
            rt = row['RT']

            # find in feature table
            mask = ((df['m/z'] - prec_mz).abs() <= 0.01) & ((df['RT'] - rt).abs() <= 0.1)
            if sum(mask) > 0:
                ms2_dda_df.at[i, col_name] = df[mask]['MS1_inchikey'].tolist()
                df.loc[mask, 'used'] = True

        print(f'{col_name}: {sum(df["used"])} annotations aligned')

        _df = ms2_dda_df[(ms2_dda_df['MS2'].notnull()) & (ms2_dda_df[col_name].notnull())]
        print(f'{col_name}: DDA MS2 collected, {len(_df)} annotations')

        _df = ms2_dda_df[(ms2_dda_df['MS2'].isnull()) & (ms2_dda_df[col_name].notnull())]
        print(f'{col_name}: DDA MS2 not collected, {len(_df)} annotations')

        print(f'{col_name}: {len(df) - sum(df["used"])} new annotations')

        # save
        out_name = f'data/{col_name.split("_inchi")[0]}_df.pkl'
        df.to_pickle(out_name)

    # save
    ms2_dda_df.to_csv('data/aligned_feature_table_all.tsv', sep='\t', index=False)
    ms2_dda_df.to_pickle('data/aligned_feature_table_all.pkl')


if __name__ == '__main__':
    print_annotation_stats()
    #
    align_feature_tables()
