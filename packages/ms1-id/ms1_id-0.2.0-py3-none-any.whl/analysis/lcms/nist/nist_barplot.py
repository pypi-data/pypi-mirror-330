# colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95', '#ca9a96', '#facaa9']

import matplotlib.pyplot as plt
import numpy as np

data = {
    'MS/MS\n(DDA)': [567, 0, 0],
    'MS1\n(DDA)': [64, 242, 0],
    'MS1\n(0 eV)': [80, 247, 157],
    'MS1\n(10 eV)': [98, 249, 164],
    'MS1\n(20 eV)': [138, 261, 205]
}

categories = ['MS/MS collected in DDA',
              'No MS/MS collected in DDA',
              'New annotations from newly detected features']

colors = ['#56648a', '#8ca5c0', '#ca9a96']

# Set up the plot
bar_width = 0.65  # Width of each bar (0-1)
starting_width = 0.5  # Space between y-axis and first bar

# Create the stacked bar plot
fig, ax = plt.subplots(figsize=(4.5, 3))  # Increased height to accommodate top legend

x = np.arange(len(data))  # the label locations
bottom = np.zeros(len(data))

for i, cat in enumerate(categories):
    values = [data[key][i] for key in data.keys()]
    ax.bar(x + starting_width, values, bar_width, bottom=bottom, label=cat, color=colors[i], alpha=0.5)

    # Add individual numbers inside each bar
    for j, v in enumerate(values):
        if v > 0:
            ax.text(j + starting_width, bottom[j] + v / 2, str(v), ha='center', va='center',
                    fontsize=10.5, fontname='Arial', color='0.1')

    bottom += values

# Customize the plot
ax.set_ylabel('Annotated features', fontsize=15, fontname='Arial', labelpad=8, color='0.2')
ax.set_xticks(x + starting_width)
ax.set_xticklabels(data.keys())

# Customize ticks and remove top and right spines
ax.tick_params(axis='x', which='major', labelsize=12, pad=5, length=2, colors='0.2')
ax.tick_params(axis='y', which='major', labelsize=10, pad=1.5, length=2, colors='0.2')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('0.5')
ax.spines['left'].set_color('0.5')

# Set x-axis and y-axis label font to Arial and color to 0.2
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontname('Arial')
    label.set_color('0.2')

# # Customize legend
# legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35),
#                    frameon=False, ncol=1,
#                    prop={'family': 'Arial', 'size': 11.25})
#
# # Explicitly set the legend text color
# for text in legend.get_texts():
#     text.set_color('0.2')

# Add total value labels on top of the bars
for i, mode in enumerate(data.keys()):
    total = sum(data[mode])
    ax.text(i + starting_width, total, str(total), ha='center', va='bottom', fontsize=10.5, fontname='Arial', color='0.1')

# Adjust layout and display the plot
plt.tight_layout()

# Save as svg
plt.savefig('data/bar_plot.svg', transparent=True, bbox_inches='tight')

plt.show()