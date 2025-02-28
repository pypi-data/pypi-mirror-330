import numpy as np
import pyimzml.ImzMLParser as imzml
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter
import matplotlib.colors as colors
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from tqdm import tqdm

def get_ion_image_from_parser(parser, target_mz, tolerance=0.01, intensity_threshold=0):
    max_x = max(x for x, y, z in parser.coordinates)
    max_y = max(y for x, y, z in parser.coordinates)
    image = np.zeros((max_y + 1, max_x + 1))

    for idx, (x, y, z) in enumerate(parser.coordinates):
        mzs, ints = parser.getspectrum(idx)
        mask = np.abs(mzs - target_mz) <= tolerance
        matched_intensities = ints[mask]

        if len(matched_intensities) > 0:
            intensity = np.max(matched_intensities)
            if intensity > intensity_threshold:
                image[y, x] = intensity

    return image

def plot_ion_image(ax, image, title, colormap='viridis', norm_max_intensity=None,
                   hot_spot_removal=False, hot_spot_percentile=99, median_filter_flag=False):
    if hot_spot_removal:
        percentile_top = np.percentile(image, hot_spot_percentile)
        image[image > percentile_top] = percentile_top

    if median_filter_flag:
        image = median_filter(image, size=3)

    if norm_max_intensity is None:
        norm_max_intensity = np.max(image)

    original_cmap = plt.get_cmap(colormap)
    colors_array = original_cmap(np.linspace(0.10, 1, 256))
    custom_cmap = colors.LinearSegmentedColormap.from_list("custom_" + colormap, colors_array)

    im = ax.imshow(image, cmap=custom_cmap, vmin=0, vmax=norm_max_intensity)
    ax.set_title(title, fontsize=8, wrap=True)
    ax.axis('off')
    return im

def plot_all_ion_images(parser, df, output_pdf):

    # df = df[(df['matched_score'] > 0.8) & (df['spectral_usage'] > 0.1)].reset_index(drop=True)

    total_metabolites = len(df)
    with PdfPages(output_pdf) as pdf:
        for i in tqdm(range(0, total_metabolites, 10), desc="Processing metabolites", unit="page"):
            fig, axs = plt.subplots(5, 2, figsize=(15, 30))
            axs = axs.ravel()

            for j in range(10):
                if i + j < total_metabolites:
                    row = df.iloc[i + j]
                    image = get_ion_image_from_parser(parser, row['precursor_mz'], tolerance=0.005)

                    title = f"{row['name']}\n{row['precursor_mz']}\n{row['precursor_type']}\nScore: {row['matched_score']:.2f}\nPeak: {row['matched_peak']:.4f}\nUsage: {row['spectral_usage']:.2f}"

                    im = plot_ion_image(axs[j], image, title,
                                        norm_max_intensity=None,
                                        hot_spot_removal=True)

                    # plt.colorbar(im, ax=axs[j], fraction=0.046, pad=0.04)
                else:
                    axs[j].axis('off')

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

# Usage
imzml_file = "/imaging/mouse_liver/Mouse liver_DMAN_200x200_25um.imzML"
df = pd.read_csv("/imaging/mouse_liver/Mouse liver_DMAN_200x200_25um/ms1_id_annotations_derep.tsv", sep='\t')
output_pdf = "ion_images.pdf"

# Load the ImzML parser once
parser = imzml.ImzMLParser(imzml_file)

# Pass the parser to the function instead of the file path
plot_all_ion_images(parser, df, output_pdf)