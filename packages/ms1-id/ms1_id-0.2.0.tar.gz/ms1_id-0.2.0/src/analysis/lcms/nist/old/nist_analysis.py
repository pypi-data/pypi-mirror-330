import numpy as np
import pandas as pd
import os
import pickle


def merge_ms1_annotations(db='gnps'):
    df_dir = f'../../../../data/nist_samples/data_1/output_{db}'
    files = [f for f in os.listdir(df_dir) if f.endswith('.tsv')]
    files = [os.path.join(df_dir, f) for f in files]

    all_df = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f, sep='\t', low_memory=False)
        df['file'] = f.split('/')[-1].split('.')[0]
        all_df = pd.concat([all_df, df])

    all_df.to_csv(f'merged_ms1_{db}.tsv', sep='\t', index=False)


def merge_ms2_annotations(db='gnps'):
    df_dir = f'../../../../data/nist_samples/data_2/output_{db}'
    files = [f for f in os.listdir(df_dir) if f.endswith('.tsv')]
    files = [os.path.join(df_dir, f) for f in files]

    all_df = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f, sep='\t', low_memory=False)
        df['file'] = f.split('/')[-1].split('.')[0]
        all_df = pd.concat([all_df, df])

    all_df.to_csv(f'merged_ms2_{db}.tsv', sep='\t', index=False)


def ms2_annotation_analysis(db='gnps', score_cutoff=0.7, min_matched_peak=4):
    df_dir = f'../../../../data/nist_samples/data_2/output_{db}'
    files = [f for f in os.listdir(df_dir) if f.endswith('.tsv')]
    files = [os.path.join(df_dir, f) for f in files]

    inchikey_ls = []
    for f in files:
        df = pd.read_csv(f, sep='\t', low_memory=False)

        df = df[df['MS2_similarity'].notnull()]

        df = df[(df['MS2_similarity'] >= score_cutoff) & (df['MS2_matched_peak'] >= min_matched_peak)]

        inchikey_ls += df['MS2_inchikey'].unique().tolist()

    # remove nan
    inchikey_ls = [i for i in inchikey_ls if not pd.isnull(i)]

    inchikey_ls = list(set(inchikey_ls))
    print(f'{db}: {len(inchikey_ls)} unique inchikeys')

    # save
    pickle.dump(inchikey_ls, open(f'ms2_inchikey_{db}.pkl', 'wb'))


def ms1_annotation_analysis(db, score_cutoff=0.7, min_matched_peak=4, ev=0):
    df_dir = f'../../../../data/nist_samples/data_1/output_{db}'
    files = [f for f in os.listdir(df_dir) if f.endswith(f'_{ev}eV_feature_table.tsv')]
    files = [os.path.join(df_dir, f) for f in files]

    inchikey_ls = []
    for f in files:
        df = pd.read_csv(f, sep='\t', low_memory=False)

        df = df[df['MS1_similarity'].notnull()]

        df = df[(df['MS1_similarity'] >= score_cutoff) & (df['MS1_matched_peak'] >= min_matched_peak)]

        inchikey_ls += df['MS1_inchikey'].unique().tolist()

    # remove nan
    inchikey_ls = [i for i in inchikey_ls if not pd.isnull(i)]

    inchikey_ls = list(set(inchikey_ls))
    print(f'{db}: {len(inchikey_ls)} unique inchikeys')

    # save
    pickle.dump(inchikey_ls, open(f'ms1_inchikey_{db}_{ev}ev.pkl', 'wb'))


def annotation_overlap(db='gnps'):
    ms2_inchikey = pickle.load(open(f'ms2_inchikey_{db}.pkl', 'rb'))

    ms1_inchikey_0ev = pickle.load(open(f'ms1_inchikey_{db}_0ev.pkl', 'rb'))

    ms1_inchikey_10ev = pickle.load(open(f'ms1_inchikey_{db}_10ev.pkl', 'rb'))

    # overlap
    print('ms2 and ms1 0 eV')
    ms2_0ev_overlap = set(ms2_inchikey).intersection(set(ms1_inchikey_0ev))
    print(f'{len(ms2_0ev_overlap)} common inchikeys: {ms2_0ev_overlap}')

    print('ms2 and ms1 10 eV')
    ms2_10ev_overlap = set(ms2_inchikey).intersection(set(ms1_inchikey_10ev))
    print(f'{len(ms2_10ev_overlap)} common inchikeys: {ms2_10ev_overlap}')

    print('0 eV and 10 eV')
    ms1_0_10_overlap = set(ms1_inchikey_0ev).intersection(set(ms1_inchikey_10ev))
    print(f'{len(ms1_0_10_overlap)} common inchikeys: {ms1_0_10_overlap}')

    print('ms2 and ms1 0 eV and 10 eV')
    overlap = set(ms2_inchikey).intersection(set(ms1_inchikey_0ev)).intersection(set(ms1_inchikey_10ev))
    print(f'{len(overlap)} common inchikeys: {overlap}')

    print('in ms1 0 eV or 10 eV but not in ms2')
    ms1_not_ms2 = set(ms1_inchikey_0ev).union(set(ms1_inchikey_10ev)).difference(set(ms2_inchikey))
    # save
    pickle.dump(ms1_not_ms2, open(f'ms1_not_ms2_{db}.pkl', 'wb'))


def ms1_not_in_ms2(db):
    ms1_not_ms2 = list(pickle.load(open(f'ms1_not_ms2_{db}.pkl', 'rb')))

    # merged ms1
    ms1_df = pd.read_csv(f'merged_ms1_{db}.tsv', sep='\t', low_memory=False)
    ms1_df = ms1_df[ms1_df['MS1_inchikey'].notnull()].reset_index(drop=True)
    ms1_df = ms1_df[ms1_df['MS1_inchikey'].isin(ms1_not_ms2)]

    # find in feature table for ms2
    ms2_df = pd.read_csv(f'merged_ms2_{db}.tsv', sep='\t', low_memory=False)

    ms1_df['ms2_in_feature_table'] = False
    for i, row in ms1_df.iterrows():
        prec_mz = row['m/z']
        rt = row['RT']
        # find in feature table, precmz tolerance 0.01, rt tolerance 0.05
        df = ms2_df[((ms2_df['m/z'] - prec_mz).abs() <= 0.01) & ((ms2_df['RT'] - rt).abs() <= 0.05)]
        if len(df) > 0:
            # if at least one row has MS2
            if df['MS2'].notnull().any():
                ms1_df.at[i, 'ms2_in_feature_table'] = True

    ms1_df.to_csv(f'ms1_not_ms2_{db}.tsv', sep='\t', index=False)


def ms2_ce_analysis(score_cutoff, min_matched_peak):
    """
    collision energy analysis
    """
    df_dir = '/data/nist_samples/data_2/output_nist20'
    files = [f for f in os.listdir(df_dir) if f.endswith('.tsv')]
    files = [os.path.join(df_dir, f) for f in files]

    all_df = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f, sep='\t', low_memory=False)

        df = df[df['MS2_similarity'].notnull()]

        df = df[(df['MS2_similarity'] >= score_cutoff) & (df['MS2_matched_peak'] >= min_matched_peak)]

        all_df = pd.concat([all_df, df])

    # all_df['ms2_ce_valid'] = all_df['MS2_collision_energy'].apply(lambda x: 'eV' in str(x))
    all_df['ms2_ce_valid'] = all_df['MS2_collision_energy'].apply(lambda x: 'NCE' in str(x))

    # sort by inchikey, then ms2_ce_valid, then MS2_similarity
    all_df = all_df.sort_values(['MS2_inchikey', 'ms2_ce_valid', 'MS2_similarity'],
                                ascending=[True, False, False])
    # remove duplicates
    all_df = all_df.drop_duplicates('MS2_inchikey', keep='first')

    # all_df['ms2_ce'] = all_df.apply(lambda x: x['MS2_collision_energy'].split(' ')[1].split('eV')[0] if x['ms2_ce_valid'] else None, axis=1)
    all_df['ms2_ce'] = all_df.apply(
        lambda x: x['MS2_collision_energy'].split('%')[0].split('=')[1] if x['ms2_ce_valid'] else None, axis=1)

    all_ce = all_df['ms2_ce'].tolist()
    all_ce = [int(c) for c in all_ce if c is not None]

    # save to file
    all_df.to_csv('ms2_ce_analysis.tsv', sep='\t', index=False)
    pickle.dump(all_ce, open('ms2_ce.pkl', 'wb'))


def ms1_ce_analysis(score_cutoff, min_matched_peak, ev=0):
    """
    collision energy analysis
    """
    df_dir = '/data/nist_samples/data_1/output_nist20'
    files = [f for f in os.listdir(df_dir) if f.endswith(f'_{ev}eV_feature_table.tsv')]
    files = [os.path.join(df_dir, f) for f in files]

    all_df = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f, sep='\t', low_memory=False)

        df = df[df['MS1_similarity'].notnull()]

        df = df[(df['MS1_similarity'] >= score_cutoff) & (df['MS1_matched_peak'] >= min_matched_peak)]

        all_df = pd.concat([all_df, df])

    # all_df['ms1_ce_valid'] = all_df['MS1_collision_energy'].apply(lambda x: 'eV' in str(x))
    all_df['ms1_ce_valid'] = all_df['MS1_collision_energy'].apply(lambda x: 'NCE' in str(x))

    # sort by inchikey, then ms1_ce_valid, then MS1_similarity
    all_df = all_df.sort_values(['MS1_inchikey', 'ms1_ce_valid', 'MS1_similarity'],
                                ascending=[True, False, False])
    # remove duplicates
    all_df = all_df.drop_duplicates('MS1_inchikey', keep='first')

    # all_df['ms1_ce'] = all_df.apply(lambda x: x['MS1_collision_energy'].split(' ')[1].split('eV')[0] if x['ms1_ce_valid'] else None, axis=1)
    all_df['ms1_ce'] = all_df.apply(
        lambda x: x['MS1_collision_energy'].split('%')[0].split('=')[1] if x['ms1_ce_valid'] else None, axis=1)

    all_ce = all_df['ms1_ce'].tolist()
    all_ce = [int(c) for c in all_ce if c is not None]

    # save to file
    all_df.to_csv(f'ms1_ce_analysis_{ev}ev.tsv', sep='\t', index=False)
    pickle.dump(all_ce, open(f'ms1_ce_{ev}ev.pkl', 'wb'))


def plot_ms2_ce():
    import matplotlib.pyplot as plt

    all_ce = pickle.load(open('ms2_ce.pkl', 'rb'))

    # Create histogram
    plt.figure(figsize=(5, 3))
    plt.hist(all_ce, bins=np.arange(0, max(all_ce) + 5, 10), color='#56648a', alpha=0.6)
    plt.title('Histogram of MS2 Collision Energies', fontname='Arial', fontsize=12)
    plt.xlabel('NCE (%)')
    plt.ylabel('Frequency')
    plt.xlim(-5, 70)
    plt.savefig('ms2_ce_histogram.svg', transparent=True)
    plt.show()


def plot_ms1_ce(ev=0):
    import matplotlib.pyplot as plt

    all_ce = pickle.load(open(f'ms1_ce_{ev}ev.pkl', 'rb'))

    # Create histogram
    plt.figure(figsize=(5, 3))
    plt.hist(all_ce, bins=np.arange(0, max(all_ce) + 5, 10), color='#56648a', alpha=0.6)
    plt.title('Histogram of MS1 Collision Energies', fontname='Arial', fontsize=12)
    plt.xlabel('NCE (%)')
    plt.ylabel('Frequency')
    plt.xlim(-5, 70)
    # plt.ylim(0, 100)
    plt.savefig(f'ms1_ce_histogram_{ev}ev.svg', transparent=True)
    plt.show()


if __name__ == '__main__':

    score_cutoff = 0.7
    min_matched_peak = 4
    ############################
    ##### annotation analysis #####
    # merge_ms1_annotations(db='gnps')
    # merge_ms1_annotations(db='nist20')
    # merge_ms2_annotations(db='gnps')
    # merge_ms2_annotations(db='nist20')

    # print('=' * 20)
    # print('MS2 annotation')
    # ms2_annotation_analysis('gnps', score_cutoff, min_matched_peak)
    # ms2_annotation_analysis('nist20', score_cutoff, min_matched_peak)
    # #
    # print('=' * 20)
    # print('MS1 annotation')
    # ms1_annotation_analysis('gnps', score_cutoff, min_matched_peak, 0)
    # ms1_annotation_analysis('nist20', score_cutoff, min_matched_peak, 0)
    # #
    # ms1_annotation_analysis('gnps', score_cutoff, min_matched_peak, 10)
    # ms1_annotation_analysis('nist20', score_cutoff, min_matched_peak, 10)
    #
    # print('=' * 20)
    # print('Annotation overlap')
    # annotation_overlap('gnps')
    # annotation_overlap('nist20')
    #
    # ms1_not_in_ms2('gnps')

    ############################
    ##### collision energy analysis #####
    # ms2_ce_analysis(score_cutoff, min_matched_peak)
    # ms1_ce_analysis(score_cutoff, min_matched_peak, 0)
    # ms1_ce_analysis(score_cutoff, min_matched_peak, 10)

    plot_ms2_ce()
    plot_ms1_ce(ev=0)
    plot_ms1_ce(ev=10)
