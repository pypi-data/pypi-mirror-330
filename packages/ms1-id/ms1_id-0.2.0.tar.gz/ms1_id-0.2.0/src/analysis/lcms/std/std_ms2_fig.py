import pickle

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_single_spectrum(mz_arr, int_arr, fig_size=(3.6, 1.5),
                         peak_int_power=0.5,
                         intensity_threshold_label=0, label_decimals=2,
                         max_x=None,
                         peak_color='0.2',
                         save=False,
                         output_name='single_spectrum.svg'):
    plt.figure(figsize=fig_size)

    int_arr = np.power(int_arr, peak_int_power)

    # Normalize intensities
    max_intensity = max(int_arr[mz_arr < max_x])
    int_arr = int_arr / max_intensity * 100

    # Set axis limits
    if max_x is None:
        max_x = np.max(mz_arr) * 1.05  # Add 5% margin

    # Plot peaks
    plt.vlines(mz_arr, 0, int_arr, color=peak_color, linewidth=1.5)

    plt.xlim(0, max_x)
    plt.ylim(0, 110)

    # Add labels for peaks above threshold
    for mz, intensity in zip(mz_arr, int_arr):
        if intensity >= intensity_threshold_label and mz < max_x:
            plt.text(mz, intensity + 0.1, f'{mz:.{label_decimals}f}', ha='center', va='bottom', fontsize=8,
                     fontname='Arial')

    plt.xlabel(r'$\mathit{m/z}$', fontname='Arial', fontsize=12, labelpad=2, color='0.2')
    plt.ylabel('Intensity (%)', fontname='Arial', fontsize=12, labelpad=2, color='0.2')

    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    # Set the color of the frame (axes spines)
    for spine in plt.gca().spines.values():
        spine.set_color('0.5')

    # Remove grid
    plt.grid(False)

    # Use Arial font for tick labels
    plt.xticks(fontname='Arial', fontsize=10)
    plt.yticks(fontname='Arial', fontsize=10)

    # Adjust tick parameters
    plt.tick_params(axis='x', pad=4, length=2, color='0.5')
    plt.tick_params(axis='y', pad=2.5, length=2, color='0.5')

    # Set the color of tick labels to 0.2
    plt.gca().tick_params(axis='both', colors='0.2')

    # Modify y-axis ticks and labels
    yticks = plt.gca().get_yticks()
    yticks = [y for y in yticks if y <= 100]
    plt.gca().set_yticks(yticks)
    plt.gca().set_yticklabels([str(int(y)) for y in yticks])

    # Save the plot
    plt.tight_layout()
    if save:
        plt.savefig(output_name, transparent=True)
    plt.show()
    plt.close()


def create_mirror_plot(mz_arr, int_arr, mz_arr_ref, int_arr_ref, fig_size=(3.6, 2.2),
                       ms2_tol=0.05, peak_int_power=0.5,
                       intensity_threshold_label=0, label_decimals=2,
                       max_x=None,
                       matched_peak_color='red',
                       up_spec_peak_color='0.6', down_spec_peak_color='0.2',
                       show_unmatched_peaks=True,
                       save=False,
                       output_name='demo.svg'):
    plt.figure(figsize=fig_size)

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

    # Set axis limits and labels
    if max_x is None:
        max_x = max(np.max(mz_arr), np.max(mz_arr_ref)) * 1.05  # Add 5% margin

    # Plot unmatched peaks
    if show_unmatched_peaks:
        plt.vlines(mz_arr, 0, int_arr, color=up_spec_peak_color, linewidth=1.5)
        plt.vlines(mz_arr_ref, 0, -int_arr_ref, color=down_spec_peak_color, linewidth=1.5)

    # Plot matched peaks
    plt.vlines(mz_arr[matched_indices], 0, int_arr[matched_indices], color=matched_peak_color, linewidth=1.5)
    plt.vlines(mz_arr_ref[matched_indices_ref], 0, -int_arr_ref[matched_indices_ref], color=matched_peak_color,
               linewidth=1.5)

    plt.xlim(0, max_x)
    plt.ylim(-110, 110)

    # Add labels for peaks above threshold
    for mz, intensity in zip(mz_arr, int_arr):
        if intensity >= intensity_threshold_label and mz < max_x:
            plt.text(mz, intensity + 0.1, f'{mz:.{label_decimals}f}', ha='center', va='bottom', fontsize=8,
                     fontname='Arial')

    for mz, intensity in zip(mz_arr_ref, int_arr_ref):
        if intensity >= intensity_threshold_label and mz < max_x:
            plt.text(mz, -intensity - 2, f'{mz:.{label_decimals}f}', ha='center', va='top', fontsize=8,
                     fontname='Arial')

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
    # plt.tick_params(axis='x', pad=4, length=2, color='0.5')
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


def get_ref_spec(std_k0, std_k10, annotation, precursor_type, db_name):
    if db_name == 'std_k0.pkl':
        eng = std_k0
    elif db_name == 'std_k10.pkl':
        eng = std_k10
    else:
        raise ValueError(f'Unknown database name: {db_name}')

    for spec in eng:
        if spec['name'] == annotation and spec['precursor_type'] == precursor_type:
            mz_arr_ref = spec['peaks'][:, 0]
            int_arr_ref = spec['peaks'][:, 1]
            return mz_arr_ref, int_arr_ref

    raise ValueError(f'No reference spectrum found for {annotation} ({precursor_type})')


def demo(name, index, file='mixture_Bile_acids_20eV'):
    df = pd.read_csv(
        f'output_all/{file}_feature_table.tsv', sep='\t', low_memory=False)

    df = df[df['MS1_similarity'].notnull()]
    df = df[df['MS1_matched_peak'] >= 4].reset_index(drop=True)
    df = df.sort_values('MS1_similarity', ascending=False).reset_index(drop=True)

    if name is not None:
        idx = df[df['MS1_annotation'] == name].index[index]
    else:
        idx = index

    print(df.iloc[idx]['MS1_annotation'])
    print(df.iloc[idx]['MS1_precursor_type'])
    print(df.iloc[idx]['m/z'])
    print(df.iloc[idx]['MS1_similarity'])
    print(df.iloc[idx]['MS1_matched_peak'])

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

    # load search engine
    with open('/data/std_mix/std_k0.pkl', 'rb') as file:
        std_k0 = pickle.load(file)
    with open('/data/std_mix/std_k10.pkl', 'rb') as file:
        std_k10 = pickle.load(file)

    # mz_arr_ref, int_arr_ref = get_ref_spec(std_k0, std_k10,
    #                                        df.iloc[idx]['MS1_annotation'],
    #                                        df.iloc[idx]['MS1_precursor_type'],
    #                                        df.iloc[idx]['MS1_db_name'])

    mz_arr_ref, int_arr_ref = get_ref_spec(std_k0, std_k10,
                                           df.iloc[idx]['MS1_annotation'],
                                           df.iloc[idx]['MS1_precursor_type'],
                                           'std_k0.pkl')

    # Create a mask for mz values in mz_arr that have a close match in mz_arr_ref
    mask = np.any(np.abs(mz_arr[:, np.newaxis] - mz_arr_ref) <= 0.02, axis=1)

    print('len(mz_arr):', len(mz_arr))

    # Apply the mask to both mz_arr and int_arr
    mz_arr = mz_arr[mask]
    print('len(mz_arr):', len(mz_arr))
    int_arr = int_arr[mask]

    alpha = np.array(mz_arr_ref) / float(df.iloc[idx]['m/z']) * 10
    int_arr_ref = np.array(int_arr_ref) * np.exp(alpha)

    create_mirror_plot(np.array(mz_arr), np.array(int_arr),
                       np.array(mz_arr_ref), np.array(int_arr_ref),
                       #fig_size=(12, 6),
                       ms2_tol=0.02, peak_int_power=1,
                       intensity_threshold_label=101,
                       label_decimals=2,
                       # max_x=float(df.iloc[idx]['m/z']) * 0.99,
                       max_x=float(df.iloc[idx]['m/z']) * 1.02,
                       matched_peak_color='#F08976',
                       # matched_peak_color='0.65',
                       up_spec_peak_color='0.75', down_spec_peak_color='0.65',
                       show_unmatched_peaks=True,
                       save=True,
                       output_name='demo2.svg')

    # plot_single_spectrum(mz_arr, int_arr,
    #                      fig_size=(3.6, 1.7),
    #                      peak_int_power=0.5,
    #                      intensity_threshold_label=101, label_decimals=2,
    #                      max_x=float(df.iloc[idx]['m/z']) * 1.05,
    #                      peak_color='#aa3e53',
    #                      save=True,
    #                      output_name='sulfadimethoxine3.svg')


if __name__ == '__main__':

    # mixture_Bile_acids_20eV
    # mixture_Drugs_20eV
    # sixmix_2_20eV

    demo(None, 0, 'mixture_Drugs_20eV')
    # demo(None, 0, 'sixmix_2_10eV')

    # demo('venlafaxine', 0, 'mixture_Drugs_20eV')
    # demo('sulfadimethoxine', 0, 'sixmix_2_20eV')
    # demo('Taurolithocholic acid', 2, 'mixture_Bile_acids_20eV')

    # cosine between two vectors
    def scale(peaks, prec_mz):
        scaling_factor = peaks[:, 0] / prec_mz * 10
        # print('scaling_factor:', scaling_factor)
        return peaks[:, 1] * np.exp(scaling_factor)


    def cosine_similarity(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


    print(cosine_similarity(np.array([3, 7, 5, 4, 8, 17, 0, 0, 0, 0, 0]),
                            np.array([3, 7, 5, 4, 8, 17, 11, 4, 14, 6, 5])))
