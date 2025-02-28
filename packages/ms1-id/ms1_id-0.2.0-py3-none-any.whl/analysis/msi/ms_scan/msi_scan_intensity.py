import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
from numba import njit
from pyimzml.ImzMLParser import ImzMLParser


def get_spectrum_from_imzml(imzml_file, coordinate=None, index=None):
    """
    Get a spectrum from an imzML file by coordinate or index.
    Prints out the coordinate range of the imzML file.

    Parameters:
    - imzml_file (str): Path to the imzML file.
    - coordinate (tuple): (x, y) coordinate of the spectrum to retrieve.
    - index (int): Index of the spectrum to retrieve.

    Returns:
    - mzs (np.array): m/z values of the spectrum.
    - intensities (np.array): Intensity values of the spectrum.

    Note: Provide either coordinate or index, not both.
    """
    if coordinate is None and index is None:
        raise ValueError("Must provide either coordinate or index.")
    if coordinate is not None and index is not None:
        raise ValueError("Provide either coordinate or index, not both.")

    # Parse the imzML file
    imzml = ImzMLParser(imzml_file)

    # Get coordinate range
    x_coords, y_coords, _ = zip(*imzml.coordinates)
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    print(f"Coordinate range: X: {x_min} to {x_max}, Y: {y_min} to {y_max}")
    print(f"Total number of spectra: {len(imzml.coordinates)}")

    if coordinate is not None:
        x, y = coordinate
        # Find the index of the spectrum at the given coordinate
        for idx, (x_, y_, _) in enumerate(imzml.coordinates):
            if x_ == x and y_ == y:
                index = idx
                break
        else:
            raise ValueError(f"No spectrum found at coordinate ({x}, {y})")

    # Get the spectrum at the specified index
    mzs, intensities = imzml.getspectrum(index)

    return np.array(mzs), np.array(intensities)


@njit
def apply_moving_average_numba(mz_array, intensity_array, mz_window=50.0,
                               percentage_lowest=0.05, factor=5):
    """
    Apply moving average algorithm to a single mass spectrum using an m/z-based window.
    This function is optimized with Numba.

    :param mz_array: numpy array of m/z values
    :param intensity_array: numpy array of intensity values
    :param mz_window: size of the moving window in Da (default: 100.0)
    :param n_lowest: number of lowest points to consider in each window (default: 5)
    :param factor: factor to multiply the mean of the lowest points (default: 5.0)
    :return: tuple of (filtered_mz_array, filtered_intensity_array)
    """
    filtered_mz = []
    filtered_intensity = []
    noise_mz = []
    noise_intensity = []

    for i in range(len(mz_array)):
        mz_min = mz_array[i] - mz_window / 2
        mz_max = mz_array[i] + mz_window / 2

        window_intensities = intensity_array[(mz_array >= mz_min) & (mz_array <= mz_max)]

        if len(window_intensities) > 0:
            positive_intensities = window_intensities[window_intensities > 0]
            if len(positive_intensities) > 0:
                sorted_intensities = np.sort(positive_intensities)
                n_lowest = max(1, int(len(sorted_intensities) * percentage_lowest))
                lowest_n = sorted_intensities[:n_lowest]
                baseline = factor * np.mean(lowest_n)
            else:
                baseline = 0.0
        else:
            baseline = 0.0

        if intensity_array[i] > baseline:
            filtered_mz.append(mz_array[i])
            filtered_intensity.append(intensity_array[i])
        else:
            noise_mz.append(mz_array[i])
            noise_intensity.append(intensity_array[i])

    return np.array(filtered_mz), np.array(filtered_intensity), np.array(noise_mz), np.array(noise_intensity)


def load_ms_imaging_data(data_dir):
    """
    Load pre-generated MS imaging data from files.

    Parameters:
    - data_dir: string, path to the directory containing the data files

    Returns:
    - mz_values: numpy array of m/z values
    - intensity_matrix: 2D numpy array where each row corresponds to an m/z value and each column to a pixel
    - coordinates: list of (x, y) coordinates for each pixel
    """
    mz_values_path = os.path.join(data_dir, 'mz_values.npy')
    intensity_matrix_path = os.path.join(data_dir, 'intensity_matrix.npy')
    coordinates_path = os.path.join(data_dir, 'coordinates.pkl')

    # Load mz_values
    mz_values = np.load(mz_values_path)

    # Load intensity_matrix
    intensity_matrix = np.load(intensity_matrix_path)

    # Load coordinates
    with open(coordinates_path, 'rb') as f:
        coordinates = pickle.load(f)

    return mz_values, intensity_matrix, coordinates


def get_ms_spectrum(mz_values, intensity_matrix, pixel_index):
    """
    Get MS spectrum for a given pixel.

    Parameters:
    - mz_values: numpy array of m/z values
    - intensity_matrix: 2D numpy array where each row corresponds to an m/z value and each column to a pixel
    - pixel_index: index of the pixel to retrieve

    Returns:
    - tuple of (mz_array, intensity_array)
    """
    return mz_values, intensity_matrix[:, pixel_index]


def plot_ms_spectrum(mzs, intensities, title=None,
                     x_range=None, y_range=None):
    """
    Plot MS spectrum for a given pixel.

    Parameters:
    - mz_values: numpy array of m/z values
    - intensity_matrix: 2D numpy array where each row corresponds to an m/z value and each column to a pixel
    - coordinates: list of (x, y) coordinates for each pixel
    - pixel_index: index of the pixel to plot
    - title: optional title for the plot
    - xlim: optional tuple of (min, max) for x-axis limits
    - ylim: optional tuple of (min, max) for y-axis limits

    Returns:
    - fig, ax: matplotlib figure and axis objects
    """

    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 6))

    # Plot the spectrum
    ax.vlines(mzs, [0], intensities, linewidth=1)

    # Set labels and title
    ax.set_xlabel('m/z')
    ax.set_ylabel('Intensity')

    # Set axis limits if provided
    if x_range:
        ax.set_xlim(x_range[0], x_range[1])
    if y_range:
        ax.set_ylim(y_range[0], y_range[1])

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)

    # Add title
    if title:
        ax.set_title(title)

    # Adjust layout
    plt.tight_layout()

    return fig, ax


def centroid_spectrum(mz_list, intensity_list, centroid_mode='max',
                      ms2_da=0.005, ms2_ppm=25.0):
    """
    Centroid a spectrum by merging peaks within the +/- ms2_ppm or +/- ms2_da.
    centroid_mode: 'max' or 'sum'
    """
    peaks = list(zip(mz_list, intensity_list))
    peaks = np.asarray(peaks, dtype=np.float32, order="C")
    # Sort the peaks by m/z.
    peaks = peaks[np.argsort(peaks[:, 0])]
    peaks = _centroid_spectrum(peaks, centroid_mode, ms2_da=ms2_da, ms2_ppm=ms2_ppm)

    return peaks[:, 0], peaks[:, 1]


@njit
def _centroid_spectrum(peaks, centroid_mode='max',
                       ms2_da=0.005, ms2_ppm=25.0) -> np.ndarray:
    """Centroid a spectrum by merging peaks within the +/- ms2_ppm or +/- ms2_da,
    only merging peaks with lower intensity than the target peak."""
    # Construct a new spectrum to avoid memory reallocation.
    peaks_new = np.zeros((peaks.shape[0], 2), dtype=np.float32)
    peaks_new_len = 0

    # Get the intensity argsort order.
    intensity_order = np.argsort(peaks[:, 1])

    # Iterate through the peaks from high to low intensity.
    for idx in intensity_order[::-1]:
        if peaks[idx, 1] > 0:
            mz_delta_allowed_ppm_in_da = peaks[idx, 0] * ms2_ppm * 1e-6
            mz_delta_allowed = max(ms2_da, mz_delta_allowed_ppm_in_da)

            # Find indices of peaks to merge.
            indices = np.where(np.logical_and(np.abs(peaks[:, 0] - peaks[idx, 0]) <= mz_delta_allowed,
                                              peaks[:, 1] < peaks[idx, 1]))[0]

            if centroid_mode == 'max':
                # Merge the peaks
                peaks_new[peaks_new_len, 0] = peaks[idx, 0]
                peaks_new[peaks_new_len, 1] = peaks[idx, 1]
                peaks_new_len += 1

                peaks[indices, 1] = 0

            elif centroid_mode == 'sum':
                # Merge the peaks
                intensity_sum = peaks[idx, 1]
                intensity_weighted_mz_sum = peaks[idx, 1] * peaks[idx, 0]
                for i in indices:
                    intensity_sum += peaks[i, 1]
                    intensity_weighted_mz_sum += peaks[i, 1] * peaks[i, 0]
                    peaks[i, 1] = 0  # Set the intensity of the merged peaks to 0

                peaks_new[peaks_new_len, 0] = intensity_weighted_mz_sum / intensity_sum
                peaks_new[peaks_new_len, 1] = intensity_sum
                peaks_new_len += 1

                # Set the intensity of the target peak to 0
                peaks[idx, 1] = 0

    # Return the new spectrum.
    peaks_new = peaks_new[:peaks_new_len]
    return peaks_new[np.argsort(peaks_new[:, 0])]


def _check_centroid(peaks, ms2_da=0.005, ms2_ppm=25.0) -> int:
    """Check if the spectrum is centroided. 0 for False and 1 for True."""
    if peaks.shape[0] <= 1:
        return 1

    # Calculate ms2_ppm_in_da
    ms2_ppm_in_da = peaks[1:, 0] * ms2_ppm * 1e-6

    # Use bitwise OR to choose the maximum
    threshold = np.maximum(ms2_da, ms2_ppm_in_da)

    # Check if the spectrum is centroided
    return 1 if np.all(np.diff(peaks[:, 0]) >= threshold) else 0


def plot_filtered_spectrum(filtered_mz, filtered_intensity, noise_mz, noise_ints,
                           title=None, x_range=None, y_range=None):
    import matplotlib.pyplot as plt

    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 6))

    # Plot the filtered spectrum
    ax.vlines(filtered_mz, [0], filtered_intensity, linewidth=1, label='Filtered Spectrum')

    # Plot the noise
    ax.vlines(noise_mz, [0], noise_ints, color='red', linewidth=1, alpha=0.5, label='Noise')

    # Set labels and title
    ax.set_xlabel('m/z')
    ax.set_ylabel('Intensity')

    # Set axis limits if provided
    if x_range:
        ax.set_xlim(x_range[0], x_range[1])
    if y_range:
        ax.set_ylim(y_range[0], y_range[1])

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)

    # Add legend
    ax.legend()

    # Add title
    if title:
        ax.set_title(title)

    # Adjust layout
    plt.tight_layout()

    return fig, ax


if __name__ == "__main__":
    # imzml_file = '/Users/shipei/Documents/projects/ms1_id/imaging/HeLa/14052018_coculture_HeLa_NIH3T3_H3_Neg.imzML'

    imzml_file = '/Users/shipei/Documents/projects/ms1_id/imaging/macrophage/20220127_250x271_5um_single cell macro eau_AcOH_dan_Neg_mode_200-2000mz_70K_Laser39_6.5kV_400C_Slens90_Line_leftright_centroid.imzML'

    mz_array, intensity_array = get_spectrum_from_imzml(imzml_file, index=10)
    peaks = np.column_stack((mz_array, intensity_array))

    filtered_mz, filtered_intensity, noise_mz, noise_ints = apply_moving_average_numba(mz_array, intensity_array,
                                                                                       mz_window=100.0,
                                                                                       percentage_lowest=0.05,
                                                                                       factor=1)

    centroid_mz, centroid_intensity = centroid_spectrum(filtered_mz, filtered_intensity,
                                                        centroid_mode='max',
                                                        ms2_da=0.005, ms2_ppm=25)

    x_range = None
    y_range = None

    # mask = (peaks[:, 0] >= x_range[0]) & (peaks[:, 0] <= x_range[1])
    # print(peaks[mask])

    fig, ax = plot_ms_spectrum(mz_array, intensity_array, title='original', x_range=x_range, y_range=y_range)
    fig, ax = plot_filtered_spectrum(filtered_mz, filtered_intensity, noise_mz, noise_ints,
                                     title='filtered', x_range=x_range, y_range=y_range)
    fig, ax = plot_ms_spectrum(centroid_mz, centroid_intensity, title='centroided', x_range=x_range, y_range=y_range)

    # Display the plot
    plt.show()

    # Optionally, save the plot
    # fig.savefig('ms_spectrum_pixel_0.png', dpi=300, bbox_inches='tight')
