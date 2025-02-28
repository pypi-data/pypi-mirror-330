import pickle
import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet
import matplotlib.font_manager as fm

# Load the InChIKey sets
hilic_pos = set(pickle.load(open('hilic_pos_inchikey.pkl', 'rb')))
hilic_neg = set(pickle.load(open('hilic_neg_inchikey.pkl', 'rb')))
c8_pos = set(pickle.load(open('c8_pos_inchikey.pkl', 'rb')))
c18_neg = set(pickle.load(open('c18_neg_inchikey.pkl', 'rb')))

# Create a dictionary of sets
data = {
    'HILIC+': hilic_pos,
    'HILIC-': hilic_neg,
    'C8+': c8_pos,
    'C18-': c18_neg
}

# Get all unique InChIKeys as a list
all_inchikeys = list(set.union(*data.values()))

# Create a DataFrame with boolean indicators for each set
df = pd.DataFrame({
    set_name: [inchikey in inchikeys for inchikey in all_inchikeys]
    for set_name, inchikeys in data.items()
}, index=all_inchikeys)

# Count the occurrences of each combination
combinations = df.groupby(list(data.keys())).size()

# Set up fonts
plt.rcParams['font.family'] = 'Arial'

# Font sizes (increased)
TITLE_SIZE = 20
LABEL_SIZE = 24
TICK_SIZE = 14
MODE_NAME_SIZE = 16

# Colors
colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95', '#ca9a96', '#facaa9']

# Create the UpSet plot
fig = plt.figure(figsize=(4, 2))
upset = UpSet(combinations,
              sort_by='cardinality',
              min_subset_size=0,
              show_counts=True,
              orientation='horizontal',
              facecolor=colors[0],
              intersection_plot_elements=10,
              element_size=60)

upset.plot()

# Adjust font sizes
plt.ylabel('Annotated compounds', fontsize=LABEL_SIZE, labelpad=10)

# Adjust tick label sizes
for ax in fig.get_axes():
    ax.tick_params(axis='both', which='major', labelsize=TICK_SIZE)
    for text in ax.texts:
        text.set_fontsize(TICK_SIZE)

# Increase font size for mode names
upset.style_subsets(facecolor='#56648a', edgecolor='black', linewidth=10)

# Manually set the font size for subset labels
for text in plt.gca().texts:
    if text.get_text() in data.keys():
        text.set_fontsize(MODE_NAME_SIZE)

# Adjust the layout
plt.tight_layout()
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

# Save the figure
plt.savefig('inchikey_upset_plot.svg', bbox_inches='tight', transparent=True)
plt.show()