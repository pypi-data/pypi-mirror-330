import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def get_peak_height_ls():
    df = pd.read_pickle('data/aligned_feature_table_all.pkl')

    # max intensity
    df['max_intensity'] = df.iloc[:, 22:28].max(axis=1)

    ms2_dda_ph_ls = df[df['similarity'].notnull()]['max_intensity'].tolist()
    ms1_dda_ph_ls = df[df['ms1_dda_inchikeys'].notnull()]['max_intensity'].tolist()
    ms1_0ev_ph_ls = df[df['ms1_0ev_inchikeys'].notnull()]['max_intensity'].tolist()
    ms1_10ev_ph_ls = df[df['ms1_10ev_inchikeys'].notnull()]['max_intensity'].tolist()
    ms1_20ev_ph_ls = df[df['ms1_20ev_inchikeys'].notnull()]['max_intensity'].tolist()

    return ms2_dda_ph_ls, ms1_dda_ph_ls, ms1_0ev_ph_ls, ms1_10ev_ph_ls, ms1_20ev_ph_ls


# Set up the plot
plt.rcParams['font.family'] = 'Arial'
fig, ax = plt.subplots(figsize=(5, 1.85))

# Get peak height data
peak_heights = get_peak_height_ls()

# Labels for x-axis
labels = ['MS/MS\n(DDA)', 'MS1\n(DDA)', 'MS1\n(0 eV)', 'MS1\n(10 eV)', 'MS1\n(20 eV)']

# Plot scatter points behind the box
for i, heights in enumerate(peak_heights):
    x = np.random.normal(i + 1, 0.04, len(heights))
    ax.scatter(x, heights, alpha=0.1, s=2, color='blue', edgecolors='none', zorder=1)

# Create box plot
box_color = 'lightgrey'
box_width = 0.3  # Adjust this value to change the width of the boxes
box_plot = ax.boxplot(peak_heights, patch_artist=True, tick_labels=labels, showfliers=False, widths=box_width)

# Customize box appearance
for element in ['boxes', 'fliers', 'means', 'medians']:
    plt.setp(box_plot[element], color='none')

# Set only whiskers color
plt.setp(box_plot['whiskers'], color='0.5')
plt.setp(box_plot['caps'], color='0.5')

for median in box_plot['medians']:
    median.set(color='white', linewidth=1.5)

for patch in box_plot['boxes']:
    patch.set_facecolor(box_color)
    patch.set_edgecolor('none')
    patch.set_alpha(0.8)

# Customize the plot
ax.set_ylabel('Peak height', fontsize=12, fontname='Arial', labelpad=8, color='0.2')
ax.set_yscale('log')

# Set y-axis limits and show minor ticks
ax.set_ylim(2e5, 1.5e8)
ax.yaxis.set_minor_locator(plt.LogLocator(subs=np.arange(2, 10)))

# Customize ticks and remove top and right spines
ax.tick_params(axis='x', which='major', labelsize=10, pad=5, length=2, colors='0.2')
ax.tick_params(axis='y', which='major', labelsize=8, pad=2, length=2, colors='0.2')
ax.tick_params(axis='y', which='minor', length=1, colors='0.2')  # Show minor ticks
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('0.5')
ax.spines['left'].set_color('0.5')

# Set x-axis and y-axis label font to Arial and color to 0.2
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontname('Arial')
    label.set_color('0.2')

# Adjust the space between the first box and y-axis
plt.xlim(0.3, len(labels) + 0.5)

# # Calculate Mann-Whitney U test and add p-values with lines
# ms2_dda = peak_heights[0]
# y_max = ax.get_ylim()[1]
# line_heights = [0.45, 0.8, 1.15, 1.5]  # Adjusted heights for each comparison

# for i, (other_data, line_height) in enumerate(zip(peak_heights[1:], line_heights), start=1):
#     statistic, p_value = stats.mannwhitneyu(ms2_dda, other_data, alternative='two-sided')
#     p_text = f'$\it{{P}}$ = {p_value:.2e}'
#
#     # Draw line
#     x1, x2 = 1, i + 1
#     y = y_max * line_height
#     ax.plot([x1, x1, x2, x2], [y, y + y_max * 0.02, y + y_max * 0.02, y],
#             lw=1, color='0.5')
#
#     # Add p-value text
#     ax.text((x1 + x2) * 0.5, y, p_text,
#             ha='center', va='bottom', fontsize=8, color='0.2')
#
# # Adjust y-axis limit to show the lines and p-values
# ax.set_ylim(2e5, y_max * 1.9)

print("Cap coordinates for each box:")
for i in range(len(labels)):
    bottom_cap = box_plot['caps'][2*i].get_ydata()[0]
    top_cap = box_plot['caps'][2*i + 1].get_ydata()[0]
    print(f"{labels[i]}:")
    print(f"  Bottom cap: {bottom_cap}")
    print(f"  Top cap: {top_cap}")

# # Add dashed lines connecting top and bottom caps
# bright_color = '#FF4500'  # Bright orange-red color
# for i in range(2, 4):  # Connect 3rd to 4th, then 4th to 5th
#     # Connect top caps
#     top_cap_y = box_plot['caps'][2 * i - 1].get_ydata()[0]  # Y-coordinate of current box's top cap
#     next_top_cap_y = box_plot['caps'][2 * i + 1].get_ydata()[0]  # Y-coordinate of next box's top cap
#     ax.plot([i + 1, i + 2], [top_cap_y, next_top_cap_y], color=bright_color, linestyle='--', linewidth=1, zorder=3)
#
#     # Connect bottom caps
#     bottom_cap_y = box_plot['caps'][2 * i - 2].get_ydata()[0]  # Y-coordinate of current box's bottom cap
#     next_bottom_cap_y = box_plot['caps'][2 * i].get_ydata()[0]  # Y-coordinate of next box's bottom cap
#     ax.plot([i + 1, i + 2], [bottom_cap_y, next_bottom_cap_y], color=bright_color, linestyle='--', linewidth=1,
#             zorder=3)

plt.tight_layout()

# Save as svg
plt.savefig('data/peak_height_boxplot.svg', transparent=True, bbox_inches='tight')

plt.show()