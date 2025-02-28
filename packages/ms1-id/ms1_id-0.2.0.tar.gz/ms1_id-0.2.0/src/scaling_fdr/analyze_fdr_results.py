import pandas as pd


def add_ion_mode(search):
    """
    only keep rows with ion mode matched
    """
    nist20 = pd.read_csv('/Users/shipei/Documents/projects/ms2/ms2_lib/nist20/nist20/nist20.tsv',
                         sep='\t', low_memory=False)
    nist20['Ion_mode'] = nist20['Ion_mode'].str.lower()
    # dict from NIST_No to ion mode
    nist_no_to_ion_mode = nist20.set_index('NIST_No')['Ion_mode'].to_dict()

    gnps = pd.read_pickle('/Users/shipei/Documents/projects/ms1_id/data/ms2db/gnps.pkl')
    gnps['ion_mode'] = gnps['ion_mode'].str[0].str.lower()
    gnps_id_to_ion_mode_dict = dict(zip(gnps['db_id'], gnps['ion_mode']))

    df = pd.read_csv(f'{search}_results_mces.tsv', sep='\t')

    df['matched_gnps_id'] = df['matched_db_id'].apply(lambda x: x.split('=')[1].split(';')[0])  # gnps
    df['matched_ion_mode'] = df['matched_gnps_id'].map(gnps_id_to_ion_mode_dict)

    df['qry_ion_mode'] = df['qry_db_id'].map(nist_no_to_ion_mode)

    df['ion_mode_match'] = df['qry_ion_mode'] == df['matched_ion_mode']

    # save
    df.to_csv(f'{search}_results_mces.tsv', sep='\t', index=False)
    print(df['ion_mode_match'].value_counts())


def main_fdr(search, score_cutoff=0.8, min_matched_peak=4, mces_dist_cutoff=2):
    df = pd.read_csv(f'{search}_results_mces.tsv', sep='\t')

    df = df[(pd.notnull(df['mces_dist'])) & (df['ion_mode_match'])].reset_index(drop=True)
    df = df[(df['score'] >= score_cutoff) & (df['matched_peak'] >= min_matched_peak)].reset_index(drop=True)

    df['match'] = df['mces_dist'] <= mces_dist_cutoff

    print('====================')
    print(df['match'].value_counts())
    print('FDR: ', sum(df['match'] == False) / df.shape[0])

    # for each qry_id, retain the best match
    df = df.sort_values('score', ascending=False).drop_duplicates('qry_db_id').reset_index(drop=True)
    print('====================')
    print('After best match selection:')
    print(df['match'].value_counts())
    print('FDR: ', sum(df['match'] == False) / df.shape[0])


def search_merged_fdr(score_cutoff=0.8, min_matched_peak=4, mces_dist_cutoff=2):
    mode = 'k10'
    df1 = pd.read_csv('k0_results_mces.tsv', sep='\t')
    df2 = pd.read_csv(f'{mode}_results_mces.tsv', sep='\t')

    df = pd.concat([df1, df2]).reset_index(drop=True)
    df = df[(pd.notnull(df['mces_dist'])) & (df['ion_mode_match'])].reset_index(drop=True)

    df = df[(df['score'] >= score_cutoff) & (df['matched_peak'] >= min_matched_peak)].reset_index(drop=True)
    df.drop_duplicates(subset=['qry_db_id', 'matched_db_id'], inplace=True)

    df['match'] = df['mces_dist'] <= mces_dist_cutoff

    print('====================')
    print(df['match'].value_counts())

    print('FDR: ', sum(df['match'] == False) / df.shape[0])

    # for each qry_id, retain the best match
    df = df.sort_values('score', ascending=False).drop_duplicates('qry_db_id').reset_index(drop=True)
    print('====================')
    print('After best match selection:')
    print(df['match'].value_counts())
    print('FDR: ', sum(df['match'] == False) / df.shape[0])


if __name__ == '__main__':
    # add_ion_mode('k0')
    # add_ion_mode('k10')

    mces_dist_cutoff = 4

    min_score = 0.7
    min_peaks = 3
    main_fdr('k0', min_score, min_peaks, mces_dist_cutoff)

    main_fdr('k10', min_score, min_peaks, mces_dist_cutoff)

    search_merged_fdr(min_score, min_peaks, mces_dist_cutoff)
