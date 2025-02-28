import pandas as pd
import numpy as np
from matchms import Spectrum
from matchms.similarity import CosineGreedy
from matplotlib import pyplot as plt


from json import loads as loads
from requests import get


def gnps_id_to_spec(gnps_id):
    usi = f'mzspec:GNPS:GNPS-LIBRARY:accession:{gnps_id}'
    # get spectrum from USI
    url = 'https://metabolomics-usi.gnps2.org/json/?usi1=' + usi
    response = get(url)
    json_data = loads(response.text)
    ms2_mz = np.array(json_data['peaks'])[:, 0]
    ms2_int = np.array(json_data['peaks'])[:, 1]

    return ms2_mz, ms2_int, json_data['precursor_mz']


def get_gnps_std_spec():
    gnps_id_ls = ['CCMSLIB00010011135', 'CCMSLIB00010012730', 'CCMSLIB00010011156']
    names = ['Citrulline-C9:0', '3-hydroxy lauric acid-C22:5', 'L-DOPA-C10:0']

    spectrum_ls = []
    for gnps_id, name in zip(gnps_id_ls, names):
        ms2_mz, ms2_int, prec_mz = gnps_id_to_spec(gnps_id)

        # 1% relative intensity
        mask = (ms2_int > max(ms2_int) * 0.01) & (ms2_mz < prec_mz - 0.1)
        ms2_mz = ms2_mz[mask]
        ms2_int = ms2_int[mask]
        spectrum = Spectrum(mz=ms2_mz, intensities=ms2_int,
                            metadata={"precursor_mz": prec_mz,
                                      "name": name})
        spectrum_ls.append(spectrum)

    return spectrum_ls


def get_std_pms2():
    df = pd.read_csv(
        '/bin/ms1id/lcms/analysis/std/output_all/mixture_Drugs_0eV_feature_table.tsv',
        sep='\t', low_memory=False)

    df = df[(df['MS1_precursor_type'].isin(['[M+H]+'])) & (df['MS1_matched_peak'] > 4)]
    # df = df[(df['MS1_precursor_type'].isin(['[M+H]+', '[M+H-H2O]+'])) & (df['MS1_matched_peak'] > 4)]

    #  sort by MS1_spectral_usage
    df = df.sort_values('MS1_matched_peak', ascending=False)

    # take first 10 rows
    df = df.iloc[:10]

    spectrum_ls = []
    for i, row in df.iterrows():

        pms2 = row['pseudo_ms2'].split(';')
        pms2 = [x.strip().split(' ') for x in pms2][:-1]
        pms2 = [[float(x) for x in y] for y in pms2]
        pms2 = np.array(pms2, dtype=np.float32)

        # remove ions larger than precursor
        pms2 = pms2[pms2[:, 0] < row['m/z'] - 0.1]

        mzs = pms2[:, 0]
        intensities = pms2[:, 1]

        # sort
        idx = np.argsort(mzs)
        mzs = mzs[idx]
        intensities = intensities[idx]

        spectrum = Spectrum(mz=mzs, intensities=intensities,
                            metadata={"precursor_mz": float(row['m/z']),
                                      "name": row['MS1_annotation']})
        spectrum_ls.append(spectrum)

    return spectrum_ls


def get_ref_pms2():
    df = pd.read_csv(
        '/data/nist/fullscan_0ev/aligned_feature_table.tsv',
        sep='\t', low_memory=False)

    df = df[(df['MS1_similarity'].notnull()) & (df['MS1_matched_peak'] > 4)]

    #  sort by MS1_spectral_usage
    df = df.sort_values('MS1_matched_peak', ascending=False)

    # # take first 3 rows
    # df = df.iloc[:3]

    spectrum_ls = []
    for i, row in df.iterrows():

        pms2 = row['pseudo_ms2'].split(';')
        pms2 = [x.strip().split(' ') for x in pms2][:-1]
        pms2 = [[float(x) for x in y] for y in pms2]
        pms2 = np.array(pms2, dtype=np.float32)

        # remove ions larger than precursor
        pms2 = pms2[pms2[:, 0] < row['m/z'] + 0.1]

        mzs = pms2[:, 0]
        intensities = pms2[:, 1]

        # sort
        idx = np.argsort(mzs)
        mzs = mzs[idx]
        intensities = intensities[idx]

        spectrum = Spectrum(mz=mzs, intensities=intensities,
                            metadata={"precursor_mz": float(row['m/z']),
                                      "name": row['MS1_annotation']})
        spectrum_ls.append(spectrum)

    return spectrum_ls


def main(spectrum_ls):

    df = pd.read_csv(
        '/data/PR000639/output/hilic_pos_aligned_feature_table.tsv',
        sep='\t', low_memory=False)

    # Use factory to construct a similarity function
    cosine_greedy = CosineGreedy(tolerance=0.02)

    for i, spec in enumerate(spectrum_ls):
        prec_mz = spec.get("precursor_mz")
        name = spec.get("compound_name")

        sub_df = df[(df['m/z'] > prec_mz - 0.01) & (df['m/z'] < prec_mz + 0.01) & pd.notnull(df['pseudo_ms2'])]

        if len(sub_df) == 0:
            continue

        for j, row in sub_df.iterrows():
            pms2 = row['pseudo_ms2'].split(';')
            pms2 = [x.split(' ') for x in pms2][:-1]
            pms2 = [[float(x) for x in y] for y in pms2]
            pms2 = np.array(pms2, dtype=np.float32)

            # remove ions larger than precursor
            pms2 = pms2[pms2[:, 0] < prec_mz + 0.1]

            mzs = pms2[:, 0]
            intensities = pms2[:, 1]

            # sort
            idx = np.argsort(mzs)
            mzs = mzs[idx]
            intensities = intensities[idx]

            qry_spec = Spectrum(mz=mzs, intensities=intensities,
                                metadata={"precursor_mz": float(row['m/z'])})

            score = cosine_greedy.pair(spec, qry_spec)

            if score['matches'] > 5 and score['score'] > 0.5:
                spec.plot_against(qry_spec)
                plt.xlim(0, float(row['m/z']) * 1.2)
                plt.show()
                print(f"{name} matched with ID {row['ID']} with score {score['score']:.2f} and {score['matches']} matched peaks")


if __name__ == "__main__":
    spectrum_ls = get_ref_pms2()
    main(spectrum_ls)
