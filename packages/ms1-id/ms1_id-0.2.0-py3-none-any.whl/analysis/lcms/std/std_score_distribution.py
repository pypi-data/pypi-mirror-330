import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def similarity_scores(search='k0'):

    ba_names = pd.read_csv('/data/std_mix/BA_std.tsv', sep='\t')['name'].tolist()
    drug_names = pd.read_csv('/data/std_mix/drug_std.tsv', sep='\t')['name'].tolist()

    data_dir = f'./output_{search}'

    files = [f for f in os.listdir(data_dir) if f.endswith('.tsv') and f.startswith('mixture')]

    all_scores = []
    for f in files:
        df = pd.read_csv(os.path.join(data_dir, f), sep='\t')
        df = df[df['MS1_similarity'].notnull()].reset_index(drop=True)

        # filter out BAs and drugs
        if 'Bile_acids' in f:
            df = df[df['MS1_annotation'].isin(ba_names)].reset_index(drop=True)
        elif 'Drugs' in f:
            df = df[df['MS1_annotation'].isin(drug_names)].reset_index(drop=True)

        df = df[(df['MS1_matched_peak'] >= 4) & (df['MS1_spectral_usage'] >= 0.20)].reset_index(drop=True)

        all_scores += df['MS1_similarity'].tolist()

    print(f'{search}: {len(all_scores)} MS1 scores')
    # save
    np.save(f'data/ms1_scores_{search}.npy', np.array(all_scores))


def plot_score_distributions(searches=['k0', 'k10', 'all'], legend=True, bw_adjust=1.0):
    # Set the font to Arial for all elements
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']

    fig, ax = plt.subplots(figsize=(8.5, 5))

    legend_labels = {
        'k0': 'No peak scaling',
        'k10': 'Peak scaling applied',
        'all': 'Search both'
    }
    colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95', '#ca9a96', '#facaa9']
    color_mapping = {
        'k0': colors[4],
        'k10': colors[2],
        'all': colors[0]
    }

    for search in searches:
        scores = np.load(f'data/ms1_scores_{search}.npy')
        if legend:
            sns.kdeplot(scores,
                        label=legend_labels[search],
                        fill=True, ax=ax,
                        color=color_mapping[search],
                        bw_adjust=bw_adjust)
        else:
            sns.kdeplot(scores,
                        fill=True, ax=ax,
                        color=color_mapping[search],
                        bw_adjust=bw_adjust)

    # Add vertical line at score of 0.7
    ax.axvline(x=0.7, color='0.2', linestyle='--', linewidth=1.25)

    # Remove grid
    ax.grid(False)

    # Adjust frame colors
    for spine in ax.spines.values():
        spine.set_edgecolor('0.4')

    # Adjust tick length and padding
    ax.tick_params(axis='x', which='major', length=3, width=1, pad=4, colors='0.3')
    ax.tick_params(axis='y', which='major', length=3, width=1, pad=1.5, colors='0.3')

    ax.set_xlabel('Similarity score', fontname='Arial', color='0.2', fontsize=18, labelpad=10)
    ax.set_ylabel('Density', fontname='Arial', color='0.2', fontsize=18, labelpad=10)

    if legend:
        ax.legend(prop={'family': 'Arial'})

    ax.set_xlim(-0.002, 1.002)

    # Ensure tick labels are also in Arial and colored '0.4'
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontname('Arial')
        label.set_fontsize(12)
        label.set_color('0.3')

    plt.tight_layout()
    plt.savefig('data/ms1_score_distributions.svg', transparent=True)
    plt.show()


if __name__ == '__main__':
    # similarity_scores(search='k0')
    # similarity_scores(search='k10')
    # similarity_scores(search='all')

    plot_score_distributions(legend=False, bw_adjust=0.7)
