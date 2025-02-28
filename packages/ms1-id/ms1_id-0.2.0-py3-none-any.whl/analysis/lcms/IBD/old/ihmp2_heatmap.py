import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def load_data():

    df = pd.read_csv('filtered_statistical_analysis_manual.tsv', sep='\t', low_memory=False)

    df = df[df['selected']].reset_index(drop=True)

    # sort by show_name
    df = df.sort_values('show_name').reset_index(drop=True)

    print(f"Number of selected features: {df.shape[0]}")
    return df


def heatmap(df, colormap='coolwarm'):
    plt.rcParams['font.family'] = 'Arial'

    metadata = pd.read_csv('/data/PR000639/metadata/metadata.csv')

    # Define the custom colors for diagnoses and sex
    diagnosis_colors = {'nonIBD': '#56648a', 'UC': '#8ca5c0', 'CD': '#facaa9'}
    sex_colors = {'Male': 'lightblue', 'Female': 'pink'}

    # Create ordering for the diagnoses and sex
    diagnosis_order = ['nonIBD', 'CD', 'UC']
    sex_order = ['Male', 'Female']

    # Create a new column in metadata that combines diagnosis and sex
    metadata['group'] = metadata['Diagnosis'] + ' ' + metadata['sex']

    # Create a custom order for the combined groups
    group_order = [f"{d} {s}" for d in diagnosis_order for s in sex_order]

    # Select data columns (starting from the 52nd column)
    data_columns = df.columns[51:]

    # Extract the data to plot
    plot_data = df[data_columns]

    # Cap the top 1% intensities to the 99th percentile for each row
    # plot_data = plot_data.apply(lambda row: row.clip(upper=np.percentile(row, 99)))

    # Apply log transformation (adding a small constant to avoid log(0))
    epsilon = 1e-10
    plot_data_log = np.log(plot_data + epsilon)

    # Perform z-score normalization within each row after log transformation
    plot_data_normalized = plot_data_log.apply(lambda x: (x - x.mean()) / x.std(), axis=1)

    # Calculate total z-scores for each sample
    total_z_scores = plot_data_normalized.sum()

    # Add total z-scores to metadata
    metadata['total_z_score'] = metadata['local_sample_id'].map(total_z_scores)

    # Create a sorting key for the group order
    metadata['group_order'] = metadata['group'].map({g: i for i, g in enumerate(group_order)})

    # Sort the metadata based on group order and total z-score within each group
    metadata_sorted = metadata.sort_values(['group_order', 'total_z_score'], ascending=[True, False])

    # Get the sorted sample names
    sorted_samples = metadata_sorted['local_sample_id']

    # Reorder columns based on sorted samples
    plot_data_normalized = plot_data_normalized[sorted_samples]

    # Create the heatmap
    plt.figure(figsize=(20, 5))
    g = sns.clustermap(plot_data_normalized,
                       col_cluster=False,
                       row_cluster=False,
                       yticklabels=df['show_name'],
                       xticklabels=False,
                       cmap=colormap,
                       center=0,
                       linewidths=0,
                       figsize=(20, 5))

    # Move y-axis labels to the left side and make ticks shorter
    g.ax_heatmap.yaxis.tick_left()
    g.ax_heatmap.yaxis.set_label_position('left')
    g.ax_heatmap.tick_params(axis='y', length=2)

    # Add colored bars to indicate diagnosis and sex
    ax_col = g.ax_col_dendrogram
    ax_col.set_visible(True)

    # Add color bars
    for i, sample in enumerate(sorted_samples):
        diagnosis = metadata.loc[metadata['local_sample_id'] == sample, 'Diagnosis'].iloc[0]
        sex = metadata.loc[metadata['local_sample_id'] == sample, 'sex'].iloc[0]
        ax_col.add_patch(plt.Rectangle((i, 0.5), 1, 0.5, facecolor=diagnosis_colors[diagnosis], edgecolor='none'))
        ax_col.add_patch(plt.Rectangle((i, 0), 1, 0.5, facecolor=sex_colors[sex], edgecolor='none'))

    ax_col.set_xlim(0, len(sorted_samples))
    ax_col.set_ylim(0, 1)
    ax_col.axis('off')

    plt.tight_layout()

    # save
    plt.savefig('heatmap.svg', transparent=True)
    plt.show()


def heatmap_2(df, colormap='coolwarm'):
    """
    heatmap, without sex
    """
    plt.rcParams['font.family'] = 'Arial'

    metadata = pd.read_csv('/data/PR000639/metadata/metadata.csv')

    # Define the custom colors for diagnoses
    diagnosis_colors = {'nonIBD': '#56648a', 'UC': '#8ca5c0', 'CD': '#facaa9'}

    # Create ordering for the diagnoses
    diagnosis_order = ['nonIBD', 'CD', 'UC']

    # Select data columns (starting from the 52nd column)
    data_columns = df.columns[51:]

    # Extract the data to plot
    plot_data = df[data_columns]

    # Cap the top 1% intensities to the 99th percentile for each row
    # plot_data = plot_data.apply(lambda row: row.clip(upper=np.percentile(row, 99)))

    # Apply log transformation (adding a small constant to avoid log(0))
    epsilon = 1e-10
    plot_data_log = np.log(plot_data + epsilon)

    # Perform z-score normalization within each row after log transformation
    plot_data_normalized = plot_data_log.apply(lambda x: (x - x.mean()) / x.std(), axis=1)

    # Calculate total z-scores for each sample
    total_z_scores = plot_data_normalized.sum()

    # Add total z-scores to metadata
    metadata['total_z_score'] = metadata['local_sample_id'].map(total_z_scores)

    # Create a sorting key for the diagnosis order
    metadata['diagnosis_order'] = metadata['Diagnosis'].map({d: i for i, d in enumerate(diagnosis_order)})

    # Sort the metadata based on diagnosis order and total z-score within each diagnosis
    metadata_sorted = metadata.sort_values(['diagnosis_order', 'total_z_score'], ascending=[True, False])

    # Get the sorted sample names
    sorted_samples = metadata_sorted['local_sample_id']

    # Reorder columns based on sorted samples
    plot_data_normalized = plot_data_normalized[sorted_samples]

    # Create the heatmap
    plt.figure(figsize=(20, 5))
    g = sns.clustermap(plot_data_normalized,
                       col_cluster=False,
                       row_cluster=False,
                       yticklabels=df['show_name'],
                       xticklabels=False,
                       cmap=colormap,
                       center=0,
                       linewidths=0,
                       figsize=(20, 5))

    # Move y-axis labels to the left side and make ticks shorter
    g.ax_heatmap.yaxis.tick_left()
    g.ax_heatmap.yaxis.set_label_position('left')
    g.ax_heatmap.tick_params(axis='y', length=2)

    # Add colored bars to indicate diagnosis
    ax_col = g.ax_col_dendrogram
    ax_col.set_visible(True)

    # Add color bars
    for i, sample in enumerate(sorted_samples):
        diagnosis = metadata.loc[metadata['local_sample_id'] == sample, 'Diagnosis'].iloc[0]
        ax_col.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=diagnosis_colors[diagnosis], edgecolor='none'))

    ax_col.set_xlim(0, len(sorted_samples))
    ax_col.set_ylim(0, 1)
    ax_col.axis('off')

    plt.tight_layout()

    # save
    plt.savefig('heatmap.svg', transparent=True)
    plt.show()


def bar_plot_1(df, fig_size=(2.2, 3.75)):
    max_fc = 2
    # Create the x_axis values
    df['x_axis'] = df['nonIBD_vs_CD_fold_change'].apply(lambda x: -x if x > 1 else 1 / x)
    df['x_axis'] = df['x_axis'].apply(lambda x: np.sign(x) * max_fc if abs(x) > max_fc else x)

    # Create the scatter plot
    fig, ax = plt.subplots(figsize=fig_size)

    # Set font to Arial
    plt.rcParams['font.family'] = 'Arial'

    # Plot lines connecting each point to the y-axis with breaks for large values
    for i, (x, p_value) in enumerate(zip(df['x_axis'], df['nonIBD_vs_CD_p_value_corrected'])):
        if abs(x) == max_fc:
            # Draw the main part of the line
            ax.plot([0, np.sign(x) * 1.2], [i, i], color='0.5', linewidth=1.8, zorder=1)
            # Draw the break
            break_length = 0.2
            ax.plot([np.sign(x) * (1.2 + break_length), np.sign(x) * max_fc], [i, i], color='0.5', linewidth=1.8, zorder=1)

            # Add double slash to indicate break
            slash_width = 0.15
            slash_height = 0.25
            x_start = np.sign(x) * 1.2
            y_start = i - slash_height / 2
            for j in range(2):
                ax.plot([x_start + j * slash_width * 0.7, x_start + slash_width + j * slash_width * 0.7],
                        [y_start, y_start + slash_height],
                        color='0.5', linewidth=1.5, zorder=2)
        else:
            ax.plot([0, x], [i, i], color='0.5', linewidth=1.8, zorder=1)

        # Add stars for p-value
        if p_value < 0.001:
            stars = '***'
        elif p_value < 0.01:
            stars = '**'
        elif p_value < 0.05:
            stars = '*'
        else:
            stars = ''

        if stars:
            x_text = max(x, 0) + 0.1 if x >= 0 else min(x, 0) - 0.1
            ax.text(x_text, i, stars, ha='left' if x >= 0 else 'right', va='center', fontsize=10)

    # Plot the scatter points
    ax.scatter(df['x_axis'], range(len(df)), color='orange', zorder=3)

    # Add dashed lines to separate metabolites
    for i in range(1, len(df)):
        ax.axhline(y=i - 0.5, color='gray', linestyle='--', linewidth=0.5, zorder=0)

    # Remove x-axis label and y-axis ticks
    ax.set_xlabel('')
    ax.set_yticks([])

    # Remove left and right spines, keep top and bottom
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Add a line at x=0
    ax.axvline(x=0, color='black', linewidth=0.5, zorder=2)

    # Set x-axis limits
    max_x = 2.3
    ax.set_xlim(-max_x, max_x)

    # Set x-ticks and labels
    xticks = [-2, -1, 0, 1, 2]
    ax.set_xticks(xticks)
    ax.set_xticklabels([f'{abs(int(x))}' for x in xticks])

    # Adjust the length of x-axis ticks
    ax.tick_params(axis='x', which='major', length=2, labelsize=8, pad=3)
    ax.tick_params(axis='x', which='minor', length=2)

    # Add background color for areas
    significance_threshold = 1
    ax.axvspan(-max_x, -significance_threshold, facecolor='lightgray', alpha=0.3, zorder=0)
    ax.axvspan(significance_threshold, max_x, facecolor='lightgray', alpha=0.3, zorder=0)

    # Adjust y-axis limits
    ax.set_ylim(-0.5, len(df) - 0.5)

    # Show the plot
    plt.tight_layout()

    # save
    plt.savefig('bar_plot_1.svg', transparent=True)
    plt.show()


def bar_plot_2(df, fig_size=(2.2, 3.75)):
    # Create the x_axis values
    df['x_axis'] = df['nonIBD_vs_UC_fold_change'].apply(lambda x: -x if x > 1 else 1 / x)
    df['x_axis'] = df['x_axis'].apply(lambda x: np.sign(x) * 3 if abs(x) > 3 else x)

    # Create the scatter plot
    fig, ax = plt.subplots(figsize=fig_size)

    # Set font to Arial
    plt.rcParams['font.family'] = 'Arial'

    # Plot lines connecting each point to the y-axis with breaks for large values
    for i, (x, p_value) in enumerate(zip(df['x_axis'], df['nonIBD_vs_UC_p_value_corrected'])):
        if abs(x) == 3:
            # Draw the main part of the line
            ax.plot([0, np.sign(x) * 2.0], [i, i], color='0.5', linewidth=1.8, zorder=1)
            # Draw the break
            break_length = 0.2
            ax.plot([np.sign(x) * (2.0 + break_length), np.sign(x) * 3], [i, i], color='0.5', linewidth=1.8, zorder=1)

            # Add double slash to indicate break
            slash_width = 0.15
            slash_height = 0.25
            x_start = np.sign(x) * 2.0
            y_start = i - slash_height / 2
            for j in range(2):
                ax.plot([x_start + j * slash_width * 0.7, x_start + slash_width + j * slash_width * 0.7],
                        [y_start, y_start + slash_height],
                        color='0.5', linewidth=1.5, zorder=2)
        else:
            ax.plot([0, x], [i, i], color='0.5', linewidth=1.8, zorder=1)

        # Add stars for p-value
        if p_value < 0.001:
            stars = '***'
        elif p_value < 0.01:
            stars = '**'
        elif p_value < 0.05:
            stars = '*'
        else:
            stars = ''

        if stars:
            x_text = max(x, 0) + 0.1 if x >= 0 else min(x, 0) - 0.1
            ax.text(x_text, i, stars, ha='left' if x >= 0 else 'right', va='center', fontsize=10)

    # Plot the scatter points
    ax.scatter(df['x_axis'], range(len(df)), color='orange', zorder=3)

    # Add dashed lines to separate metabolites
    for i in range(1, len(df)):
        ax.axhline(y=i - 0.5, color='gray', linestyle='--', linewidth=0.5, zorder=0)

    # Remove x-axis label and y-axis ticks
    ax.set_xlabel('')
    ax.set_yticks([])

    # Remove left and right spines, keep top and bottom
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(True)
    ax.spines['bottom'].set_visible(True)

    # Add a line at x=0
    ax.axvline(x=0, color='black', linewidth=0.5, zorder=2)

    # Set x-axis limits
    max_x = 2.3
    ax.set_xlim(-max_x, max_x)

    # Set x-ticks and labels
    xticks = [-2, -1, 0, 1, 2]
    ax.set_xticks(xticks)
    ax.set_xticklabels([f'{abs(int(x))}' for x in xticks])

    # Adjust the length of x-axis ticks
    ax.tick_params(axis='x', which='major', length=2, labelsize=8, pad=3)
    ax.tick_params(axis='x', which='minor', length=2)

    # Add background color for areas
    significance_threshold = 1
    ax.axvspan(-max_x, -significance_threshold, facecolor='lightgray', alpha=0.3, zorder=0)
    ax.axvspan(significance_threshold, max_x, facecolor='lightgray', alpha=0.3, zorder=0)

    # Adjust y-axis limits
    ax.set_ylim(-0.5, len(df) - 0.5)

    # Show the plot
    plt.tight_layout()

    # save
    plt.savefig('bar_plot_2.svg', transparent=True)
    plt.show()


if __name__ == '__main__':
    df = load_data()

    # heatmap(df, colormap='coolwarm')
    ### heatmap_2(df, colormap='coolwarm')

    bar_plot_1(df)
    bar_plot_2(df)
