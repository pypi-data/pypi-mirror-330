import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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


def create_mirror_plot(mz_arr, int_arr, pre_mz,
                       mz_arr_ref, int_arr_ref, fig_size=(2.2, 1.0),
                       ms2_tol=0.05, peak_int_power=0.5,
                       intensity_threshold_label=0., label_decimals=2,
                       mz_range=(100, 1000),
                       max_x=None, plot_unmatched_qry=True,
                       matched_peak_color='red',
                       up_spec_peak_color='0.6', down_spec_peak_color='0.2',
                       save=False,
                       output_name='demo.svg'):
    plt.figure(figsize=fig_size)

    int_arr = np.power(int_arr, peak_int_power)
    int_arr_ref = np.power(int_arr_ref, peak_int_power)

    # mz range
    mask = (mz_arr >= mz_range[0]) & (mz_arr <= mz_range[1])
    mz_arr = mz_arr[mask]
    int_arr = int_arr[mask]
    mask = (mz_arr_ref >= mz_range[0]) & (mz_arr_ref <= mz_range[1])
    mz_arr_ref = mz_arr_ref[mask]
    int_arr_ref = int_arr_ref[mask]

    # Find matched peaks
    matched_indices = []
    matched_indices_ref = []
    for i, mz in enumerate(mz_arr):
        matches = np.where(np.abs(mz_arr_ref - mz) <= ms2_tol)[0]
        if matches.size > 0:
            print(f'{mz:.4f} matched to {mz_arr_ref[matches]}')
            matched_indices.extend([i] * len(matches))
            matched_indices_ref.extend(matches)

    # Normalize intensities
    max_intensity = max(int_arr[matched_indices])
    int_arr = int_arr / max_intensity * 100

    max_intensity_ref = max(int_arr_ref[mz_arr_ref < (pre_mz - 0.5)])
    int_arr_ref = int_arr_ref / max_intensity_ref * 100

    # Set axis limits and labels
    if max_x is None:
        max_x = max(np.max(mz_arr), np.max(mz_arr_ref)) * 1.05  # Add 5% margin

    # Plot unmatched peaks
    if plot_unmatched_qry:
        plt.vlines(mz_arr, 0, int_arr, color=up_spec_peak_color, linewidth=1.20)
    plt.vlines(mz_arr_ref, 0, -int_arr_ref, color=down_spec_peak_color, linewidth=1.20)

    # Plot matched peaks
    plt.vlines(mz_arr[matched_indices], 0, int_arr[matched_indices], color=matched_peak_color, linewidth=1.20)
    plt.vlines(mz_arr_ref[matched_indices_ref], 0, -int_arr_ref[matched_indices_ref], color=matched_peak_color,
               linewidth=1.20)

    plt.xlim(0, max_x)
    plt.ylim(-112, 112)

    # Add labels for peaks above threshold
    for mz, intensity in zip(mz_arr, int_arr):
        if intensity >= intensity_threshold_label and mz < max_x:
            plt.text(mz, intensity + 0.1, f'{mz:.{label_decimals}f}', ha='center', va='bottom', fontsize=8,
                     fontname='Arial')

    for mz, intensity in zip(mz_arr_ref, int_arr_ref):
        if intensity >= intensity_threshold_label and mz < max_x:
            plt.text(mz, -intensity - 2, f'{mz:.{label_decimals}f}', ha='center', va='top', fontsize=8,
                     fontname='Arial')

    # plt.xlabel(r'$\mathit{m/z}$', fontname='Arial', fontsize=12, labelpad=2, color='0.2')
    plt.ylabel('Intensity (%)', fontname='Arial', fontsize=9, labelpad=1, color='0.2')

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
    plt.yticks(fontname='Arial', fontsize=8)

    # Adjust tick parameters
    # plt.tick_params(axis='x', pad=4, length=2, color='0.5')
    plt.tick_params(axis='y', pad=0.5, length=1.5, color='0.5')

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


def demo(name, scale):
    df = pd.read_csv(
        '/Users/shipei/Documents/projects/ms1_id/imaging/spotted_stds/2020-12-05_ME_X190_L1_Spotted_20umss_375x450_33at_DAN_Neg/ms1_id_annotations_derep.tsv',
        sep='\t', low_memory=False)

    df['gnps_id'] = df['db_id'].apply(lambda x: x.split('=')[1].split(';')[0])

    idx = df[(df['name'] == name)].index[0]

    print(df.iloc[idx]['name'])
    print(df.iloc[idx]['precursor_mz'])
    print(df.iloc[idx]['matched_score'])
    print(df.iloc[idx]['matched_peak'])
    print(df.iloc[idx]['spectral_usage'])

    ms1 = df.iloc[idx]['pseudo_ms2']
    mz_arr = []
    int_arr = []
    for p in ms1.split(';'):
        p = p.strip()
        if not p:
            continue
        mz, inten = p.split(' ')
        mz_arr.append(float(mz))
        int_arr.append(float(inten))
    mz_arr = np.array(mz_arr)
    int_arr = np.array(int_arr)

    mz_arr_ref, int_arr_ref, _ = gnps_id_to_spec(df.iloc[idx]['gnps_id'])

    mask = (int_arr > max(int_arr) * 0.01) & (mz_arr < df.iloc[idx]['precursor_mz'] + 0.5)
    mz_arr = mz_arr[mask]
    int_arr = int_arr[mask]

    mask = (int_arr_ref > max(int_arr_ref) * 0.01) & (mz_arr_ref < df.iloc[idx]['precursor_mz'] + 0.5)
    mz_arr_ref = mz_arr_ref[mask]
    int_arr_ref = int_arr_ref[mask]

    # scale
    if scale:
        factor = mz_arr_ref / df.iloc[idx]['precursor_mz'] * 10
        int_arr_ref = int_arr_ref * np.exp(factor)

    create_mirror_plot(np.array(mz_arr), np.array(int_arr), df.iloc[idx]['precursor_mz'],
                       np.array(mz_arr_ref), np.array(int_arr_ref),
                       ms2_tol=0.05, peak_int_power=0.5,
                       intensity_threshold_label=1e5,
                       label_decimals=2,
                       plot_unmatched_qry=False,
                       mz_range=(100, 1000),
                       max_x=float(df.iloc[idx]['precursor_mz']) * 1.05,
                       matched_peak_color='#F08976',
                       up_spec_peak_color='0.9', down_spec_peak_color='0.9',
                       fig_size=(2.1, 1),
                       save=True,
                       output_name='ATP.svg')


if __name__ == '__main__':
    # carnosine
    demo("ADENOSINE 5'-TRIPHOSPHATE", scale=True)
