import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Load data
ms2_inchikeys = set(pickle.load(open('data/ms2_inchikey_gnps.pkl', 'rb')))
ms1_dda_inchikeys = set(pickle.load(open('data/ms1_inchikey_gnps_DDA.pkl', 'rb')))
ms1_0ev_inchikeys = set(pickle.load(open('data/ms1_inchikey_gnps_0ev.pkl', 'rb')))
ms1_10ev_inchikeys = set(pickle.load(open('data/ms1_inchikey_gnps_10ev.pkl', 'rb')))
ms1_20ev_inchikeys = set(pickle.load(open('data/ms1_inchikey_gnps_20ev.pkl', 'rb')))

# Calculate overlaps
ms2_overlap = [
    len(ms2_inchikeys.intersection(ms2_inchikeys)),
    len(ms2_inchikeys.intersection(ms1_dda_inchikeys)),
    len(ms2_inchikeys.intersection(ms1_0ev_inchikeys)),
    len(ms2_inchikeys.intersection(ms1_10ev_inchikeys)),
    len(ms2_inchikeys.intersection(ms1_20ev_inchikeys))
]

total_counts = [
    len(ms2_inchikeys),
    len(ms1_dda_inchikeys),
    len(ms1_0ev_inchikeys),
    len(ms1_10ev_inchikeys),
    len(ms1_20ev_inchikeys)
]

non_overlap = [total - overlap for total, overlap in zip(total_counts, ms2_overlap)]

# Set up the plot
plt.rcParams['font.family'] = 'Arial'
fig, ax = plt.subplots(figsize=(4, 3))

# Create the stacked bars
bar_width = 0.65
index = np.arange(5)

colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95', '#ca9a96', '#facaa9']
# Add transparency
overlap_color = mcolors.to_rgba(colors[2], alpha=0.7)
non_overlap_color = mcolors.to_rgba(colors[4], alpha=0.7)

p1 = ax.bar(index, ms2_overlap, bar_width, color=overlap_color, label='Overlap with MS/MS annotations')
p2 = ax.bar(index[1:], non_overlap[1:], bar_width, bottom=ms2_overlap[1:], color=non_overlap_color, label='Non-overlap')

# Customize the plot
ax.set_ylabel('Annotated metabolites', fontsize=12, color='0.2')
ax.set_xticks(index)
ax.set_xticklabels(('MS/MS\n(DDA)', 'MS1\n(DDA)', 'MS1\n(0 eV)',
                    'MS1\n(10 eV)', 'MS1\n(20 eV)'), fontsize=10, color='0.15')
# ax.legend(fontsize=10)

# Adjust frame
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('0.4')
ax.spines['bottom'].set_color('0.4')

# Adjust tick length and pad
ax.tick_params(axis='x', which='major', labelsize=10, length=2.5, width=1, pad=3.5, color='0.4', labelcolor='0.2')
ax.tick_params(axis='y', which='major', labelsize=10, length=2.5, width=1, pad=1.5, color='0.4', labelcolor='0.2')


def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:,}',
                    xy=(rect.get_x() + rect.get_width() / 2, rect.get_y() + height / 2),
                    xytext=(0, 0),
                    textcoords="offset points",
                    ha='center', va='center', fontsize=9, color='0.1')


if __name__ == '__main__':
    add_labels(p1)
    add_labels(p2)

    # Adjust layout and display
    plt.tight_layout()
    # plt.savefig('data/ms_data_comparison_bar_plot.svg', transparent=True,
    #             bbox_inches='tight')
    plt.show()
