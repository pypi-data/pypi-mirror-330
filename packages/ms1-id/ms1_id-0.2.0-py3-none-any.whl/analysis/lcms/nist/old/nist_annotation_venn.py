import pickle
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

ms2_inchikeys = set(pickle.load(open('../data/ms2_inchikey_gnps.pkl', 'rb')))
ms1_0ev_inchikeys = set(pickle.load(open('../data/ms1_inchikey_gnps_0ev.pkl', 'rb')))
ms1_10ev_inchikeys = set(pickle.load(open('../data/ms1_inchikey_gnps_10ev.pkl', 'rb')))
# ms1_20ev_inchikeys = set(pickle.load(open('data/ms1_inchikey_gnps_20ev.pkl', 'rb')))


colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95', '#ca9a96', '#facaa9']

# Set the font to Arial
plt.rcParams['font.family'] = 'Arial'

# Create the figure and axis
fig, ax = plt.subplots(figsize=(1.6, 1.6))

# Create the Venn diagram
v = venn3([ms2_inchikeys, ms1_0ev_inchikeys, ms1_10ev_inchikeys],
          # set_labels=('MS/MS', 'MS1 (0 eV)', 'MS1 (10 eV)'),
          set_labels=('', '', ''),
          set_colors=(colors[0], colors[3], colors[5]))

# Customize the diagram
for text in v.set_labels:
    text.set_fontsize(8)
for text in v.subset_labels:
    text.set_fontsize(6)

# Add circles for a cleaner look
# venn3_circles([ms2_inchikeys, ms1_0ev_inchikeys, ms1_10ev_inchikeys], linewidth=0.5, color="gray")

plt.tight_layout()

# Save the figure (optional)
plt.savefig('ms_venn_diagram_gnps.svg', transparent=True)

# Show the plot
plt.show()