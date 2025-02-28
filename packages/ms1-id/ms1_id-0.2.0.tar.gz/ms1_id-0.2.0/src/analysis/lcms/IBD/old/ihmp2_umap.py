import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from umap import UMAP
import seaborn as sns
import pickle


def preprocess_df():
    df = pd.read_csv('all_modes_statistical_analysis.tsv', sep='\t', low_memory=False)
    print(f"Original shape: {df.shape}")

    # remove all cols starting with 'PREF' (pool reference mixture)
    df = df.loc[:, ~df.columns.str.startswith('PREF')]

    # filter out rows with score and matched peaks
    df = df[(df['MS1_similarity'] >= 0.70) & (df['MS1_matched_peak'] >= 4)].reset_index(drop=True)

    # sort by MS1 inchikey, then by MS1_similarity
    df = df.sort_values(['MS1_inchikey', 'MS1_similarity'], ascending=[True, False]).reset_index(drop=True)

    # remove duplicated MS1 inchikey
    df = df.drop_duplicates('MS1_inchikey', keep='first').reset_index(drop=True)

    ########################################################
    # Select data columns
    data_columns = df.columns[49:]
    # Extract the data to plot
    plot_data = df[data_columns].copy()

    # Cap the data at the 95th percentile
    plot_data = plot_data.apply(lambda row: row.clip(upper=np.percentile(row, 95)))

    # log transformation
    plot_data = np.log(plot_data + 1)

    # Perform z-score normalization within each row after log transformation
    plot_data_normalized = plot_data.apply(lambda x: (x - x.mean()) / x.std(), axis=1)

    ########################################################
    meta = pd.read_csv('gnps_df_with_npclassifier_info.tsv', sep='\t', low_memory=False)
    # dict from inchikey to superclass
    inchikey_to_superclass = dict(zip(meta['INCHIKEY'], meta['SUPERCLASS']))
    # dict from inchikey to npsuperclass
    inchikey_to_npsuperclass = dict(zip(meta['INCHIKEY'], meta['npsuperclass']))
    # dict from inchikey to nppathway
    inchikey_to_nppathway = dict(zip(meta['INCHIKEY'], meta['nppathway']))

    # add to df
    df['superclass'] = df['MS1_inchikey'].map(inchikey_to_superclass)
    df['npsuperclass'] = df['MS1_inchikey'].map(inchikey_to_npsuperclass)
    df['nppathway'] = df['MS1_inchikey'].map(inchikey_to_nppathway)

    # save
    df.to_csv('all_modes_statistical_analysis_refined.tsv', sep='\t', index=False)
    pickle.dump(plot_data_normalized, open('plot_data_normalized.pkl', 'wb'))

    return df, plot_data_normalized


def plot_umap(df, plot_data_normalized, color_by='superclass', n_neighbors=15, min_dist=0.1, n_components=2):

    df = df.dropna(subset=[color_by])
    # df = df[~df[color_by].str.contains(';')].reset_index(drop=True)

    df[color_by] = df[color_by].apply(lambda x: x.split(';')[0] if ';' in x else x)

    # Perform UMAP
    umap_model = UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components, random_state=12)
    umap_result = umap_model.fit_transform(plot_data_normalized)

    # Create a DataFrame with UMAP results
    umap_df = pd.DataFrame(data=umap_result, columns=['UMAP1', 'UMAP2'])
    umap_df[color_by] = df[color_by]

    plt.rcParams['font.family'] = 'Arial'

    # Plot

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.spines['left'].set_visible(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    # Remove x and y axis labels
    ax.set_xlabel('UMAP1')
    ax.set_ylabel('UMAP2')

    # Remove x and y axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    sns.scatterplot(data=umap_df, x='UMAP1', y='UMAP2', hue=color_by, palette='deep', legend=False)
    # plt.title(f'UMAP plot colored by {color_by}')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()

    # save
    plt.savefig(f'umap.svg', format='svg', bbox_inches='tight', transparent=True)

    plt.show()


from sklearn.manifold import TSNE
import colorsys

def adjust_color(color, saturation_factor=0.7, brightness_factor=1.2):
    """
    Adjust a color by reducing saturation and increasing brightness.
    """
    r, g, b = color[:3]  # Get RGB values, ignore alpha if present
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = max(0, min(1, s * saturation_factor))  # Reduce saturation and clip to [0, 1]
    l = max(0, min(1, l * brightness_factor))  # Increase lightness and clip to [0, 1]
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (r, g, b)

def plot_tsne(df, plot_data_normalized, fig_size=(10, 6), legend=True,
              color_by='superclass', n_components=2, perplexity=30, n_iter=1000):
    df = df.copy()  # Create a copy to avoid SettingWithCopyWarning
    df = df.dropna(subset=[color_by])

    # Handle multiple values in the color_by column
    df[color_by] = df[color_by].apply(lambda x: x.split(';')[0] if ';' in x else x)

    # Perform t-SNE
    tsne_model = TSNE(n_components=n_components, perplexity=perplexity, max_iter=n_iter, random_state=1)
    tsne_result = tsne_model.fit_transform(plot_data_normalized)

    # Create a DataFrame with t-SNE results
    tsne_df = pd.DataFrame(data=tsne_result, columns=['tSNE1', 'tSNE2'])
    tsne_df[color_by] = df[color_by]

    # Create a custom color palette with 11 distinct colors
    base_colors = plt.cm.tab10(np.linspace(0, 1, 10)).tolist()
    base_colors.append([0.8, 0.8, 0.8, 1])  # Add an 11th color (light gray)

    # Adjust the colors
    colors = [adjust_color(color, saturation_factor=0.7, brightness_factor=1.15) for color in base_colors]

    plt.rcParams['font.family'] = 'Arial'

    # Plot
    fig, ax = plt.subplots(figsize=fig_size)

    ax.spines['left'].set_visible(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    # Set axis labels
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Remove x and y axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Use the custom palette in the scatterplot
    scatter = sns.scatterplot(data=tsne_df, x='tSNE1', y='tSNE2', hue=color_by, palette=colors, ax=ax)

    # Adjust legend
    if legend:
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    else:
        ax.get_legend().remove() if ax.get_legend() else None

    plt.tight_layout()

    # Save the plot
    plt.savefig(f'tsne_{color_by}.svg', format='svg', bbox_inches='tight', transparent=True)

    plt.show()


if __name__ == '__main__':
    # df, plot_data_normalized = preprocess_df()

    ########################################################
    # Load data
    df = pd.read_csv('all_modes_statistical_analysis_refined.tsv', sep='\t', low_memory=False)
    plot_data_normalized = pickle.load(open('plot_data_normalized.pkl', 'rb'))

    # Plot UMAP with different color options
    # plot_umap(df, plot_data_normalized, color_by='superclass', n_neighbors=15, min_dist=0.1)
    # plot_umap(df, plot_data_normalized, color_by='nppathway', n_neighbors=15, min_dist=0.1)

    # Plot t-SNE with different color options
    plot_tsne(df, plot_data_normalized, color_by='superclass', perplexity=30, n_iter=1000,
              fig_size=(10, 6), legend=True)
    # plot_tsne(df, plot_data_normalized, color_by='superclass', perplexity=30, n_iter=1000, fig_size=(6, 6),
    #           legend=False)

