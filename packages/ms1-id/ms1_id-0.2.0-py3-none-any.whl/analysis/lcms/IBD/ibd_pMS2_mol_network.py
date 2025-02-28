"""
run on server
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
import networkx as nx


def main(mode='hilic_pos'):
    # read feature table
    df = pd.read_csv(f'/Users/shipei/Documents/projects/ms1_id/data/PR000639/output/{mode}_aligned_feature_table.tsv',
                     sep='\t', low_memory=False)

    with open(f'data/{mode}_pMS2.mgf', 'w') as f:
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Writing MGF"):
            if pd.notnull(row['pseudo_ms2']):

                pms2 = row['pseudo_ms2'].split(';')
                pms2 = [x.split(' ') for x in pms2][:-1]
                pms2 = [[float(x) for x in y] for y in pms2]
                pms2 = np.array(pms2, dtype=np.float32)

                # remove ions larger than precursor
                pms2 = pms2[pms2[:, 0] < row['m/z'] + 0.1]

                mzs = pms2[:, 0]
                intensities = pms2[:, 1]

                f.write('BEGIN IONS\n')
                f.write(f'NAME={row["MS1_annotation"]}\n')
                f.write(f'PEPMASS={row["m/z"]}\n')
                f.write(f'RTINSECONDS={row["RT"] * 60}\n')
                f.write(f'SCANS={round(row["ID"])}\n')

                for mz, intensity in zip(mzs, intensities):
                    f.write(f'{mz} {intensity}\n')
                f.write('END IONS\n\n')


def demo(frag_ls, name='Tyr',
         mode='hilic_pos'):
    # read feature table
    df = pd.read_csv(f'/Users/shipei/Documents/projects/ms1_id/data/PR000639/output/{mode}_aligned_feature_table.tsv',
                     sep='\t', low_memory=False)
    df[name] = False

    with open(f'data/{mode}_pMS2_{name}.mgf', 'w') as f:
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Writing MGF"):
            if pd.notnull(row['pseudo_ms2']):

                pms2 = row['pseudo_ms2'].split(';')
                pms2 = [x.split(' ') for x in pms2][:-1]
                pms2 = [[float(x) for x in y] for y in pms2]
                pms2 = np.array(pms2, dtype=np.float32)

                # remove ions larger than precursor
                pms2 = pms2[pms2[:, 0] < row['m/z'] + 0.1]

                mzs = pms2[:, 0]
                intensities = pms2[:, 1]

                # Check if all fragments are present with >5% intensity
                mzs_5percent = mzs[intensities > 0.05 * np.max(intensities)]
                if not all(any(np.isclose(mzs_5percent, frag, atol=0.01)) for frag in frag_ls):
                    continue  # Skip this row and move to the next one

                df.loc[_, name] = True

                f.write('BEGIN IONS\n')
                f.write(f'NAME={row["MS1_annotation"]}\n')
                f.write(f'PEPMASS={row["m/z"]}\n')
                f.write(f'RTINSECONDS={row["RT"] * 60}\n')
                f.write(f'SCANS={round(row["ID"])}\n')

                for mz, intensity in zip(mzs, intensities):
                    f.write(f'{mz} {intensity}\n')
                f.write('END IONS\n\n')

    df = df[df[name]].reset_index(drop=True)
    df.to_csv(f'data/{mode}_{name}.tsv', sep='\t', index=False)


from msbuddy import Msbuddy, MsbuddyConfig
from msbuddy.base import MetaFeature, Spectrum


def annotate_formula():
    # read feature table
    df = pd.read_csv(f'/data/PR000639/output/hilic_pos_aligned_feature_table.tsv',
                     sep='\t', low_memory=False)

    df['annotated_formula_rank1'] = ''
    df['annotated_formula_rank2'] = ''
    df['annotated_formula_rank3'] = ''

    # create a MsbuddyConfig object
    msb_config = MsbuddyConfig(ppm=True,
                               ms1_tol=15,
                               ms2_tol=30,
                               halogen=False,
                               timeout_secs=60)
    # instantiate a Msbuddy object
    engine = Msbuddy(msb_config)

    all_metafeatures = []
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        if pd.notnull(row['pseudo_ms2']):
            pms2 = row['pseudo_ms2'].split(';')
            pms2 = [x.split(' ') for x in pms2][:-1]
            pms2 = [[float(x) for x in y] for y in pms2]
            pms2 = np.array(pms2, dtype=np.float32)

            # remove ions larger than precursor
            pms2 = pms2[pms2[:, 0] < row['m/z'] + 0.1]

            mz_array = pms2[:, 0]
            int_array = pms2[:, 1]

            # create a Spectrum object
            ms2_spec = Spectrum(mz_array=mz_array, int_array=int_array)

            # create a MetaFeature object
            metafeature = MetaFeature(identifier=int(row['ID']),  # unique identifier for the MetaFeature object
                                      mz=row['m/z'],  # precursor m/z
                                      rt=row['RT'],  # retention time, can be None if not available
                                      charge=1,  # precursor charge
                                      ms2=ms2_spec)
        else:
            metafeature = MetaFeature(identifier=int(row['ID']),  # unique identifier for the MetaFeature object
                                      mz=row['m/z'],
                                      rt=row['RT'],
                                      charge=1)

        all_metafeatures.append(metafeature)

    # add to the Msbuddy object
    engine.add_data(all_metafeatures)

    # run the annotation
    engine.annotate_formula()

    # get the annotated data
    results = engine.get_summary()

    for result in results:
        mask = df['ID'] == result['identifier']
        df.loc[mask, 'annotated_formula_rank1'] = result['formula_rank_1']
        df.loc[mask, 'annotated_formula_rank2'] = result['formula_rank_2']
        df.loc[mask, 'annotated_formula_rank3'] = result['formula_rank_3']

    df.to_csv(f'data/hilic_pos_annotated_formula.tsv', sep='\t', index=False)


def add_annotations_to_network_file():
    # G = nx.read_graphml('data/mn/hilic_pos.graphml')
    G = nx.read_graphml('data/mn/hilic_pos_Tyr.graphml')

    # read feature table
    ms1_df = pd.read_csv(
        'data/hilic_pos_annotated_formula.tsv',
        sep='\t', low_memory=False)

    stats_df = pd.read_csv(
        '/data/PR000639/hilic_pos_statistical_analysis_with_outlier_removal.tsv',
        sep='\t', low_memory=False)

    # Iterate through all nodes in the graph
    for node, data in G.nodes(data=True):
        mz = data['mz']
        rt = data['rt']

        # find in ms1_df
        ms1_row = ms1_df[
            (ms1_df['m/z'].between(mz - 0.005, mz + 0.005)) & (ms1_df['RT'].between(rt - 0.05, rt + 0.05))].copy()
        if len(ms1_row) > 0:
            # sort by RT difference
            ms1_row['RT_diff'] = np.abs(ms1_row['RT'] - rt)
            ms1_row = ms1_row.sort_values('RT_diff', ascending=True).iloc[0]

            # if annotated
            if not pd.isnull(ms1_row['MS1_annotation']):
                data['MS1_annotation'] = ms1_row['MS1_annotation']
                data['MS1_formula'] = ms1_row['MS1_formula']
                data['MS1_annotated'] = True
                data['MS1_similarity'] = ms1_row['MS1_similarity']
            else:
                data['MS1_annotation'] = ''
                data['MS1_formula'] = ''
                data['MS1_annotated'] = False
                data['MS1_similarity'] = 0.0

            data['ID'] = ms1_row['ID']
            data['annotated_formula_rank1'] = ms1_row['annotated_formula_rank1']
            data['annotated_formula_rank2'] = ms1_row['annotated_formula_rank2']
            data['annotated_formula_rank3'] = ms1_row['annotated_formula_rank3']

            # add stats
            data['nonIBD_vs_CD_p_value_corrected'] = stats_df.loc[ms1_row['ID'], 'nonIBD_vs_CD_p_value_corrected']
            data['nonIBD_vs_UC_p_value_corrected'] = stats_df.loc[ms1_row['ID'], 'nonIBD_vs_UC_p_value_corrected']
            data['min_p_value'] = min(data['nonIBD_vs_CD_p_value_corrected'], data['nonIBD_vs_UC_p_value_corrected'])

            if data['min_p_value'] < 0.001:
                data['significant'] = 0
            elif data['min_p_value'] < 0.01:
                data['significant'] = 1
            elif data['min_p_value'] < 0.05:
                data['significant'] = 2
            else:
                data['significant'] = 3

        else:
            data['MS1_annotation'] = ''
            data['MS1_formula'] = ''
            data['MS1_annotated'] = False
            data['MS1_similarity'] = 0.0

    # Save the modified graph to a new GraphML file
    # nx.write_graphml(G, 'data/mn/hilic_pos_annotations.graphml')
    nx.write_graphml(G, 'data/mn/hilic_pos_Tyr_annotations.graphml')


import matplotlib.pyplot as plt
import seaborn as sns


def box_plot(id_list):
    metadata = pd.read_csv('/data/PR000639/metadata/metadata.csv')
    metadata['Diagnosis'] = metadata['Diagnosis'].replace({'nonIBD': 'Non-IBD'})
    sampleid_to_group = dict(zip(metadata['local_sample_id'], metadata['Diagnosis']))

    # read feature table
    df = pd.read_csv(
        '/data/PR000639/hilic_pos_statistical_analysis.tsv',
        sep='\t', low_memory=False)

    # Set up the plot style
    plt.rcParams['font.family'] = 'Arial'

    # Define color scheme
    diagnosis_colors = {'Non-IBD': '#56648a', 'UC': '#8ca5c0', 'CD': '#facaa9'}

    for id_num in id_list:
        # Filter the dataframe for the current ID
        id_data = df[df['ID'] == id_num]

        print('nonIBD vs CD: ', id_data['nonIBD_vs_CD_p_value'].values[0])
        print('nonIBD vs UC: ', id_data['nonIBD_vs_UC_p_value'].values[0])

        # Prepare data for plotting
        plot_data = []
        for col in id_data.columns:
            if col in sampleid_to_group:
                group = sampleid_to_group[col]
                value = id_data[col].values[0]
                plot_data.append({'Group': group, 'Value': value})

        plot_df = pd.DataFrame(plot_data)

        # Print quantile and median values for all groups
        print(f"\nQuantile and Median values for ID {id_num}:")
        for group in ['Non-IBD', 'CD', 'UC']:
            group_data = plot_df[plot_df['Group'] == group]['Value']
            if not group_data.empty:
                quantiles = group_data.quantile([0.25, 0.5, 0.75])
                print(f"{group}:")
                print(f"  25th percentile: {quantiles[0.25]:.2f}")
                print(f"  Median: {quantiles[0.5]:.2f}")
                print(f"  75th percentile: {quantiles[0.75]:.2f}")
            else:
                print(f"{group}: No data available")

        # Create the box plot
        fig, ax = plt.subplots(figsize=(1.8, 1.8))

        # Define groups and their positions
        groups = ['Non-IBD', 'CD', 'UC']
        positions = {group: i for i, group in enumerate(groups)}

        # Plot scatter points
        for group in groups:
            group_data = plot_df[plot_df['Group'] == group]['Value']
            if not group_data.empty:
                x = np.random.normal(positions[group], 0.05, len(group_data))
                ax.scatter(x, group_data, alpha=0.9, s=2.5, color=diagnosis_colors[group], edgecolors='none', zorder=1)

        # Create box plot
        box_width = 0.5
        box_data = [plot_df[plot_df['Group'] == group]['Value'] for group in groups if
                    not plot_df[plot_df['Group'] == group].empty]
        box_labels = [group for group in groups if not plot_df[plot_df['Group'] == group].empty]

        box_plot = ax.boxplot(box_data, positions=[positions[label] for label in box_labels],
                              patch_artist=True, labels=box_labels,
                              showfliers=False, widths=box_width)

        # Customize box appearance
        for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(box_plot[element], color='0.5')

        for patch, label in zip(box_plot['boxes'], box_labels):
            patch.set_facecolor(diagnosis_colors[label])
            patch.set_edgecolor('none')
            patch.set_alpha(0.6)

        # Customize the plot
        ax.set_ylabel('Peak height', fontsize=10, fontname='Arial', labelpad=3.5, color='0.2')
        # ax.set_yscale('log')

        # Set y-axis limits
        ax.set_ylim(0, 7e6)
        # ax.set_yticks([0, 5e6, 1e7])

        # Customize ticks and remove top and right spines
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

        # plt.title(f'Box Plot for ID: {id_num}', fontsize=14, fontname='Arial', color='0.2')
        plt.tight_layout()

        # Save as svg
        plt.savefig(f'data/boxplot_ID_{id_num}.svg', transparent=True, bbox_inches='tight')
        plt.show()


if __name__ == '__main__':
    ########## make MGF file
    # main('hilic_pos')
    # ########
    # hilic pos, tyrosine-related
    # demo(frag_ls=[182.0830, 165.0560, 136.0770], name='Tyr', mode='hilic_pos')

    ########
    # annotate_formula()

    ########
    # add_annotations_to_network_file()

    ########
    # box_plot(id_list=[19042])
    # box_plot(id_list=[118, 280, 1808, 19042, 1630, 16867, 17379, 2909])

    box_plot(id_list=[6696])
