import matplotlib.pyplot as plt
import numpy as np

# Data
omnivore = [4032568.0, 5721773.0]
vegan = [827748.0, 2833706.0]

# Set up the plot style
plt.rcParams['font.family'] = 'Arial'

# Define color scheme
group_colors = {'Omnivore': '#56648a', 'Vegan': '#facaa9'}

# Create the scatter plot
fig, ax = plt.subplots(figsize=(1.8, 1.8))

# Define groups and their positions
groups = ['Omnivore', 'Vegan']
positions = {group: i for i, group in enumerate(groups)}

# Plot scatter points
for i, (group, data) in enumerate(zip(groups, [omnivore, vegan])):
    x = np.random.normal(i, 0.05, len(data))
    ax.scatter(x, data, alpha=0.9, s=25, color=group_colors[group], edgecolors='none', zorder=2)

# Add group means
for i, (group, data) in enumerate(zip(groups, [omnivore, vegan])):
    mean = np.mean(data)
    ax.plot([i-0.2, i+0.2], [mean, mean], color='0.5', linewidth=1.5, zorder=1)

# Customize the plot
ax.set_ylabel('Peak height', fontsize=10, fontname='Arial', labelpad=3.5, color='0.2')
ax.set_ylim(0, 7e6)

# Customize ticks and remove top and right spines
ax.set_xticks([0, 1])
ax.set_xticklabels(groups)
ax.tick_params(axis='x', which='major', labelsize=10, pad=4, length=1.2, colors='0.2')
ax.tick_params(axis='y', which='major', labelsize=10, pad=2.5, length=2, colors='0.2')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('0.5')
ax.spines['left'].set_color('0.5')

# Set x-axis and y-axis label font to Arial and color to 0.2
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontname('Arial')
    label.set_color('0.2')

plt.tight_layout()

# Save as svg
plt.savefig('data/scatter_plot_omnivore_vs_vegan.svg', transparent=True, bbox_inches='tight')
plt.show()