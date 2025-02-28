import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

from json import loads as loads
from requests import get


def usi_to_spec(usi):
    # get spectrum from USI
    url = 'https://metabolomics-usi.gnps2.org/json/?usi1=' + usi
    response = get(url)
    json_data = loads(response.text)
    ms2_mz = np.array(json_data['peaks'])[:, 0]
    ms2_int = np.array(json_data['peaks'])[:, 1]

    return ms2_mz, ms2_int, json_data['precursor_mz']


def gnps_id_to_spec(gnps_id):
    usi = f'mzspec:GNPS:GNPS-LIBRARY:accession:{gnps_id}'
    return usi_to_spec(usi)


def create_mirror_plot(mz_arr, int_arr, premz,
                       mz_arr_ref, int_arr_ref, premz_ref,
                       ms2_tol=0.05, peak_int_power=0.5,
                       intensity_threshold_label=0, label_decimals=2,
                       max_x=None,
                       matched_peak_color='red',
                       up_spec_peak_color='0.6', down_spec_peak_color='0.6',
                       save=False,
                       output_name='demo.svg'):

    plt.figure(figsize=(4.5, 2.2))

    # Set axis limits and labels
    if max_x is None:
        max_x = max(premz, premz_ref) * 1.05  # Add 5% margin

    int_arr = np.power(int_arr, peak_int_power)
    int_arr_ref = np.power(int_arr_ref, peak_int_power)

    # Normalize intensities
    max_intensity = max(int_arr[mz_arr < max_x])
    int_arr = int_arr / max_intensity * 100

    max_intensity_ref = max(int_arr_ref[mz_arr_ref < max_x])
    int_arr_ref = int_arr_ref / max_intensity_ref * 100

    # Find matched peaks
    matched_indices = []
    matched_indices_ref = []
    for i, mz in enumerate(mz_arr):
        matches = np.where(np.abs(mz_arr_ref - mz) <= ms2_tol)[0]
        if matches.size > 0:
            print(f'{mz:.4f} matched to {mz_arr_ref[matches]}')
            matched_indices.extend([i] * len(matches))
            matched_indices_ref.extend(matches)

    # Plot unmatched peaks
    plt.vlines(mz_arr, 0, int_arr, color=up_spec_peak_color, linewidth=1.5)
    plt.vlines(mz_arr_ref, 0, -int_arr_ref, color=down_spec_peak_color, linewidth=1.5)

    # Plot matched peaks
    plt.vlines(mz_arr[matched_indices], 0, int_arr[matched_indices], color=matched_peak_color, linewidth=1.5)
    plt.vlines(mz_arr_ref[matched_indices_ref], 0, -int_arr_ref[matched_indices_ref], color=matched_peak_color,
               linewidth=1.5)

    # Add dashed lines for premz and premz_ref
    plt.vlines(premz, 0, 100, color='blue', linestyle='--', linewidth=1)
    plt.vlines(premz_ref, 0, -100, color='blue', linestyle='--', linewidth=1)

    plt.xlim(0, max_x)
    plt.ylim(-110, 110)

    # Add labels for peaks above threshold
    for mz, intensity in zip(mz_arr, int_arr):
        if intensity >= intensity_threshold_label and mz < max_x:
            plt.text(mz, intensity + 0.1, f'{mz:.{label_decimals}f}', ha='center', va='bottom', fontsize=8, fontname='Arial')

    for mz, intensity in zip(mz_arr_ref, int_arr_ref):
        if intensity >= intensity_threshold_label and mz < max_x:
            plt.text(mz, -intensity - 2, f'{mz:.{label_decimals}f}', ha='center', va='top', fontsize=8, fontname='Arial')

    plt.xlabel(r'$\mathit{m/z}$', fontname='Arial', fontsize=12, labelpad=2, color='0.2')
    plt.ylabel('Intensity (%)', fontname='Arial', fontsize=12, labelpad=2, color='0.2')

    plt.gca().xaxis.set_visible(False)

    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    # Set the color of the frame (axes spines)
    for spine in plt.gca().spines.values():
        spine.set_color('0.5')

    # Remove grid
    plt.grid(False)

    # Add line at y=0
    plt.axhline(y=0, color='0.5', linewidth=1)

    # Use Helvetica font for tick labels
    # plt.xticks(fontname='Arial', fontsize=10)
    plt.yticks(fontname='Arial', fontsize=10)

    # Adjust tick parameters
    plt.tick_params(axis='x', pad=4, length=2, color='0.5')
    plt.tick_params(axis='y', pad=2.5, length=2, color='0.5')

    # Set the color of tick labels to 0.2
    plt.gca().tick_params(axis='both', colors='0.2')

    # Modify y-axis ticks and labels
    yticks = plt.gca().get_yticks()
    yticks = [y for y in yticks if abs(y) <= 100]
    plt.gca().set_yticks(yticks)
    plt.gca().set_yticklabels([str(abs(int(y))) for y in yticks])

    # Save the plot
    plt.tight_layout()
    if save:
        plt.savefig(output_name, transparent=True)
    plt.show()
    plt.close()


def demo(idx_1, idx_2):
    df = pd.read_csv(
        '/data/PR000639/output/hilic_pos_aligned_feature_table.tsv',
        sep='\t', low_memory=False)

    df = df[df['MS1_similarity'].notnull()].reset_index(drop=True)

    df['gnps_id'] = df['MS1_db_id'].apply(lambda x: x.split('=')[1].split(';')[0])

    idx_1 = df[df['ID'] == idx_1].index[0]
    idx_2 = df[df['ID'] == idx_2].index[0]

    ms2 = df.iloc[idx_1]['pseudo_ms2']
    mz_arr1 = []
    int_arr1 = []
    for p in ms2.split(';'):
        p = p.strip()
        if not p:
            continue
        mz, inten = p.split(' ')
        mz_arr1.append(float(mz))
        int_arr1.append(float(inten))

    ms2 = df.iloc[idx_2]['pseudo_ms2']
    mz_arr2 = []
    int_arr2 = []
    for p in ms2.split(';'):
        p = p.strip()
        if not p:
            continue
        mz, inten = p.split(' ')
        mz_arr2.append(float(mz))
        int_arr2.append(float(inten))

    # alpha = np.array(mz_arr) / float(df.iloc[idx]['m/z']) * 5
    # int_arr = np.array(int_arr) / np.exp(alpha)

    create_mirror_plot(np.array(mz_arr1), np.array(int_arr1), float(df.iloc[idx_1]['m/z']),
                       np.array(mz_arr2), np.array(int_arr2), float(df.iloc[idx_2]['m/z']),
                       ms2_tol=0.05, peak_int_power=1.0,
                       intensity_threshold_label=30,
                       label_decimals=2,
                       max_x=None,
                       matched_peak_color='#F08976',
                       up_spec_peak_color='0.75', down_spec_peak_color='0.65',
                       save=True,
                       output_name='demo.svg')


if __name__ == '__main__':

    demo(280, 19042)

