import numpy as np
import matplotlib.pyplot as plt
import hdbscan
from sklearn.preprocessing import MinMaxScaler
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable


def cluster_ion_image(ion_image, min_cluster_size=10, min_samples=5, intensity_weight=5.0):
    """
    Apply HDBSCAN clustering to an ion image to identify different spatial distributions.

    Parameters:
    -----------
    ion_image : 2D numpy array
        The ion image intensity data
    min_cluster_size : int
        The minimum size of clusters
    min_samples : int
        The number of samples in a neighborhood for a point to be considered as a core point
    intensity_weight : float
        Weight factor for intensity values in the feature vector

    Returns:
    --------
    labels_img : 2D numpy array
        Array of the same shape as ion_image where each pixel is labeled with its cluster ID
    n_clusters : int
        Number of clusters found (excluding noise points labeled as -1)
    """
    # Get image dimensions
    height, width = ion_image.shape

    # Create coordinate arrays
    y_coords, x_coords = np.mgrid[0:height, 0:width]

    # Create feature vectors for each pixel: [x, y, intensity]
    features = np.column_stack([
        x_coords.ravel() / width,  # Normalize x coordinates
        y_coords.ravel() / height,  # Normalize y coordinates
        ion_image.ravel() * intensity_weight  # Apply weight to intensity values
    ])

    # Scale features with MinMaxScaler (better for spatial data than StandardScaler)
    features = MinMaxScaler().fit_transform(features)

    # Apply HDBSCAN
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        gen_min_span_tree=True,
        cluster_selection_method='eom'  # Excess of Mass - better for varying density clusters
    )

    clusterer.fit(features)
    labels = clusterer.labels_

    # Reshape labels to match image dimensions
    labels_img = labels.reshape(ion_image.shape)

    # Count unique clusters (excluding noise labeled as -1)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    return labels_img, n_clusters, clusterer


def visualize_clusters(ion_image, cluster_labels, clusterer=None, save_path=None):
    """
    Visualize the original ion image and the clustering results.

    Parameters:
    -----------
    ion_image : 2D numpy array
        The original ion image
    cluster_labels : 2D numpy array
        The cluster labels for each pixel
    clusterer : HDBSCAN object or None
        The fitted HDBSCAN clusterer (for advanced visualization)
    save_path : str or None
        If provided, the figure will be saved to this path
    """
    # Create a figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot original ion image
    im1 = ax1.imshow(ion_image, cmap='viridis')
    ax1.set_title('Original Ion Image')
    ax1.set_xlabel('X position')
    ax1.set_ylabel('Y position')

    # Add colorbar
    divider = make_axes_locatable(ax1)
    cax1 = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im1, cax=cax1)

    # Create a custom colormap for clusters (noise will be black)
    unique_labels = np.unique(cluster_labels)
    n_clusters = len(unique_labels)

    # Create a colormap: black for noise (-1), then distinct colors for each cluster
    colors = ['black'] + list(plt.cm.tab20(np.linspace(0, 1, n_clusters)))
    cmap = mcolors.ListedColormap(colors)

    # Plot cluster image
    im2 = ax2.imshow(cluster_labels, cmap=cmap, interpolation='nearest')
    ax2.set_title(f'HDBSCAN Clusters: {n_clusters - (1 if -1 in unique_labels else 0)} clusters found')
    ax2.set_xlabel('X position')

    # Add colorbar
    divider = make_axes_locatable(ax2)
    cax2 = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(im2, cax=cax2, ticks=unique_labels)
    cbar.set_label('Cluster ID')

    # Adjust layout
    plt.tight_layout()

    # Save figure if path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # If HDBSCAN clusterer is provided, plot the condensed tree
    if clusterer is not None:
        plt.figure(figsize=(10, 8))
        color_list = [plt.cm.tab20(i) for i in range(20)]
        clusterer.condensed_tree_.plot(select_clusters=True, selection_palette=color_list)
        plt.title('HDBSCAN Condensed Cluster Tree')
        if save_path:
            tree_path = save_path.replace('.png', '_tree.png')
            plt.savefig(tree_path, dpi=300, bbox_inches='tight')

    plt.show()

    return fig


def analyze_feature_statistics(ion_image, cluster_labels):
    """
    Calculate statistics for each cluster to characterize the features.

    Parameters:
    -----------
    ion_image : 2D numpy array
        The original ion image
    cluster_labels : 2D numpy array
        The cluster labels for each pixel

    Returns:
    --------
    stats : dict
        Dictionary containing statistics for each cluster
    """
    unique_labels = np.unique(cluster_labels)
    stats = {}

    for label in unique_labels:
        mask = (cluster_labels == label)
        region_intensities = ion_image[mask]

        if len(region_intensities) == 0:
            continue

        # Calculate basic statistics
        stats[label] = {
            'pixel_count': np.sum(mask),
            'mean_intensity': np.mean(region_intensities),
            'median_intensity': np.median(region_intensities),
            'std_intensity': np.std(region_intensities),
            'max_intensity': np.max(region_intensities),
            'min_intensity': np.min(region_intensities),
            'area_percentage': np.sum(mask) / mask.size * 100
        }

        # Calculate centroid (center of mass)
        y_indices, x_indices = np.where(mask)
        if len(y_indices) > 0 and len(x_indices) > 0:
            stats[label]['centroid_y'] = np.mean(y_indices)
            stats[label]['centroid_x'] = np.mean(x_indices)

        # Calculate bounding box
        if len(y_indices) > 0 and len(x_indices) > 0:
            stats[label]['bbox_min_y'] = np.min(y_indices)
            stats[label]['bbox_max_y'] = np.max(y_indices)
            stats[label]['bbox_min_x'] = np.min(x_indices)
            stats[label]['bbox_max_x'] = np.max(x_indices)
            stats[label]['bbox_height'] = np.max(y_indices) - np.min(y_indices)
            stats[label]['bbox_width'] = np.max(x_indices) - np.min(x_indices)

    return stats


def process_ion_image(ion_image, min_cluster_size=10, min_samples=5, intensity_weight=5.0, save_path=None):
    """
    Main function to process an ion image with HDBSCAN clustering.

    Parameters:
    -----------
    ion_image : 2D numpy array
        The ion image intensity data
    min_cluster_size : int
        HDBSCAN minimum cluster size parameter
    min_samples : int
        HDBSCAN minimum samples parameter
    intensity_weight : float
        Weight factor for intensity values
    save_path : str or None
        If provided, the figure will be saved to this path

    Returns:
    --------
    cluster_labels : 2D numpy array
        The cluster labels for each pixel
    stats : dict
        Statistics for each cluster
    clusterer : HDBSCAN object
        The fitted HDBSCAN clusterer
    """
    # Apply HDBSCAN clustering
    cluster_labels, n_clusters, clusterer = cluster_ion_image(
        ion_image,
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        intensity_weight=intensity_weight
    )

    # Visualize results
    fig = visualize_clusters(ion_image, cluster_labels, clusterer, save_path)

    # Calculate statistics for each cluster
    stats = analyze_feature_statistics(ion_image, cluster_labels)

    # Print summary information
    print(f"Found {n_clusters} clusters (excluding noise)")

    for label, cluster_stats in stats.items():
        if label == -1:
            print(
                f"Noise points: {cluster_stats['pixel_count']} pixels ({cluster_stats['area_percentage']:.2f}% of image)")
        else:
            print(f"Cluster {label}: {cluster_stats['pixel_count']} pixels, "
                  f"Mean intensity: {cluster_stats['mean_intensity']:.2f}, "
                  f"Position: ({cluster_stats['centroid_x']:.1f}, {cluster_stats['centroid_y']:.1f})")

    return cluster_labels, stats, clusterer


# Example usage
if __name__ == "__main__":
    # Create a synthetic ion image for demonstration
    # In real use, you would load your MS imaging data here
    size = 100
    np.random.seed(42)

    # Background noise
    ion_image = np.random.normal(0, 0.1, (size, size))

    # Add three different distributions to simulate isobaric compounds
    x, y = np.mgrid[0:size, 0:size]

    # First feature: circular, centered at (30, 30)
    mask1 = np.exp(-0.01 * ((x - 30) ** 2 + (y - 30) ** 2))
    ion_image += mask1 * 2.5

    # Second feature: circular, centered at (80, 80)
    mask2 = np.exp(-0.01 * ((x - 80) ** 2 + (y - 80) ** 2))
    ion_image += mask2 * 2

    # Third feature: elongated shape, centered at (70, 30)
    mask3 = np.exp(-0.01 * ((x - 70) ** 2 + (y - 30) ** 2 / 9))
    ion_image += mask3 * 3

    # Ensure all values are positive
    ion_image = ion_image - ion_image.min()

    # Normalize the image
    ion_image = ion_image / ion_image.max()

    # Process the ion image
    cluster_labels, stats, clusterer = process_ion_image(
        ion_image,
        min_cluster_size=30,
        min_samples=10,
        intensity_weight=5,
        save_path="ms_imaging_clusters.png"
    )