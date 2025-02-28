import os
import pickle
import pandas as pd
from tqdm import tqdm
import requests
from collections import Counter
from rdkit import Chem
from myopic_mces import MCES


def remove_stereochemistry(smiles):
    if pd.isnull(smiles):
        return smiles

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None  # Invalid SMILES

    Chem.RemoveStereochemistry(mol)
    new_smiles = Chem.MolToSmiles(mol)

    return new_smiles


def calculate_mces(smiles1, smiles2):
    try:
        mces_result = MCES(smiles1, smiles2, threshold=5, always_stronger_bound=False)
        return mces_result[1]
    except:
        return None


def inchikey_to_smiles(inchikey):
    """
    Convert an InChIKey to SMILES using the PubChem PUG REST API.
    If the original InChIKey isn't found, it tries with a modified version. -UHFFFAOYSA-N
    """
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def fetch_cid(key):
        cid_url = f"{base_url}/compound/inchikey/{key}/cids/JSON"
        response = requests.get(cid_url)
        if response.status_code != 200:
            return None
        data = response.json()
        return data.get("IdentifierList", {}).get("CID", [None])[0]

    def fetch_smiles(cid):
        smiles_url = f"{base_url}/compound/cid/{cid}/property/IsomericSMILES/JSON"
        response = requests.get(smiles_url)
        if response.status_code != 200:
            return None
        data = response.json()
        return data.get("PropertyTable", {}).get("Properties", [{}])[0].get("IsomericSMILES")

    # Try with original InChIKey
    cid = fetch_cid(inchikey)

    if cid is None:
        # If not found, modify InChIKey and try again
        modified_inchikey = inchikey[:14] + "-UHFFFAOYSA-N"
        print(f"Original InChIKey not found. Trying modified InChIKey: {modified_inchikey}")
        cid = fetch_cid(modified_inchikey)

    if cid is None:
        print(f"No CID found for InChIKey {inchikey} or its modified version")
        return None

    smiles = fetch_smiles(cid)
    if smiles is None:
        print(f"No SMILES found for CID {cid}")
        return None

    return smiles


def gen_all_smiles():
    df1 = pd.read_csv('k0_results.tsv', sep='\t')
    df2 = pd.read_csv('k10_results.tsv', sep='\t')
    df = pd.concat([df1, df2]).reset_index(drop=True)

    # dict from qry_inchikey_14 to qry_smiles
    dict_1 = dict(zip(df['qry_inchikey_14'], df['qry_smiles']))
    df1['matched_smiles'] = df1['matched_inchikey_14'].map(dict_1, na_action='ignore')  # update df1
    df2['matched_smiles'] = df2['matched_inchikey_14'].map(dict_1, na_action='ignore')

    # rest inchikey_14 without smiles
    remain_qry_inchikey_14 = set(df1[df1['qry_smiles'].isnull()]['qry_inchikey_14']) | set(
        df2[df2['qry_smiles'].isnull()]['qry_inchikey_14'])
    remain_matched_inchikey_14 = set(df1[df1['matched_smiles'].isnull()]['matched_inchikey_14']) | set(
        df2[df2['matched_smiles'].isnull()]['matched_inchikey_14'])

    all_inchikeys = list(remain_qry_inchikey_14 | remain_matched_inchikey_14)
    # remove nan
    all_inchikeys = [x for x in all_inchikeys if pd.notnull(x)]

    print(f"Total unique InChIKeys w/o SMILES: {len(all_inchikeys)}")

    ########################################################
    cmpd_metadata = pd.read_parquet('/Users/shipei/Documents/resources/cmpd_properties/20230806_merged_metadata_drug_Nina_Corinna_DOA_GNPS.parquet',
                                    engine='pyarrow')
    cmpd_metadata = cmpd_metadata[['split_inchikey', 'canonical_smiles']]
    # remove rows with nan, using pd.notnull
    cmpd_metadata = cmpd_metadata[pd.notnull(cmpd_metadata['split_inchikey']) & pd.notnull(cmpd_metadata['canonical_smiles'])].reset_index(drop=True)
    # drop duplicates
    cmpd_metadata = cmpd_metadata.drop_duplicates('split_inchikey').reset_index(drop=True)
    # dict from split_inchikey to canonical_smiles
    cmpd_metadata_dict = dict(zip(cmpd_metadata['split_inchikey'], cmpd_metadata['canonical_smiles']))

    ########################################################
    # Convert InChIKeys to SMILES, using GNPS DB
    # load gnps db metadata df
    gnps = pd.read_pickle('/Users/shipei/Documents/projects/ms1_id/data/ms2db/gnps.pkl')
    gnps = gnps[['inchikey_14', 'smiles']]
    # remove nan rows
    gnps = gnps[(gnps['inchikey_14'].notnull()) & (gnps['smiles'].notnull()) & (gnps['smiles'] != 'N/A')].reset_index(
        drop=True)
    # Group by inchikey_14 and find the most common SMILES for each
    gnps_grouped = gnps.groupby('inchikey_14')['smiles'].agg(lambda x: Counter(x).most_common(1)[0][0]).reset_index()
    # Convert to dictionary for faster lookup
    gnps_dict = dict(zip(gnps_grouped['inchikey_14'], gnps_grouped['smiles']))

    ########################################################
    # create a dictionary to store InChIKey to SMILES
    inchikey_to_smiles_dict = {}
    for inchikey in tqdm(all_inchikeys):
        if inchikey in cmpd_metadata_dict:
            inchikey_to_smiles_dict[inchikey] = cmpd_metadata_dict[inchikey]
        elif inchikey in gnps_dict:
            inchikey_to_smiles_dict[inchikey] = gnps_dict[inchikey]
        else:
            continue

    # save, inchikeys are first 14 characters
    pickle.dump(inchikey_to_smiles_dict, open('inchikey_to_smiles_dict.pkl', 'wb'))

    ########################################################
    # update df1 and df2 with smiles
    df1.loc[df1['qry_smiles'].isnull(), 'qry_smiles'] = df1.loc[df1['qry_smiles'].isnull(), 'qry_inchikey_14'].map(inchikey_to_smiles_dict)
    df1.loc[df1['matched_smiles'].isnull(), 'matched_smiles'] = df1.loc[df1['matched_smiles'].isnull(), 'matched_inchikey_14'].map(inchikey_to_smiles_dict)

    df2.loc[df2['qry_smiles'].isnull(), 'qry_smiles'] = df2.loc[df2['qry_smiles'].isnull(), 'qry_inchikey_14'].map(inchikey_to_smiles_dict)
    df2.loc[df2['matched_smiles'].isnull(), 'matched_smiles'] = df2.loc[df2['matched_smiles'].isnull(), 'matched_inchikey_14'].map(inchikey_to_smiles_dict)

    ########################################################
    # remove stereochemistry
    df1['qry_smiles'] = df1['qry_smiles'].apply(remove_stereochemistry)
    df1['matched_smiles'] = df1['matched_smiles'].apply(remove_stereochemistry)

    df1.to_csv('k0_results_smiles.tsv', sep='\t', index=False)
    df2.to_csv('k10_results_smiles.tsv', sep='\t', index=False)


def calc_mces_for_all(mode='k0'):
    # Read the CSV file
    df = pd.read_csv(f'{mode}_results_smiles.tsv', sep='\t')

    # Initialize mces_dist column with None
    df['mces_dist'] = None

    # Fill rows with the same inchikey_14 with 0
    df.loc[df['qry_inchikey_14'] == df['matched_inchikey_14'], 'mces_dist'] = 0

    # Get unique pairs of SMILES for different inchikey_14
    unique_pairs = df[
        (df['mces_dist'].isna()) &
        (pd.notnull(df['qry_smiles'])) &
        (pd.notnull(df['matched_smiles']))
        ][['qry_smiles', 'matched_smiles']].drop_duplicates()

    # Calculate MCES for unique pairs
    if os.path.exists('mces_dict.pkl'):
        mces_dict = pickle.load(open('mces_dict.pkl', 'rb'))
    else:
        mces_dict = {}

    for _, row in tqdm(unique_pairs.iterrows(), total=len(unique_pairs)):

        if (row['qry_smiles'], row['matched_smiles']) in mces_dict:
            continue

        mces = calculate_mces(row['qry_smiles'], row['matched_smiles'])
        mces_dict[(row['qry_smiles'], row['matched_smiles'])] = mces

    # Save the MCES dictionary
    pickle.dump(mces_dict, open('mces_dict.pkl', 'wb'))

    # Fill back the MCES values
    df.loc[df['mces_dist'].isna(), 'mces_dist'] = df[df['mces_dist'].isna()].apply(
        lambda row: mces_dict.get((row['qry_smiles'], row['matched_smiles'])), axis=1
    )

    # Save the results
    df.to_csv(f'{mode}_results_mces.tsv', sep='\t', index=False)


if __name__ == '__main__':

    gen_all_smiles()

    calc_mces_for_all('k0')

    calc_mces_for_all('k10')
