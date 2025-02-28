import pandas as pd


def find_demo(file):
    """
    find demo: one annotation, multi adduct forms
    """

    df = pd.read_csv(
        f'/Users/shipei/Documents/projects/ms1_id/data/nist/data_1/output_gnps/{file}',
        sep='\t', low_memory=False)

    # Filter out rows with null MS1_similarity
    df = df[df['MS1_similarity'].notnull()].reset_index(drop=True)

    # Group by MS1_inchikey and aggregate
    grouped = df.groupby('MS1_inchikey').agg({
        'MS1_precursor_type': lambda x: list(set(x)),  # List unique precursor types
        'MS1_annotation': 'first',  # Keep the first MS1_annotation for reference
        'MS1_similarity': 'max',  # Keep the max MS1_similarity for reference
    })

    # Add a column for the count of unique adduct forms
    grouped['adduct_count'] = grouped['MS1_precursor_type'].apply(len)

    # Filter groups with more than one unique MS1_precursor_type
    multi_adduct = grouped[grouped['adduct_count'] > 1]

    # Sort by number of unique adducts (descending) and then by MS1_similarity (descending)
    multi_adduct = multi_adduct.sort_values(['adduct_count', 'MS1_similarity'], ascending=[False, False])

    # Display the results
    print(f"Total unique InChIKeys with multiple adduct forms: {len(multi_adduct)}")
    print("\nTop 10 entries:")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(multi_adduct.head(10))

    # save
    multi_adduct.to_csv('data/multi_adduct_forms.tsv', sep='\t', index=True)

    print("\nResults have been saved to 'multi_adduct_forms.csv'")


if __name__ == '__main__':
    find_demo('NIST_pool_1_10eV_feature_table.tsv')
