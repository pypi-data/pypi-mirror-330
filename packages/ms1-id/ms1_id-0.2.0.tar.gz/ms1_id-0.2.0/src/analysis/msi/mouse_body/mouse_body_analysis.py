import pandas as pd


df = pd.read_csv('/Users/shipei/Documents/projects/ms1_id/imaging/mouse_body/wb xenograft in situ metabolomics test - rms_corrected/ms1_id_annotations_all.tsv', sep='\t', low_memory=False)

df = df[~pd.isnull(df['inchikey'])].reset_index(drop=True)

print(f"Number of unique inchikeys: {df['inchikey'].nunique()}")
