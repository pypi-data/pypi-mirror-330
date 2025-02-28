import pandas as pd
import joblib
import numpy as np


def prepare_qry_spec():
    # ['Name', 'Precursor_type', 'Instrument_type', 'Collision_energy',
    #        'Precursor_mz', 'Formula', 'MW', 'CAS', 'NIST_No', 'Notes',
    #        'Instrument', 'Ionization', 'Collision_gas', 'Sample_inlet',
    #        'Spectrum_type', 'Ion_mode', 'InChIKey', 'Fragment_No', 'MS2mz',
    #        'MS2int', 'Frag_formula', 'Loss_formula']

    df = joblib.load('/Users/shipei/Documents/projects/ms2/ms2_lib/nist20/nist20/nist20.joblib')

    df = pd.DataFrame(df)

    # drop cols of 'Frag_formula', 'Loss_formula'
    df.drop(['Frag_formula', 'Loss_formula'], axis=1, inplace=True)

    df = df[df['Spectrum_type'] == 'MS2']

    # convert 'InChIKey' to str
    df['InChIKey'] = df['InChIKey'].astype(str)

    # print(df['Collision_energy'].value_counts())

    df['cleaned_CE'], df['CE_mode'] = zip(*df['Collision_energy'].apply(_clean_CE))

    # sort by Instrument_type, Ion_mode, InChIKey, Name, Precursor_type, Collision_gas, cleaned_CE, CE_mode
    df = df.sort_values(['Instrument_type', 'Ion_mode', 'InChIKey', 'Name', 'Precursor_type', 'Collision_gas', 'cleaned_CE', 'CE_mode'])

    # deduplicate by Instrument_type, Ion_mode, InChIKey, Name, Precursor_type, Collision_gas, CE_mode, keep first
    df = df.drop_duplicates(subset=['Instrument_type', 'Ion_mode', 'InChIKey', 'Name', 'Precursor_type', 'Collision_gas', 'CE_mode'], keep='first')

    df['peaks'] = df.apply(lambda x: np.array([[float(y) for y in x['MS2mz'].split(';')],
                                               [float(y) for y in x['MS2int'].split(';')]]).T, axis=1)

    # filter
    mask_1 = (df['cleaned_CE'] < 3) & (df['CE_mode'] == 'ev')
    mask_2 = (df['cleaned_CE'] < 3) & (df['CE_mode'] == 'nce')
    df = df[mask_1 | mask_2]
    # df = df[mask_1]

    df = df[df['Precursor_type'].isin(['[M+H]+', '[M-H]-'])]

    df.to_pickle('low_energy_nist20.pkl')
    df.to_csv('low_energy_nist20.tsv', sep='\t', index=False)
    print(df.shape[0])


def _clean_CE(x):
    try:
        return float(x), 'ev'
    except:
        if 'NCE' in x:

            # return float(x.split('=')[1].split('%')[0]), 'nce'

            if 'eV' in x:
                return float(x.split(' ')[1].split('eV')[0]), 'ev'
            else:
                return float(x.split('=')[1].split('%')[0]), 'nce'


def read_mgf_to_df(library_mgf, write_pkl=False, out_path=None):
    """
    Generate a dataframe from mgf file
    """
    with open(library_mgf, 'r') as file:
        spectrum_list = []
        for line in file:
            # empty line
            _line = line.strip()
            if not _line:
                continue
            elif line.startswith('BEGIN IONS'):
                spectrum = {}
                # initialize spectrum
                mz_list = []
                intensity_list = []
            elif line.startswith('END IONS'):
                if len(mz_list) == 0:
                    continue
                spectrum['mz_ls'] = mz_list
                spectrum['intensity_ls'] = intensity_list
                spectrum_list.append(spectrum)
                continue
            else:
                # if line contains '=', it is a key-value pair
                if '=' in _line:
                    # split by first '='
                    key, value = _line.split('=', 1)
                    spectrum[key] = value
                else:
                    # if no '=', it is a spectrum pair
                    this_mz, this_int = _line.split()
                    try:
                        mz_list.append(float(this_mz))
                        intensity_list.append(float(this_int))
                    except:
                        continue

    df = pd.DataFrame(spectrum_list)

    if write_pkl:
        if out_path is None:
            out_path = library_mgf.split('/')[-1].split('.')[0] + '_df.pkl'
        df.to_pickle(out_path)

    return df


if __name__ == '__main__':

    prepare_qry_spec()  # prepare low energy nist20, 5358 spectra

    # prepare nist20, for smiles
    # read_mgf_to_df('/Users/shipei/Documents/projects/ms2/ms2_lib/nist20/nist20/NIST20/NIST20_HR.mgf',
    #                write_pkl=True, out_path='nist20_df.pkl')

