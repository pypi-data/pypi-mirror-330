import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def get_peak_height_ls():
    df = pd.read_pickle('data/aligned_feature_table_all.pkl')
    df['max_intensity'] = df.iloc[:, 22:28].max(axis=1)

    ms2_dda_ph_ls = df[df['similarity'].notnull()]['max_intensity'].tolist()
    ms1_dda_ph_ls = df[df['ms1_dda_inchikeys'].notnull()]['max_intensity'].tolist()
    ms1_0ev_ph_ls = df[df['ms1_0ev_inchikeys'].notnull()]['max_intensity'].tolist()
    ms1_10ev_ph_ls = df[df['ms1_10ev_inchikeys'].notnull()]['max_intensity'].tolist()
    ms1_20ev_ph_ls = df[df['ms1_20ev_inchikeys'].notnull()]['max_intensity'].tolist()

    return ms2_dda_ph_ls, ms1_dda_ph_ls, ms1_0ev_ph_ls, ms1_10ev_ph_ls, ms1_20ev_ph_ls


# Set up the plot
plt.rcParams['font.family'] = 'Arial'
fig, ax = plt.subplots(figsize=(4.85, 1.95))

# Get peak height data
peak_heights = get_peak_height_ls()

# Labels for y-axis
labels = ['MS1 (20 eV)', 'MS1 (10 eV)', 'MS1 (0 eV)', 'MS1 (DDA)', 'MS/MS (DDA)']

# Plot scatter points behind the box
for i, heights in enumerate(reversed(peak_heights)):
    y = np.random.normal(i + 1, 0.05, len(heights))
    ax.scatter(heights, y, alpha=0.15, s=2.5, color='blue', edgecolors='none', zorder=1)

# Create box plot
box_color = 'lightgrey'
box_width = 0.35
box_plot = ax.boxplot(list(reversed(peak_heights)), vert=False, patch_artist=True, labels=labels, showfliers=False,
                      widths=box_width)

# Customize box appearance
for element in ['boxes', 'fliers', 'means', 'medians']:
    plt.setp(box_plot[element], color='none')

plt.setp(box_plot['whiskers'], color='0.5')
plt.setp(box_plot['caps'], color='0.5')

for median in box_plot['medians']:
    median.set(color='white', linewidth=1.5)

for patch in box_plot['boxes']:
    patch.set_facecolor(box_color)
    patch.set_edgecolor('none')
    patch.set_alpha(0.85)

# Customize the plot
ax.set_xlabel('Peak height of annotated features', fontsize=12, fontname='Arial', labelpad=3.5, color='0.2')
ax.set_xscale('log')

# Set x-axis limits and show minor ticks
ax.set_xlim(2.45e5, 1.5e8)
ax.xaxis.set_minor_locator(plt.LogLocator(subs=np.arange(2, 10)))

# Customize ticks and remove top and right spines
ax.tick_params(axis='y', which='major', labelsize=10, pad=5, length=1.5, colors='0.2')
ax.tick_params(axis='x', which='major', labelsize=8, pad=2, length=2, colors='0.2')
ax.tick_params(axis='x', which='minor', length=1.3, colors='0.2')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('0.5')
ax.spines['left'].set_color('0.5')

# Set x-axis and y-axis label font to Arial and color to 0.2
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontname('Arial')
    label.set_color('0.2')

# Adjust the space between the first box and x-axis
plt.ylim(0.3, len(labels) + 0.5)

plt.tight_layout()

# Save as svg
plt.savefig('data/peak_height_vertical_boxplot.svg', transparent=True, bbox_inches='tight')

plt.show()


# Perform Mann-Whitney U test
ms2_dda_ph_ls, ms1_dda_ph_ls, ms1_0ev_ph_ls, ms1_10ev_ph_ls, ms1_20ev_ph_ls = peak_heights

comparisons = [
    ('MS/MS (DDA)', 'MS1 (DDA)', ms2_dda_ph_ls, ms1_dda_ph_ls),
    ('MS/MS (DDA)', 'MS1 (0 eV)', ms2_dda_ph_ls, ms1_0ev_ph_ls),
    ('MS/MS (DDA)', 'MS1 (10 eV)', ms2_dda_ph_ls, ms1_10ev_ph_ls),
    ('MS/MS (DDA)', 'MS1 (20 eV)', ms2_dda_ph_ls, ms1_20ev_ph_ls)
]

print("Mann-Whitney U test results:")
for group1, group2, data1, data2 in comparisons:
    statistic, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
    print(f"{group1} vs {group2}: p-value = {p_value:.4e}")