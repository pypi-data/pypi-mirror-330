import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import math
import pandas as pd
from requests import get
from json import loads
import time
from functools import wraps


def retry_on_exception(max_attempts=5, delay=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def usi_to_spec(usi):
    # get spectrum from USI
    url = 'https://metabolomics-usi.gnps2.org/json/?usi1=' + usi
    response = get(url, timeout=30)
    json_data = loads(response.text)
    ms2_mz = np.array(json_data['peaks'])[:, 0]
    ms2_int = np.array(json_data['peaks'])[:, 1]
    return ms2_mz, ms2_int, json_data['precursor_mz']


@retry_on_exception(max_attempts=5, delay=0.1)
def gnps_id_to_spec(gnps_id):
    usi = f'mzspec:GNPS:GNPS-LIBRARY:accession:{gnps_id}'
    return usi_to_spec(usi)

def create_single_plot(ax,
                       mz_arr, int_arr, prec_mz,
                       mz_arr_ref, int_arr_ref,
                       max_x, mz_range=(100, 1200),
                       ref_scale=0,
                       query_matched_only=False,
                       ms2_tol=0.05, peak_int_power=1.0,
                       plot_info=None, plot_title=None):
    int_arr = np.power(int_arr, peak_int_power)
    int_arr_ref = np.power(int_arr_ref, peak_int_power)

    # mz range
    mask = (mz_arr >= mz_range[0]) & (mz_arr <= min(mz_range[1], max_x))
    mz_arr = mz_arr[mask]
    int_arr = int_arr[mask]
    mask = (mz_arr_ref >= mz_range[0]) & (mz_arr_ref <= min(mz_range[1], max_x))
    mz_arr_ref = mz_arr_ref[mask]
    int_arr_ref = int_arr_ref[mask]

    # Scale ref MS2
    factor = mz_arr_ref / prec_mz
    int_arr_ref = int_arr_ref * np.exp(ref_scale * factor)

    # Find matched peaks
    matched_indices = []
    matched_indices_ref = []
    for i, mz in enumerate(mz_arr):
        matches = np.where(np.abs(mz_arr_ref - mz) <= ms2_tol)[0]
        if matches.size > 0:
            matched_indices.extend([i] * len(matches))
            matched_indices_ref.extend(matches)

    # Normalize intensities for pseudo MS2
    if matched_indices:
        max_matched_intensity = max(int_arr[matched_indices])
        int_arr = int_arr / max_matched_intensity * 100
    else:
        # If no matches, normalize by the overall maximum
        int_arr = int_arr / max(int_arr) * 100

    # Normalize intensities for ref MS2
    max_intensity_ref = max(int_arr_ref)
    int_arr_ref = int_arr_ref / max_intensity_ref * 100

    # Plot unmatched peaks
    if not query_matched_only:
        ax.vlines(mz_arr, 0, int_arr, color='0.7', linewidth=0.6)
    ax.vlines(mz_arr_ref, 0, -int_arr_ref, color='0.7', linewidth=0.6)

    # Plot matched peaks
    ax.vlines(mz_arr[matched_indices], 0, int_arr[matched_indices], color='#F08976', linewidth=0.7)
    ax.vlines(mz_arr_ref[matched_indices_ref], 0, -int_arr_ref[matched_indices_ref], color='#F08976', linewidth=0.7)

    ax.set_xlim(0, max_x)
    ax.set_ylim(-120, 120)

    ax.set_xlabel(r'$\mathit{m/z}$', fontname='Arial', fontsize=8, labelpad=2, color='0.2')
    ax.set_ylabel('Intensity (%)', fontname='Arial', fontsize=8, labelpad=2, color='0.2')

    # Add "Pseudo MS2" and "Ref. MS2" labels
    ax.text(0.02, 0.95, 'Pseudo MS2', transform=ax.transAxes, ha='left', va='top', fontsize=7, color='0.2')
    ax.text(0.02, 0.20, 'Ref. MS2', transform=ax.transAxes, ha='left', va='bottom', fontsize=7, color='0.2')

    # Add plot information above "Ref. MS2" label
    if plot_info:
        ax.text(0.02, 0.30, plot_info, transform=ax.transAxes, ha='left', va='bottom', fontsize=5.5, color='0.2')

    ax.xaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color('0.5')

    ax.grid(False)
    ax.axhline(y=0, color='0.5', linewidth=0.5)

    ax.tick_params(axis='y', pad=2, length=2, color='0.5')
    ax.tick_params(axis='both', colors='0.2')

    yticks = ax.get_yticks()
    yticks = [y for y in yticks if abs(y) <= 100]
    ax.set_yticks(yticks)
    ax.set_yticklabels([str(abs(int(y))) for y in yticks], fontsize=6)

    # Add plot title if provided
    if plot_title:
        ax.set_title(plot_title, fontsize=8, pad=2, wrap=True)


def plot_multiple_figures(annotation_file, output_pdf_name='multiple_plots.pdf',
                          min_score=0.7, min_matched_peak=3, min_spectral_usage=0.15, peak_int_power=1.0,
                          rows=5, cols=2):
    df = pd.read_csv(annotation_file, sep='\t', low_memory=False)

    df = df.sort_values(['mz', 'matched_score'], ascending=[True, False])
    # df = df.sort_values(['spectral_usage', 'matched_score', 'matched_peak'], ascending=[False, False, False])

    df['gnps_id'] = df['db_id'].apply(lambda x: x.split('=')[1].split(';')[0])

    # Filter by score, matched peak, and spectral usage
    df = df[(df['matched_score'] >= min_score) &
            (df['matched_peak'] >= min_matched_peak) &
            (df['spectral_usage'] >= min_spectral_usage)].reset_index(drop=True)

    print(f"Loaded {len(df)} annotations from {annotation_file}")

    with PdfPages(output_pdf_name) as pdf:
        num_plots = len(df)
        plots_per_page = rows * (cols // 2)  # Each spectrum takes 2 columns

        for page in range(math.ceil(num_plots / plots_per_page)):
            start_idx = page * plots_per_page
            end_idx = min((page + 1) * plots_per_page, num_plots)
            plots_on_page = end_idx - start_idx

            # Calculate the number of rows needed for this page
            rows_on_page = math.ceil(plots_on_page / (cols // 2))

            # Create figure with extra space at the top of each row for titles
            fig, axs = plt.subplots(rows_on_page, cols, figsize=(cols * 6, rows_on_page * 2.3))
            fig.subplots_adjust(hspace=0.5, wspace=0.3, top=0.95)

            # Ensure axs is always a 2D array
            if rows_on_page == 1:
                axs = axs.reshape(1, -1)

            for i in range(plots_on_page):
                idx = start_idx + i
                row = i // (cols // 2)
                col = (i % (cols // 2)) * 2

                print('Processing', idx, df.iloc[idx]['name'])
                ms1 = df.iloc[idx]['pseudo_ms2']
                mz_arr = []
                int_arr = []
                for p in ms1.split(';'):
                    p = p.strip()
                    if not p:
                        continue
                    mz, inten = p.split(' ')
                    if float(inten) > 0:
                        mz_arr.append(float(mz))
                        int_arr.append(float(inten))

                mz_arr_ref, int_arr_ref, _ = gnps_id_to_spec(df.iloc[idx]['gnps_id'])
                # add precursor m/z for visualization
                if np.min(np.abs(mz_arr_ref - df.iloc[idx]['precursor_mz'])) > 0.05:
                    mz_arr_ref = np.append(mz_arr_ref, df.iloc[idx]['precursor_mz'])
                    int_arr_ref = np.append(int_arr_ref, 0.01)

                prec_mz = float(df.iloc[idx]['precursor_mz'])

                # Prepare plot information
                plot_info = f"Score: {df.iloc[idx]['matched_score']:.2f}\n" \
                            f"Matched: {df.iloc[idx]['matched_peak']} (w/o precursor)\n" \
                            f"Usage: {df.iloc[idx]['spectral_usage']:.2f}"

                # Prepare plot title
                metabolite_name = df.iloc[idx]['name']
                mz_value = df.iloc[idx]['precursor_mz']
                precursor_type = df.iloc[idx]['precursor_type']
                plot_title = f"{metabolite_name}\nm/z: {mz_value:.4f}, {precursor_type}"

                if metabolite_name == 'PC(0:0/18:0); [M+H]+ C26H55N1O7P1':
                    print('PC(0:0/18:0); [M+H]+ C26H55N1O7P1')

                # Original plot
                create_single_plot(axs[row, col], np.array(mz_arr), np.array(int_arr), prec_mz,
                                   np.array(mz_arr_ref), np.array(int_arr_ref), prec_mz + 2,
                                   ref_scale=0,
                                   peak_int_power=peak_int_power,
                                   query_matched_only=True,
                                   plot_info=plot_info, plot_title=plot_title)
                axs[row, col].set_title(plot_title, fontsize=6.5, pad=2, wrap=True)
                axs[row, col].text(0.5, 0.88, "Non-scaled", transform=axs[row, col].transAxes, ha='center', va='bottom',
                                   fontsize=6)

                # Square root plot
                create_single_plot(axs[row, col + 1], np.array(mz_arr), np.array(int_arr), prec_mz,
                                   np.array(mz_arr_ref), np.array(int_arr_ref), prec_mz + 2,
                                   ref_scale=10,
                                   peak_int_power=peak_int_power,
                                   query_matched_only=True,
                                   plot_info=plot_info, plot_title=plot_title)
                axs[row, col + 1].set_title(plot_title, fontsize=6.5, pad=2, wrap=True)
                axs[row, col + 1].text(0.5, 0.88, "Scaled", transform=axs[row, col + 1].transAxes, ha='center',
                                       va='bottom', fontsize=6)

            # Remove any unused subplots
            for i in range(plots_on_page, rows_on_page * (cols // 2)):
                row = i // (cols // 2)
                col = (i % (cols // 2)) * 2
                fig.delaxes(axs[row, col])
                fig.delaxes(axs[row, col + 1])

            pdf.savefig(fig)
            plt.close(fig)

    print(f"PDF saved as {output_pdf_name}")


if __name__ == '__main__':
    min_score = 0.7
    min_matched_peak = 4
    min_spectral_usage = 0.05

    # file_name = '/Users/shipei/Documents/projects/ms1_id/bin/msi/analysis/mouse_brain/all_brain_annotations.tsv'
    # plot_multiple_figures(file_name, 'all_brain_mirror_plot.pdf', min_score, min_matched_peak, min_spectral_usage)

    file_name = '/bin/ms1id/msi/analysis/mouse_brain/all_brain_annotations_verified.tsv'
    plot_multiple_figures(file_name, 'all_brain_verified_sqrt_mirror_plot.pdf',
                          min_score,
                          min_matched_peak,
                          min_spectral_usage,
                          peak_int_power=0.5)
    plot_multiple_figures(file_name, 'all_brain_verified_mirror_plot.pdf',
                          min_score,
                          min_matched_peak,
                          min_spectral_usage,
                          peak_int_power=1)

    # file_name = '/Users/shipei/Documents/projects/ms1_id/imaging/mouse_body/wb xenograft in situ metabolomics test - rms_corrected/ms1_id_annotations_derep.tsv'
    # plot_multiple_figures(file_name, 'mouse_body_mirror_plot.pdf', min_score, min_matched_peak, min_spectral_usage)
    #
    # file_name = '/Users/shipei/Documents/projects/ms1_id/imaging/mouse_kidney/mouse kidney - root mean square - metaspace/ms1_id_annotations_derep.tsv'
    # plot_multiple_figures(file_name, 'mouse_kidney_mirror_plot.pdf', min_score, min_matched_peak, min_spectral_usage)
    #
    # file_name = '/Users/shipei/Documents/projects/ms1_id/imaging/mouse_liver/Mouse liver_DMAN_200x200_25um/ms1_id_annotations_derep.tsv'
    # plot_multiple_figures(file_name, 'mouse_liver_mirror_plot.pdf', min_score, min_matched_peak, min_spectral_usage)
