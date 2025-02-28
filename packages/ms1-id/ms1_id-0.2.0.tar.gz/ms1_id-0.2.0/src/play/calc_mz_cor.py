import multiprocessing as mp
import os
import tempfile

import numpy as np
from numba import njit
from scipy.sparse import csr_matrix, save_npz, load_npz
from tqdm import tqdm

import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import pyimzml.ImzMLParser as imzml
from scipy.ndimage import median_filter
import matplotlib.colors as colors
from scipy.stats import pearsonr


def get_ion_image_from_imzml(imzml_file, target_mz, tolerance=0.01, intensity_threshold=0):
    parser = imzml.ImzMLParser(imzml_file)

    # Get the maximum x and y coordinates from all spectra
    max_x = max(x for x, y, z in parser.coordinates)
    max_y = max(y for x, y, z in parser.coordinates)

    # Initialize the image array with the maximum dimensions
    image = np.zeros((max_y + 1, max_x + 1))

    for idx, (x, y, z) in enumerate(parser.coordinates):
        mzs, ints = parser.getspectrum(idx)
        mask = np.abs(mzs - target_mz) <= tolerance
        matched_intensities = ints[mask]

        if len(matched_intensities) > 0:
            intensity = np.max(matched_intensities)
            if intensity > intensity_threshold:
                image[y, x] = intensity

    return image, parser.coordinates


def plot_ion_image(image, title=None, colormap='viridis',
                   x_range=None, y_range=None,
                   hot_spot_removal=False, hot_spot_percentile=99.9,
                   apply_median_filter=False,
                   save=False, name='ion_image.svg'):
    """
    Plot the ion image, with options to plot partial data.

    Parameters:
    - image: 2D numpy array representing the ion image
    - title: Optional title for the plot
    - colormap: Colormap to use for the image (default: 'viridis')
    - x_range: Tuple of (start, end) for x-axis. If None, plot all. (default: None)
    - y_range: Tuple of (start, end) for y-axis. If None, plot all. (default: None)
    """
    # Apply ranges if specified
    if x_range is not None:
        image = image[:, x_range[0]:x_range[1]]
    if y_range is not None:
        image = image[y_range[0]:y_range[1], :]

    # Apply processing
    if hot_spot_removal:
        percentile_top = np.percentile(image[image > 0], hot_spot_percentile)
        image[image > percentile_top] = percentile_top

    if apply_median_filter:
        image = median_filter(image, size=3)

    plt.figure(figsize=(10, 8))

    # Create a custom colormap using the later 90% of viridis
    original_cmap = plt.get_cmap(colormap)
    colors_array = original_cmap(np.linspace(0.10, 1, 256))
    custom_cmap = colors.LinearSegmentedColormap.from_list("custom_" + colormap, colors_array)

    plt.imshow(image, cmap=custom_cmap, vmin=0, vmax=np.max(image))
    plt.colorbar(label='Intensity')

    if title:
        plt.title(title)

    plt.axis('off')
    plt.tight_layout()

    if save:
        plt.savefig(name, transparent=True)
    plt.show()

def plot_im(arr):
    im = arr.reshape(450, -1)
    colormap = 'viridis'  # viridis, cividis, magma, inferno, plasma
    # Plot partial image
    plot_ion_image(im,
                   title=None, colormap='viridis',
                   x_range=(None, None), y_range=(None, None),
                   hot_spot_removal=True, hot_spot_percentile=99.9,
                   apply_median_filter=False,
                   save=False,
                   name='ion_image.svg')

def plot_correlation(array1, array2, title="Correlation Visualization"):
    """
    Create a line plot showing the correlation between two arrays by sorting the first one.

    Parameters:
    - array1: First numpy array
    - array2: Second numpy array
    - title: Plot title
    """
    # Create a copy to avoid modifying the original arrays
    a1 = np.array(array1)
    a2 = np.array(array2)

    # Get sorting indices from the first array
    sort_indices = np.argsort(a1)

    # Sort both arrays based on the first array's order
    a1_sorted = a1[sort_indices]
    a2_sorted = a2[sort_indices]

    # Calculate correlations
    pearson_corr, p_value_pearson = pearsonr(a1, a2)
    spearman_corr, p_value_spearman = spearmanr(a1, a2)

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot both arrays
    plt.plot(range(len(a1_sorted)), a1_sorted / np.max(a1_sorted),
             'b-', label='Array 1 (sorted)')
    plt.plot(range(len(a2_sorted)), a2_sorted / np.max(a2_sorted),
             'r-', label='Array 2 (reordered)')

    # Add a title and labels
    plt.title(
        f"{title}\nPearson r={pearson_corr:.4f} (p={p_value_pearson:.4f}), Spearman r={spearman_corr:.4f} (p={p_value_spearman:.4f})")
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add a secondary plot showing the direct correlation
    plt.figure(figsize=(8, 8))
    plt.scatter(a1, a2, alpha=0.6)
    plt.title(f"Direct Correlation\nPearson r={pearson_corr:.4f}, Spearman r={spearman_corr:.4f}")
    plt.xlabel('Array 1')
    plt.ylabel('Array 2')
    plt.grid(True, alpha=0.3)

    # Show the plots
    plt.tight_layout()
    plt.show()


def region_based_mz_correlation_with_visualization(intensities1, intensities2, n_regions=3, min_overlap=5):
    """
    Calculate correlation between two intensity arrays using a region-based approach with visualization.

    Parameters:
    - intensities1, intensities2: Input intensity arrays
    - n_regions: Number of regions to split the data into along the x-axis
    - min_overlap: Minimum number of points required in a region

    Returns:
    - Dictionary containing correlation results and visualization data
    """
    import matplotlib.pyplot as plt

    # Remove zero intensities
    non_zero_mask = (intensities1 > 0) & (intensities2 > 0)
    x = intensities1[non_zero_mask]
    y = intensities2[non_zero_mask]

    n = len(x)
    if n < min_overlap:
        return {"max_correlation": 0.0, "regions": {}}

    # Get sorting indices and sort the data by x values
    sorted_indices = np.argsort(x)
    x_sorted = x[sorted_indices]
    y_sorted = y[sorted_indices]

    # Calculate region sizes
    region_size = n // n_regions

    # Track results
    results = {"regions": {}}
    max_corr = 0
    max_corr_region = -1

    # Set up colors for visualization
    colors = plt.cm.tab10(np.linspace(0, 1, n_regions))

    # Create figure for visualization
    plt.figure(figsize=(12, 10))
    plt.subplot(211)

    # Process each region
    for i in range(n_regions):
        start_idx = i * region_size
        end_idx = (i + 1) * region_size if i < n_regions - 1 else n

        # Get data for this region
        x_region = x_sorted[start_idx:end_idx]
        y_region = y_sorted[start_idx:end_idx]

        # Skip if too few points
        if len(x_region) < min_overlap:
            continue

        # Calculate correlation for this region
        pearson_r = np.corrcoef(x_region, y_region)[0, 1]

        # Store results
        results["regions"][f"region_{i}"] = {
            "x_range": (min(x_region), max(x_region)),
            "pearson_r": pearson_r,
            "n_points": len(x_region)
        }

        # Update maximum if needed
        if abs(pearson_r) > abs(max_corr):
            max_corr = pearson_r
            max_corr_region = i

        # Plot this region
        plt.scatter(x_region, y_region,
                    c=[colors[i]],
                    label=f"Region {i} (r={pearson_r:.3f}, n={len(x_region)})",
                    alpha=0.7)

    # If no valid regions found, use overall correlation
    if max_corr_region == -1:
        max_corr = np.corrcoef(x, y)[0, 1]

    # Store overall results
    results["max_correlation"] = max_corr
    results["max_region"] = f"region_{max_corr_region}" if max_corr_region != -1 else "overall"
    results["overall_correlation"] = np.corrcoef(x, y)[0, 1]

    # Finalize the first plot
    plt.title("Region-Based Correlation Analysis")
    plt.xlabel("Array 1")
    plt.ylabel("Array 2")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Create second plot showing original data
    plt.subplot(212)
    plt.scatter(x, y, alpha=0.3, c='gray')
    plt.title(f"Original Data (Overall Pearson r={results['overall_correlation']:.4f})")
    plt.xlabel("Array 1")
    plt.ylabel("Array 2")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return results


# Replace your existing _mz_correlation function with this one
def _mz_correlation_region(intensities1, intensities2, min_overlap=5):
    return region_based_mz_correlation_with_visualization(intensities1, intensities2,
                                      n_regions=1,  # Adjust as needed
                                      min_overlap=min_overlap)


#@njit
def _mz_correlation(intensities_x, intensities_y, min_overlap=5):
    plot_im(intensities_x)
    plot_im(intensities_y)

    non_zero_mask_x = intensities_x > 0
    non_zero_mask_y = intensities_y > 0
    non_zero_mask = non_zero_mask_x & non_zero_mask_y

    ratio_x = sum(non_zero_mask > 0) / sum(non_zero_mask_x > 0)
    ratio_y = sum(non_zero_mask > 0) / sum(non_zero_mask_y > 0)

    non_zero_mask = (intensities_x > 0) & (intensities_y > 0)
    x = intensities_x[non_zero_mask]
    y = intensities_y[non_zero_mask]
    plot_correlation(x, y, title="Correlation, with both non-zero intensities")

    n = len(x)
    if n < min_overlap:
        return 0.0

    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x * x)
    sum_y2 = np.sum(y * y)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = np.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))

    cor = numerator / denominator if denominator != 0 else 0.0

    return cor


def worker(start_idx, end_idx, mmap_filename, intensity_matrix_shape, min_overlap,
           min_cor, return_dict):
    intensity_matrix = np.memmap(mmap_filename, dtype=np.float64, mode='r', shape=intensity_matrix_shape)
    n_mzs = intensity_matrix_shape[0]

    rows = []
    cols = []
    data = []

    for i in range(start_idx, end_idx):
        for j in range(i + 1, n_mzs):
            corr = _mz_correlation(intensity_matrix[i], intensity_matrix[j], min_overlap)
            if corr >= min_cor:
                rows.append(i)
                cols.append(j)
                data.append(corr)

    return_dict[start_idx] = (rows, cols, data)


def calc_all_mz_correlations(intensity_matrix, min_overlap=5, min_cor=0.8,
                             save_dir=None, n_processes=None, chunk_size=500):
    """
    Calculate m/z correlation matrix for MS imaging data using multiprocessing and numpy memmap

    :param intensity_matrix: 2D numpy array where rows are m/z values and columns are spectra
    :param min_overlap: Minimum number of overlapping spectra between two ions
    :param min_cor: Minimum correlation value to keep
    :param save_dir: Directory to save the result if save is True
    :param n_processes: Number of processes to use (default: number of CPU cores)
    :param chunk_size: Number of rows to process in each chunk
    :return: Sparse correlation matrix
    """

    mz_cor_func = _mz_correlation

    # check if result files exist
    if save_dir is not None:
        path = os.path.join(save_dir, 'mz_correlation_matrix.npz')
        if os.path.exists(path):
            print("Loading existing correlation matrix...")
            return load_npz(path)

    n_mzs, n_spectra = intensity_matrix.shape

    n_processes = n_processes or mp.cpu_count()

    # Create a temporary memmap file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    mmap_filename = temp_file.name
    mmap_array = np.memmap(mmap_filename, dtype=np.float64, mode='w+', shape=intensity_matrix.shape)
    mmap_array[:] = intensity_matrix[:]
    mmap_array.flush()

    # Prepare chunks
    chunks = [(i, min(i + chunk_size, n_mzs)) for i in range(0, n_mzs, chunk_size)]

    print(f"Calculating m/z spatial correlations...")

    if n_processes == 1:
        # Non-parallel processing
        all_rows = []
        all_cols = []
        all_data = []
        for start, end in tqdm(chunks, desc="Processing chunks"):
            rows, cols, data = [], [], []
            for i in range(start, end):
                for j in range(i + 1, n_mzs):
                    corr = mz_cor_func(mmap_array[i], mmap_array[j], min_overlap)
                    if corr >= min_cor:
                        rows.append(i)
                        cols.append(j)
                        data.append(corr)
            all_rows.extend(rows)
            all_cols.extend(cols)
            all_data.extend(data)
    else:
        # Parallel processing
        manager = mp.Manager()
        return_dict = manager.dict()

        with mp.Pool(processes=n_processes) as pool:
            jobs = [
                pool.apply_async(worker, (start, end, mmap_filename, intensity_matrix.shape,
                                          min_overlap, min_cor, return_dict))
                for start, end in chunks
            ]

            for job in tqdm(jobs, desc="Processing chunks"):
                job.get()  # Wait for the job to complete

        all_rows = []
        all_cols = []
        all_data = []
        for result in return_dict.values():
            all_rows.extend(result[0])
            all_cols.extend(result[1])
            all_data.extend(result[2])

    corr_matrix = csr_matrix((all_data, (all_rows, all_cols)), shape=(n_mzs, n_mzs), dtype=np.float64)
    corr_matrix = corr_matrix + corr_matrix.T
    corr_matrix.setdiag(1.0)

    if save_dir:
        path = os.path.join(save_dir, 'mz_correlation_matrix.npz')
        print(f"Saving correlation matrix to {path}...")
        save_npz(path, corr_matrix)

    # Clean up the temporary memmap file
    os.unlink(mmap_filename)

    return corr_matrix



if __name__ == '__main__':

    # from scipy.sparse import csr_matrix, load_npz
    # mz_cor_matrix = load_npz('/Users/shipei/Documents/projects/ms1_id/imaging/spotted_stds/2020-12-05_ME_X190_L1_Spotted_20umss_375x450_33at_DAN_Neg/mz_correlation_matrix.npz')
    # if not isinstance(mz_cor_matrix, csr_matrix):
    #     correlation_matrix = csr_matrix(mz_cor_matrix)

    # mz_values = np.load('/Users/shipei/Documents/projects/ms1_id/imaging/spotted_stds/2020-12-05_ME_X190_L1_Spotted_20umss_375x450_33at_DAN_Neg/mz_values.npy')
    # print(mz_values.shape)


    # 128.0353, 143.0462, 306.0765
    # idx: 116, 211, 1044

    #
    # ######
    int_matrix = np.load('/Users/shipei/Documents/projects/ms1_id/imaging/spotted_stds/2020-12-05_ME_X190_L1_Spotted_20umss_375x450_33at_DAN_Neg/intensity_matrix.npy')
    print(int_matrix.shape)

    int_matrix = int_matrix[[1044, 116, 211]]

    calc_all_mz_correlations(int_matrix, min_overlap=5, min_cor=0.8, save_dir=None, n_processes=1, chunk_size=500)

