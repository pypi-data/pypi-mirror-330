import matplotlib.pyplot as plt
from pyteomics import mzml
import numpy as np
import pickle
import pandas as pd
from flash_cos import FlashCos
from molmass import Formula


_adduct_pos = [
    {'name': '[M+H]+', 'm': 1, 'charge': 1, 'mass': 1.00727645223},
    {'name': '[M+Na]+', 'm': 1, 'charge': 1, 'mass': 22.989220702},
    {'name': '[M+K]+', 'm': 1, 'charge': 1, 'mass': 38.9631579064},
    {'name': '[M+NH4]+', 'm': 1, 'charge': 1, 'mass': 18.03382555335},
    {'name': '[M+H-H2O]+', 'm': 1, 'charge': 1, 'mass': -17.0032882318},
    {'name': '[2M+H]+', 'm': 2, 'charge': 1, 'mass': 1.00727645223},
    {'name': '[2M+Na]+', 'm': 2, 'charge': 1, 'mass': 22.989220702},
    {'name': '[2M+K]+', 'm': 2, 'charge': 1, 'mass': 38.9631579064},
    {'name': '[2M+NH4]+', 'm': 2, 'charge': 1, 'mass': 18.03382555335},
    {'name': '[M+2H]2+', 'm': 1, 'charge': 2, 'mass': 2.01455290446},
]


def make_library_main(peak_scale_k=8):
    db_ls = []
    db_ls1 = make_library('/data/std_mix/data_2/mixture_Drugs_DDA.mzML',
                          '/data/std_mix/drug_std.tsv')
    print('Drugs:', len(db_ls1))
    db_ls2 = make_library('/data/std_mix/data_2/mixture_Bile_acids_DDA.mzML',
                          '/data/std_mix/BA_std.tsv')
    print('BA:', len(db_ls2))
    db_ls3 = make_library('/data/std_mix/data_2/sixmix_2_DDA.mzML',
                          '/data/std_mix/six_std.tsv')
    print('Six:', len(db_ls3))

    db_ls.extend(db_ls1)
    db_ls.extend(db_ls2)
    db_ls.extend(db_ls3)

    if peak_scale_k is not None:
        out_name = f'/Users/shipei/Documents/projects/ms1_id/data/std_mix/std_k{peak_scale_k}.pkl'
    else:
        out_name = '/Users/shipei/Documents/projects/ms1_id/data/std_mix/std.pkl'

    index_library(db_ls, out_name, peak_scale_k)


def make_library(mzml_file, tsv_file):
    db_ls = []

    df = pd.read_csv(tsv_file, sep='\t', low_memory=False)
    df['neutral_mass'] = df['formula'].apply(calc_exact_mass)

    with mzml.read(mzml_file) as reader:
        spectra = list(reader)

    for i, row in df.iterrows():
        for adduct in _adduct_pos:
            adduct_mz = (row['neutral_mass'] * adduct['m'] + adduct['mass']) / adduct['charge']
            spectrum = find_closest_ms2(spectra, adduct_mz, row['rt'], rt_tolerance=0.05, mass_tolerance=0.01)

            if spectrum is not None:
                peaks = np.column_stack((spectrum['m/z array'], spectrum['intensity array']))

                db_ls.append({
                    'id': f"{i}_{adduct['name']}",
                    'name': row['name'],
                    'precursor_mz': adduct_mz,
                    'formula': row['formula'],
                    'precursor_type': adduct['name'],
                    'ion_mode': 'positive',
                    'original_peaks': peaks,
                    'peaks': peaks
                })

    return db_ls


def index_library(db_ls, out_name, peak_scale_k):
    mz_tol = 0.05

    search_engine = FlashCos(max_ms2_tolerance_in_da=mz_tol * 1.005,
                             mz_index_step=0.0001,
                             peak_scale_k=peak_scale_k,
                             peak_intensity_power=0.5)
    print('building index')
    search_engine.build_index(db_ls,
                              max_indexed_mz=1000,
                              precursor_ions_removal_da=0.5,
                              noise_threshold=0.0,
                              min_ms2_difference_in_da=mz_tol * 2.02,
                              clean_spectra=True)

    # save as pickle
    with open(out_name, 'wb') as file:
        # Dump the data into the file
        pickle.dump(search_engine, file)


def calc_exact_mass(formula):
    """
    Calculate the exact mass for a given formula string
    """
    try:
        f = Formula(formula)
        return f.monoisotopic_mass
    except:
        return None


def find_closest_ms2(spectra, target_mz, target_rt, rt_tolerance=0.05, mass_tolerance=0.01):
    closest_spectrum = None
    min_rt_diff = float('inf')

    for spectrum in spectra:
        if spectrum['ms level'] != 2:
            continue

        rt = spectrum.get('scanList', {}).get('scan', [{}])[0].get('scan start time', 0)
        if abs(rt - target_rt) > rt_tolerance:
            continue

        precursor_mz = \
        spectrum.get('precursorList', {}).get('precursor', [{}])[0].get('selectedIonList', {}).get('selectedIon', [{}])[
            0].get('selected ion m/z')
        if precursor_mz is None or abs(precursor_mz - target_mz) > mass_tolerance:
            continue

        rt_diff = abs(rt - target_rt)
        if rt_diff < min_rt_diff:
            closest_spectrum = spectrum
            min_rt_diff = rt_diff

    return closest_spectrum


def get_spectrum_by_scan(mzml_file, scan_number):
    """
    Function to get a spectrum by scan number from an mzML file.
    :param mzml_file: Path to the mzML file.
    :param scan_number: The scan number of the spectrum to retrieve.
    :return: A dictionary containing the m/z array, intensity array, and metadata of the spectrum.
    """
    with mzml.read(mzml_file) as reader:
        for spectrum in reader:
            if spectrum['index'] + 1 == scan_number:  # mzML scan numbers are 1-based, but index is 0-based
                return {
                    'mz': np.array(spectrum['m/z array']),
                    'intensity': np.array(spectrum['intensity array'])
                }

    return None


def plot_spectrum(spectrum):
    """
    Function to plot a spectrum.
    :param spectrum: A dictionary containing 'm/z array' and 'intensity array'.
    """
    plt.figure(figsize=(10, 6))
    plt.vlines(spectrum['mz'], 0, spectrum['intensity'])
    plt.xlabel('m/z')
    plt.ylabel('Intensity')
    plt.show()


if __name__ == '__main__':
    make_library_main(peak_scale_k=0)
    # make_library_main(peak_scale_k=3)
    # make_library_main(peak_scale_k=5)
    # make_library_main(peak_scale_k=8)
    # make_library_main(peak_scale_k=9)
    make_library_main(peak_scale_k=10)
    # make_library_main(peak_scale_k=13)
    # make_library_main(peak_scale_k=15)
    # make_library_main(peak_scale_k=18)

