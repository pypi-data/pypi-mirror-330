import pandas as pd
import numpy as np


def calculate_fdr_vs_score(search, min_matched_peak=4, score_range=np.arange(0.60, 0.96, 0.05)):
    df = pd.read_csv(f'{search}_results_mces.tsv', sep='\t')

    # Filter the dataframe
    df = df[(pd.notnull(df['mces_dist'])) & (df['ion_mode_match'])].reset_index(drop=True)
    df = df[df['matched_peak'] >= min_matched_peak].reset_index(drop=True)

    # Define the match condition
    df['match'] = df['mces_dist'] <= mces_dist_cutoff

    fdr_results = []
    for score_cutoff in score_range:
        df_filtered = df[df['score'] >= score_cutoff]
        if df_filtered.empty:
            fdr = np.nan
        else:
            fdr = (df_filtered['match'] == False).sum() / df_filtered.shape[0]
        fdr_results.append((score_cutoff, fdr))

    return pd.DataFrame(fdr_results, columns=['score_cutoff', 'fdr'])


def calculate_fdr_vs_score_merged(min_matched_peak=4, score_range=np.arange(0.60, 0.96, 0.05)):
    df1 = pd.read_csv('k0_results_mces.tsv', sep='\t')
    df2 = pd.read_csv('k10_results_mces.tsv', sep='\t')

    df = pd.concat([df1, df2]).reset_index(drop=True)

    # Define the match condition
    df['match'] = df['mces_dist'] <= mces_dist_cutoff

    # Filter the dataframe
    df = df[(pd.notnull(df['mces_dist'])) & (df['ion_mode_match'])].reset_index(drop=True)
    df = df[df['matched_peak'] >= min_matched_peak].reset_index(drop=True)
    # sort by score
    df = df.sort_values('score', ascending=False)

    fdr_results = []
    for score_cutoff in score_range:
        df_filtered = df[df['score'] >= score_cutoff]
        df_filtered = df_filtered.drop_duplicates(subset=['qry_db_id', 'matched_db_id'])
        if df_filtered.empty:
            fdr = np.nan
        else:
            fdr = (df_filtered['match'] == False).sum() / df_filtered.shape[0]
        fdr_results.append((score_cutoff, fdr))

    return pd.DataFrame(fdr_results, columns=['score_cutoff', 'fdr'])


def gen_all_results(min_matched_peak=4):
    fdr_df_k0 = calculate_fdr_vs_score('k0', min_matched_peak)
    fdr_df_k0['mode'] = 'k0'

    fdr_df_k10 = calculate_fdr_vs_score('k10', min_matched_peak)
    fdr_df_k10['mode'] = 'k10'

    fdr_df = calculate_fdr_vs_score_merged(min_matched_peak)
    fdr_df['mode'] = 'merged'

    # merge dfs
    fdr_df = pd.concat([fdr_df_k0, fdr_df_k10, fdr_df]).reset_index(drop=True)

    fdr_df.to_csv(f'fdr_df_minpeak{min_matched_peak}.tsv', sep='\t', index=False)


import matplotlib.pyplot as plt


def plot(min_matched_peak):
    # Read the data
    df = pd.read_csv(f'fdr_df_minpeak{min_matched_peak}.tsv', sep='\t')

    # Set the font to Arial
    plt.rcParams['font.family'] = 'Arial'

    # Create the plot
    plt.figure(figsize=(5, 3))

    # Plot lines and scatter points for each mode
    for i, mode in enumerate(df['mode'].unique()):
        mode_data = df[df['mode'] == mode]
        label = ['Non-scaled', 'Scaled', 'Search both'][i]
        plt.plot(mode_data['score_cutoff'], mode_data['fdr'], label=label)
        plt.scatter(mode_data['score_cutoff'], mode_data['fdr'], s=15)

    # Customize the plot
    plt.xlabel('Score cutoff', fontname='Arial', fontsize=14, labelpad=8, color='0.2')
    plt.ylabel('FDR', fontname='Arial', fontsize=14, labelpad=6, color='0.2')
    plt.legend(prop={'family': 'Arial'})
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.ylim(0, 0.6)

    plt.title(f'Minimum matched peak: {min_matched_peak}', fontname='Arial', fontsize=14, pad=10, color='0.2')

    # Adjust frame color to 0.4 (gray) and increase tick length
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_edgecolor('0.4')
    ax.tick_params(width=1, length=2, color='0.4')

    # Ensure all text uses Arial
    for text in plt.gca().get_children():
        if isinstance(text, plt.Text):
            text.set_fontname('Arial')

    # Show the plot
    plt.tight_layout()

    # save as svg
    plt.savefig(f'fdr_plot_minpeak{min_matched_peak}.svg', transparent=True)
    plt.show()


if __name__ == '__main__':
    mces_dist_cutoff = 4

    # gen_all_results(min_matched_peak=3)
    # gen_all_results(min_matched_peak=4)
    # gen_all_results(min_matched_peak=5)
    # gen_all_results(min_matched_peak=6)

    plot(min_matched_peak=3)
    plot(min_matched_peak=4)
    plot(min_matched_peak=5)
    plot(min_matched_peak=6)
