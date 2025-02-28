import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse


def correlation_summary(cor_matrix, thresholds=[0.90, 0.80, 0.70]):
    """
    Summarize correlation scores and create a histogram plot for a csr_matrix.

    :param cor_matrix: scipy.sparse.csr_matrix of correlation scores
    :param thresholds: List of correlation thresholds to report
    """
    if not sparse.issparse(cor_matrix) or not isinstance(cor_matrix, sparse.csr_matrix):
        raise ValueError("Input must be a scipy.sparse.csr_matrix")

    # Get upper triangle (excluding diagonal)
    upper_tri = sparse.triu(cor_matrix, k=1)

    # Convert to array (this step might be memory-intensive for very large matrices)
    upper_tri_array = upper_tri.data

    # Print summary statistics
    print(f"Total number of correlations: {len(upper_tri_array)}")
    print(f"Mean correlation: {np.mean(upper_tri_array):.4f}")
    print(f"Median correlation: {np.median(upper_tri_array):.4f}")

    for threshold in thresholds:
        count = np.sum(upper_tri_array >= threshold)
        percentage = (count / len(upper_tri_array)) * 100
        print(f"Correlations >= {threshold}: {count} ({percentage:.2f}%)")

    # Create histogram
    plt.figure(figsize=(10, 6))
    plt.hist(upper_tri_array, bins=np.arange(-1.01, 1.011, 0.02), color='#56648a', edgecolor='none')
    plt.title('Histogram of correlation scores')
    plt.xlabel('Correlation score')
    plt.ylabel('Frequency')

    # Add vertical lines for thresholds with different colors
    colors = ['red', 'green', 'blue']  # Standard colors for threshold lines
    for threshold, color in zip(thresholds, colors):
        plt.axvline(x=threshold, color=color, linestyle='--', label=f'Threshold {threshold}')

    plt.legend(loc='upper right')
    plt.tight_layout()

    plt.savefig('correlation_histogram.svg', transparent=True)
    plt.show()


if __name__ == '__main__':
    ################
    ####### careful, in the file folder is filtered mz correlation matrix
    ################ have to recalculate the mz correlation matrix
    file_path = '/Users/shipei/Documents/projects/ms1_id/imaging/MTBLS313/Brain01_Bregma1-42_01_centroid/intensity_matrix.npy'

    intensity_matrix = np.load(file_path)

    from src.ms1_id.msi.calculate_mz_cor_parallel import calc_all_mz_correlations

    mz_cor_matrix = calc_all_mz_correlations(intensity_matrix, min_overlap=10,
                                             min_cor=-1.01,
                                             n_processes=10, save=True,
                                             save_dir='data')

    # mz_cor_matrix = sparse.load_npz('./data/mz_correlation_matrix.npz')

    correlation_summary(mz_cor_matrix)
