import matplotlib.pyplot as plt
from pyteomics import mzml
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def get_xics(mzml_file, target_mzs, ms_level=1, rt_range=None, mz_tol=0.02):
    """
    Function to extract multiple XICs for given masses, MS level, and retention time period.
    :param mzml_file: Path to the mzML file.
    :param target_mzs: List of target m/z values.
    :param ms_level: MS level to consider (1 or 2).
    :param rt_range: Retention time range as a tuple (start, end). If None, extract for all.
    :param mz_tol: Tolerance for the m/z value.
    :return: Dictionary of XICs and retention times.
    """
    xics = {target_mz: [] for target_mz in target_mzs}
    times = []

    with mzml.read(mzml_file) as reader:
        for spectrum in reader:
            if spectrum['ms level'] == ms_level:
                time = spectrum['scanList']['scan'][0]['scan start time']

                # Check if the retention time is within the specified range
                if rt_range is not None and not (rt_range[0] <= time <= rt_range[1]):
                    continue

                if len(times) == 0 or times[-1] != time:
                    times.append(time)

                mz_array = spectrum['m/z array']
                intensity_array = spectrum['intensity array']

                for target_mz in target_mzs:
                    xic_intensity = np.sum(
                        intensity_array[(mz_array >= target_mz - mz_tol) & (mz_array <= target_mz + mz_tol)])
                    xics[target_mz].append(xic_intensity)

    return times, xics


def plot_xics(times, xics, target_mzs, rt_range=None,
              fig_size=(3, 3), linewidth=2.5,
              y_max=None, x_axis=True,
              legend=True,
              save=False, name='xics.svg'):
    """
    Function to plot XICs.
    :param times: List of retention times.
    :param xics: Dictionary of XICs.
    :param target_mzs: List of target m/z values.
    :param rt_range: Retention time range as a tuple (start, end) in minutes.
    """
    colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95', '#facaa9', '#ca9a96']
    plt.figure(figsize=fig_size)

    if len(target_mzs) > len(colors):
        # Create a custom colormap
        cmap = LinearSegmentedColormap.from_list("custom", colors, N=len(target_mzs))
        color_list = [cmap(i) for i in np.linspace(0, 1, len(target_mzs))]
    else:
        color_list = colors

    for i, target_mz in enumerate(target_mzs):
        plt.plot(np.array(times), xics[target_mz],
                 label=f'$\it{{m/z}}$ {target_mz:.2f}', color=color_list[i % len(color_list)], linewidth=linewidth)

    plt.xlabel('RT (min)', fontname='Arial', fontsize=12, labelpad=4, color='0.2')
    # plt.ylabel('Intensity', fontname='Arial', fontsize=12, labelpad=2, color='0.2')

    if legend:
        plt.legend(prop={'family': 'Arial', 'size': 10})

    if rt_range:
        plt.xlim(rt_range)

    ax = plt.gca()

    # Remove top, right, and left spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set the color of the frame (axes spines)
    for spine in ax.spines.values():
        spine.set_color('0.5')

    ax.yaxis.set_visible(False)

    if not x_axis:
        ax.xaxis.set_visible(False)
        for spine in ax.spines.values():
            spine.set_visible(True)

    # Set the color of tick labels to 0.2
    ax.tick_params(axis='both', colors='0.2')

    if y_max:
        plt.ylim(0, y_max)

    plt.tight_layout()

    if save:
        plt.savefig(name, transparent=True)
    plt.show()


from scipy.signal import savgol_filter
def smooth_xics(xics, window_size=3):
    """
    Function to smooth XICs using a moving average.
    :param xics: Dictionary of XICs.
    :param window: Window size for the moving average.
    :return: Dictionary of smoothed XICs.
    """
    smoothed_xics = {}
    for target_mz, intensities in xics.items():
        smoothed_xics[target_mz] = savgol_filter(intensities, window_size, 2)
    return smoothed_xics


if __name__ == '__main__':

    #############
    target_mzs = [103.06, 107.05, 120.08, 131.05, 149.06, 166.09]

    times, xics = get_xics('/data/nist_samples/data_1/Nist_pool_2_0eV.mzML',
                           target_mzs)

    # smoothing
    xics = smooth_xics(xics, window_size=3)

    plot_xics(times, xics, target_mzs, rt_range=(0.8, 1.1), y_max=None, x_axis=True, legend=False,
              save=False, name='xics1.svg')
    #
    # plot_xics(times, xics, target_mzs, rt_range=(0.8, 1.05), y_max=3e6, x_axis=False, legend=False,
    #           save=True, name='xics2.svg')

    plot_xics(times, xics, target_mzs, rt_range=(0.8, 1.05), y_max=3e6, x_axis=False, legend=True,
              save=False, name='xics3.svg')

    #############
    # target_mzs = [238.1071, 123.0443, 165.0544, 182.0811, 136.0757]
    #
    # times, xics = get_xics('/Users/shipei/Documents/projects/ms1_id/data/nist_samples/data_1/Nist_pool_1_10eV.mzML',
    #                        target_mzs)
    # plot_xics(times, xics, target_mzs, fig_size=(10, 6), linewidth=1.5,
    #           rt_range=(0.6, 0.8), y_max=5e7, x_axis=True, legend=True,
    #           save=False, name='xics_.svg')
