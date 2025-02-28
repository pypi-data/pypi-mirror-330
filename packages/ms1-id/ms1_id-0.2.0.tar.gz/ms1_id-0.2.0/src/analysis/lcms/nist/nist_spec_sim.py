import pandas as pd
import numpy as np


def align_feature_tables():
    """
    based on feature table from DDA MS2 analysis, align results from DDA MS1, Full scan MS1 0, 10, 20 eV
    """
    # read feature tables
    ms2_dda_df = pd.read_csv('../../../../data/nist/dda_ms2/aligned_feature_table.tsv', sep='\t', low_memory=False)
    ms1_dda_df = pd.read_csv('../../../../data/nist/dda_ms1/aligned_feature_table.tsv', sep='\t', low_memory=False)
    ms1_0ev_df = pd.read_csv('../../../../data/nist/fullscan_0ev/aligned_feature_table.tsv', sep='\t', low_memory=False)
    ms1_10ev_df = pd.read_csv('../../../../data/nist/fullscan_10ev/aligned_feature_table.tsv', sep='\t', low_memory=False)
    ms1_20ev_df = pd.read_csv('../../../../data/nist/fullscan_20ev/aligned_feature_table.tsv', sep='\t', low_memory=False)

    # align to DDA MS2
    ms2_dda_df['ms1_dda_pms2'] = [None] * ms2_dda_df.shape[0]
    ms2_dda_df['ms1_0ev_pms2'] = [None] * ms2_dda_df.shape[0]
    ms2_dda_df['ms1_10ev_pms2'] = [None] * ms2_dda_df.shape[0]
    ms2_dda_df['ms1_20ev_pms2'] = [None] * ms2_dda_df.shape[0]

    for df, col_name in zip([ms1_dda_df, ms1_0ev_df, ms1_10ev_df, ms1_20ev_df],
                            ['ms1_dda_pms2', 'ms1_0ev_pms2', 'ms1_10ev_pms2', 'ms1_20ev_pms2']):
        print(f'Aligning {col_name}...')

        for i, row in ms2_dda_df.iterrows():
            prec_mz = row['m/z']
            rt = row['RT']

            # find in feature table
            mask = ((df['m/z'] - prec_mz).abs() <= max(0.005, prec_mz * 1e-5)) & ((df['RT'] - rt).abs() <= 0.05)
            if sum(mask) > 0:
                pms2_list = df[mask]['pseudo_ms2'].tolist()
                # remove nan
                pms2_list = [x for x in pms2_list if not pd.isnull(x)]

                if len(pms2_list) > 0:
                    final_pms2_list = []
                    # convert to 2d numpy arrays
                    for pms2 in pms2_list:
                        pms2 = pms2.split(';')
                        pms2 = [x.split(' ') for x in pms2][:-1]
                        pms2 = [[float(x) for x in y] for y in pms2]
                        pms2 = np.array(pms2, dtype=np.float32)
                        final_pms2_list.append(pms2)
                    ms2_dda_df.at[i, col_name] = final_pms2_list

        print(f'{col_name}: {sum(ms2_dda_df[col_name].notnull())} features aligned')

    # save
    ms2_dda_df.to_pickle('data/aligned_feature_table_pms2.pkl')


from revcos_main import *
from matchms import Spectrum
def calc_revcos(reverse_cosine, pseudo_ms2, dda_ms2, prec_mz):

    # remove peaks with mz > precursor_mz
    pseudo_ms2 = pseudo_ms2[pseudo_ms2[:, 0] < prec_mz + 0.05]
    dda_ms2 = dda_ms2[dda_ms2[:, 0] < prec_mz + 0.05]

    # # remove peaks with relative intensity < 1%
    # pseudo_ms2 = pseudo_ms2[pseudo_ms2[:, 1] > pseudo_ms2[:, 1].max() * 0.01]
    # dda_ms2 = dda_ms2[dda_ms2[:, 1] > dda_ms2[:, 1].max() * 0.01]

    # sort by mz
    pseudo_ms2 = pseudo_ms2[np.argsort(pseudo_ms2[:, 0])]
    dda_ms2 = dda_ms2[np.argsort(dda_ms2[:, 0])]

    spectrum_1 = Spectrum(mz=dda_ms2[:, 0], intensities=np.sqrt(dda_ms2[:, 1]), metadata={"precursor_mz": prec_mz})
    spectrum_2 = Spectrum(mz=pseudo_ms2[:, 0], intensities=np.sqrt(pseudo_ms2[:, 1]), metadata={"precursor_mz": prec_mz})

    score, matched_peak, spec_usage_ref, spec_usage_qry, idx_ls_ref, idx_ls_qry = (
        reverse_cosine.pair(spectrum_1, spectrum_2))

    return (score, matched_peak, spec_usage_ref, spec_usage_qry,
            matched_peak / len(dda_ms2), matched_peak / len(pseudo_ms2))


def calc_spec_similarity():
    df = pd.read_pickle('data/aligned_feature_table_pms2.pkl')

    revcos_engine = ReverseCosine(tolerance=0.05)

    for col_name in ['ms1_dda_pms2', 'ms1_0ev_pms2', 'ms1_10ev_pms2', 'ms1_20ev_pms2']:
        df[f'{col_name}_similarity'] = [None] * df.shape[0]
        for i, row in df.iterrows():
            if pd.isnull(row['MS2']):
                continue

            if not isinstance(row[col_name], list):
                continue

            pms2_ls = row[col_name]

            # DDA MS2
            dda_ms2 = row['MS2']
            dda_ms2 = dda_ms2.split('|')
            dda_ms2 = [x.split(';') for x in dda_ms2]
            dda_ms2 = [[float(x) for x in y] for y in dda_ms2]
            dda_ms2 = np.array(dda_ms2, dtype=np.float32)

            score_ls = []
            matched_peak_ls = []
            spec_usage_qry_ls = []
            spec_usage_ref_ls = []
            match_ratio_qry_ls = []
            match_ratio_ref_ls = []
            for pms2 in pms2_ls:
                result = calc_revcos(revcos_engine, pms2, dda_ms2, row['m/z'])
                score_ls.append(result[0])
                matched_peak_ls.append(result[1])
                spec_usage_ref_ls.append(result[2])
                spec_usage_qry_ls.append(result[3])
                match_ratio_ref_ls.append(result[4])
                match_ratio_qry_ls.append(result[5])

                # peak scaling
                factor = np.exp(pms2[:, 0] / row['m/z'] * 10)
                pms2[:, 1] *= factor
                result = calc_revcos(revcos_engine, pms2, dda_ms2, row['m/z'])
                score_ls.append(result[0])
                matched_peak_ls.append(result[1])
                spec_usage_ref_ls.append(result[2])
                spec_usage_qry_ls.append(result[3])
                match_ratio_ref_ls.append(result[4])
                match_ratio_qry_ls.append(result[5])
            df.at[i, f'{col_name}_similarity'] = max(score_ls)

        print(f'{col_name}: {sum(df[f"{col_name}_similarity"].notnull())} similarities calculated')

    df.to_pickle('data/aligned_feature_table_pms2_revcos.pkl')


import matplotlib.pyplot as plt
def result_analysis():

    df = pd.read_pickle('data/aligned_feature_table_pms2_revcos.pkl')

    for col_name in ['ms1_dda_pms2', 'ms1_0ev_pms2', 'ms1_10ev_pms2', 'ms1_20ev_pms2']:
        sim_col_name = f'{col_name}_similarity'

        # histogram
        df[sim_col_name].hist(bins=50)
        plt.title(f'{col_name} similarity')
        plt.show()



if __name__ == '__main__':
    # align_feature_tables()

    # calc_spec_similarity()

    result_analysis()