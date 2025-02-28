import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load data
ms2_dda_inchikey = pickle.load(open('data/ms2_dda_inchikey.pkl', 'rb'))
ms1_dda_inchikey = pickle.load(open('data/ms1_dda_inchikey.pkl', 'rb'))
ms1_0ev_inchikey = pickle.load(open('data/ms1_0ev_inchikey.pkl', 'rb'))
ms1_10ev_inchikey = pickle.load(open('data/ms1_10ev_inchikey.pkl', 'rb'))
ms1_20ev_inchikey = pickle.load(open('data/ms1_20ev_inchikey.pkl', 'rb'))

metadata_df = pd.read_csv(
    '/Users/shipei/Documents/projects/chemical_conjugate/main/gnps_lib/metadata_df_with_npclassifier_info.tsv',
    sep='\t')

# dict from inchikey to superclass
inchikey_to_superclass = dict(zip(metadata_df['INCHIKEY_14'], metadata_df['SUPERCLASS']))
inchikey_to_class = dict(zip(metadata_df['INCHIKEY_14'], metadata_df['CLASS']))


# Function to count molecules for each superclass in a dataset
def count_molecules(dataset, inchikey_to_class_dict):
    counts = {}
    for inchikey in dataset:
        if inchikey in inchikey_to_class_dict:
            _class = inchikey_to_class_dict[inchikey]
            if pd.notna(_class):  # Only count non-NaN classes
                counts[_class] = counts.get(_class, 0) + 1
    return counts


# Count molecules for each dataset
datasets = {
    'MS1 (20 eV)': ms1_20ev_inchikey,
    'MS1 (10 eV)': ms1_10ev_inchikey,
    'MS1 (0 eV)': ms1_0ev_inchikey,
    'MS1 (DDA)': ms1_dda_inchikey,
    'MS/MS (DDA)': ms2_dda_inchikey
}

all_counts = {name: count_molecules(dataset, inchikey_to_superclass) for name, dataset in datasets.items()}

# Get unique superclasses, excluding NaN values
all_superclasses = list(set.union(*[set(counts.keys()) for counts in all_counts.values()]))

# Create a DataFrame for easier plotting
df = pd.DataFrame(index=datasets.keys(), columns=all_superclasses)
for dataset, counts in all_counts.items():
    for superclass in all_superclasses:
        df.loc[dataset, superclass] = counts.get(superclass, 0)

# Fill NaN values with 0
df = df.fillna(0)

# Calculate total annotations for each class
total_annotations = df.sum()

# Filter classes with total number larger than 10
# filtered_classes = total_annotations[total_annotations > 10].index
# df = df[filtered_classes].reset_index()

# Sort classes by total annotations (descending order)
sorted_classes = df.sum().sort_values(ascending=False).index

# # Sort classes alphabetically
# sorted_classes = sorted(df.columns)

# Reorder DataFrame columns based on sorted superclasses
df = df[sorted_classes]

# Create the plot
plt.rcParams['font.family'] = 'Arial'
fig, ax = plt.subplots(figsize=(6, 3.3))

# Add light grey grid and set it to the background
ax.grid(True, color='0.9', linestyle='-', linewidth=0.4, alpha=0.6, zorder=0)

# Plot circles with individual numbers
for i, dataset in enumerate(df.index):
    for j, superclass in enumerate(df.columns):
        count = df.loc[dataset, superclass]
        if count > 0:
            ax.scatter(j, i, s=3 * count + 50, c='#facaa9', alpha=1.0, edgecolors='none', zorder=2)  # Increase zorder
            ax.text(j, i, str(int(count)), ha='center', va='center', fontsize=8, color='0.15',
                    zorder=3)  # Increase zorder

# Customize the plot
ax.set_xticks(range(len(df.columns)))
ax.set_xticklabels(df.columns, rotation=-35, ha='right', fontsize=8, color='0.15')
ax.xaxis.tick_top()  # Move x-axis labels to the top
ax.xaxis.set_label_position('top')  # Move x-axis label to the top
ax.set_yticks(range(len(datasets)))
ax.set_yticklabels(datasets.keys(), fontsize=10, color='0.15')

# Remove all frames
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Remove ticks
ax.tick_params(axis='both', which='both', length=0)

# Adjust layout
plt.tight_layout()

# Save as SVG
plt.savefig('data/cmpd_class_dot.svg', format='svg', bbox_inches='tight')
plt.show()
