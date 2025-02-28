import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from tqdm import tqdm


def fill_zeros(row):
    row = pd.to_numeric(row, errors='coerce')
    non_zero_min = row[row > 0].min() if (row > 0).any() else 0
    fill_value = min(30000, 0.1 * non_zero_min)
    return row.fillna(fill_value).replace(0, fill_value)


def calculate_fold_change(group1_data, group2_data):
    return group1_data.mean() / group2_data.mean()


def remove_outliers_iqr(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data >= lower_bound) & (data <= upper_bound)]


def perform_statistical_analysis(mode):
    df = pd.read_csv(
        f'/Users/shipei/Documents/projects/ms1_id/data/PR000639/{mode}_aligned_feature_table_with_metadata.tsv',
        sep='\t', low_memory=False)

    diagnosis = df.iloc[0]
    sex = df.iloc[1]

    data = df.iloc[2:]

    metadata_cols = list(data.columns[:22]) + list(data.columns[-8:])
    data_cols = [col for col in data.columns if col not in metadata_cols]

    data[data_cols] = data[data_cols].apply(fill_zeros, axis=1)

    comparisons = [
        ('nonIBD', 'CD', None),
        ('nonIBD', 'UC', None),
        ('nonIBD', 'CD', 'male'),
        ('nonIBD', 'CD', 'female'),
        ('nonIBD', 'UC', 'male'),
        ('nonIBD', 'UC', 'female')
    ]

    results = {}

    for comparison in comparisons:
        group1, group2, gender = comparison

        if gender:
            cols1 = [col for col in data_cols if diagnosis[col] == group1 and sex[col].lower() == gender.lower()]
            cols2 = [col for col in data_cols if diagnosis[col] == group2 and sex[col].lower() == gender.lower()]
        else:
            cols1 = [col for col in data_cols if diagnosis[col] == group1]
            cols2 = [col for col in data_cols if diagnosis[col] == group2]

        print(f"Comparison: {comparison}")
        print(f"Number of columns in group1: {len(cols1)}")
        print(f"Number of columns in group2: {len(cols2)}")

        p_values = []
        fold_changes = []
        for _, row in tqdm(data[data_cols].iterrows(), desc=f"Processing {comparison}"):
            group1_data = row[cols1].astype(float)
            group2_data = row[cols2].astype(float)

            # Remove outliers for each group separately
            group1_data_clean = remove_outliers_iqr(group1_data)
            group2_data_clean = remove_outliers_iqr(group2_data)

            if len(group1_data_clean) > 0 and len(group2_data_clean) > 0:
                stat, p = stats.mannwhitneyu(group1_data_clean, group2_data_clean, alternative='two-sided')
                fc = calculate_fold_change(group1_data_clean, group2_data_clean)
                p_values.append(p)
                fold_changes.append(fc)
            else:
                p_values.append(np.nan)
                fold_changes.append(np.nan)

        valid_p_values = [p for p in p_values if not np.isnan(p)]
        if valid_p_values:
            _, p_corrected, _, _ = multipletests(valid_p_values, method='fdr_bh')
            p_corrected_full = [p_corrected[valid_p_values.index(p)] if not np.isnan(p) else np.nan for p in p_values]
        else:
            p_corrected_full = [np.nan] * len(p_values)

        comparison_name = f"{group1}_vs_{group2}{'_' + gender if gender else ''}"
        results[f"{comparison_name}_p_value"] = p_values
        results[f"{comparison_name}_p_value_corrected"] = p_corrected_full
        results[f"{comparison_name}_fold_change"] = fold_changes

    result_df = pd.DataFrame(results, index=data.index)
    combined_df = pd.concat([data, result_df], axis=1)
    cols_order = metadata_cols + data_cols + list(results.keys())
    combined_df = combined_df[cols_order]

    return combined_df


def stats_main():
    modes = ['hilic_pos', 'hilic_neg', 'c8_pos', 'c18_neg']

    for mode in modes:
        print(f"\nProcessing {mode}...")
        results = perform_statistical_analysis(mode)
        results.to_csv(
            f'/Users/shipei/Documents/projects/ms1_id/data/PR000639/{mode}_statistical_analysis_with_outlier_removal.tsv',
            sep='\t', index=False)


def merge_all_modes():
    """
    merge all modes into one DataFrame, only shared columns are kept
    """
    modes = ['hilic_pos', 'hilic_neg', 'c8_pos', 'c18_neg']

    dfs = []
    for mode in modes:
        df = pd.read_csv(
            f'/Users/shipei/Documents/projects/ms1_id/data/PR000639/{mode}_statistical_analysis_with_outlier_removal.tsv',
            sep='\t', low_memory=False)
        print(f"Number of columns in {mode}: {len(df.columns)}")
        df['mode'] = mode
        dfs.append(df)

    common_columns = set(dfs[0].columns[30:-19])
    for df in dfs[1:]:
        common_columns = common_columns.intersection(set(df.columns[30:-19]))

    common_columns = list(common_columns)
    common_columns = dfs[0].columns[:30].tolist() + dfs[0].columns[-19:].tolist() + common_columns

    print(f"Number of common columns: {len(common_columns)}")

    dfs_common = [df[common_columns] for df in dfs]

    combined_df = pd.concat(dfs_common, axis=0)

    print(f"Shape of combined DataFrame: {combined_df.shape}")

    combined_df.to_csv('all_modes_statistical_analysis_with_outlier_removal.tsv',
                       sep='\t', index=False)


if __name__ == '__main__':
    stats_main()
    merge_all_modes()