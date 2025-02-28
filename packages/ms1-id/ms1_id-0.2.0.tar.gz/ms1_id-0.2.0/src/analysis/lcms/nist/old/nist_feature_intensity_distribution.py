import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from scipy import stats

# Load data
ms2_inchikeys = set(pickle.load(open('data/ms2_inchikey_gnps.pkl', 'rb')))

# Set Arial font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']


def plot_combined_distribution(evs=[0, 10, 20], y_range=None, dataset_spacing=1.5):
    plt.figure(figsize=(5, 3))  # Slightly increased height to accommodate legend
    colors = ['#8ca5c0', '#ca9a96']
    whisker_color = '0.5'
    font_color = '0.15'

    all_data = []
    median_positions = []
    p_values = []

    for ev in evs:
        df = pd.read_csv('data/merged_ms1_gnps.tsv', sep='\t', low_memory=False)
        df = df[~df['MS1_inchikey'].isnull()]
        df = df[df['file'].str.contains(f'_{ev}eV')].reset_index(drop=True)
        df = df.sort_values(by='peak_height', ascending=False)
        df['MS1_inchikey14'] = df['MS1_inchikey'].str[:14]
        df = df.drop_duplicates(subset='MS1_inchikey14', keep='first')

        in_ms2 = df[df['MS1_inchikey14'].isin(ms2_inchikeys)]['peak_height']
        not_in_ms2 = df[~df['MS1_inchikey14'].isin(ms2_inchikeys)]['peak_height']

        all_data.extend([in_ms2, not_in_ms2])
        median_positions.append(np.median(in_ms2))

        # Perform Mann-Whitney U test
        statistic, p_value = stats.mannwhitneyu(in_ms2, not_in_ms2, alternative='two-sided')
        p_values.append(p_value)

    positions = []
    for i in range(len(evs)):
        positions.extend([i * dataset_spacing - 0.25, i * dataset_spacing + 0.25])

    bp = plt.boxplot(all_data, positions=positions, widths=0.25, patch_artist=True,
                     showfliers=False, medianprops=dict(color="white", linewidth=1))

    for element in ['whiskers', 'caps']:
        for item in bp[element]:
            item.set_color(whisker_color)

    for i, box in enumerate(bp['boxes']):
        box.set(facecolor=to_rgba(colors[i % 2], alpha=0.85), edgecolor='none')

    plt.yscale('log')
    plt.ylabel('Peak height', fontsize=12, color=font_color)

    plt.xticks([i * dataset_spacing for i in range(len(evs))], [f'MS1 ({ev} eV)' for ev in evs],
               color=font_color, fontsize=12)

    plt.yticks(color=font_color, fontsize=10)

    if y_range is not None:
        plt.ylim(y_range)

    plt.tick_params(axis='x', which='major', length=2.5, width=0.5, color=whisker_color, pad=4)
    plt.tick_params(axis='y', which='major', length=2.5, width=0.5, color=whisker_color, pad=2)
    plt.tick_params(axis='y', which='minor', length=2, width=0.5, color=whisker_color, pad=2)

    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Set color for remaining spines
    plt.gca().spines['left'].set_edgecolor(whisker_color)
    plt.gca().spines['bottom'].set_edgecolor(whisker_color)

    for i, data in enumerate(all_data):
        y = data
        x = np.random.normal(positions[i], 0.04, size=len(y))
        plt.scatter(x, y, alpha=0.2, s=2, color=colors[i % 2], zorder=3)

    # Add dots at the median of 'overlap with MS/MS annotation' boxes and connect with a dashed line
    # median_x = [i * dataset_spacing - 0.25 for i in range(len(evs))]
    # plt.plot(median_x, median_positions, color='0.5', linestyle='--', linewidth=1, zorder=4)

    # Add legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, facecolor=colors[0], edgecolor='none', alpha=0.85,
                      label='Overlap with MS/MS annotations'),
        plt.Rectangle((0, 0), 1, 1, facecolor=colors[1], edgecolor='none', alpha=0.85, label='Non-overlap'),
    ]
    plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.1),
               ncol=2, fontsize=9, frameon=False)

    # Add p-values to the plot
    for i, p_value in enumerate(p_values):
        plt.text(i * dataset_spacing, plt.ylim()[1] - 1e9, f'P = {p_value:.2e}',
                 horizontalalignment='center', verticalalignment='bottom',
                 fontsize=9, color=font_color)

    plt.tight_layout()
    plt.savefig('data/combined_peak_height_distribution.svg', transparent=True, bbox_inches='tight')
    plt.show()
    plt.close()


y_range = (1.5e5, 1.5e9)
plot_combined_distribution(evs=[0, 10, 20], y_range=y_range, dataset_spacing=1.5)