import pickle
from collections import Counter

import pandas as pd
import requests
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Avalon import pyAvalonTools
from rdkit.Chem import AllChem
from tqdm import tqdm


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


def calculate_similarity_metrics(smiles1, smiles2):
    # Convert SMILES to RDKit molecules
    try:
        mol1 = Chem.MolFromSmiles(smiles1)
        mol2 = Chem.MolFromSmiles(smiles2)
    except:
        return None

    if mol1 is None or mol2 is None:
        return None

    # Remove stereochemistry
    Chem.RemoveStereochemistry(mol1)
    Chem.RemoveStereochemistry(mol2)

    # Generate fingerprints for all types
    morgan_fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, 2, nBits=2048)
    morgan_fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, 2, nBits=2048)

    rdkit_fp1 = Chem.RDKFingerprint(mol1)
    rdkit_fp2 = Chem.RDKFingerprint(mol2)

    maccs_fp1 = AllChem.GetMACCSKeysFingerprint(mol1)
    maccs_fp2 = AllChem.GetMACCSKeysFingerprint(mol2)

    # Add PubChem fingerprint
    pubchem_fp1 = AllChem.GetHashedAtomPairFingerprintAsBitVect(mol1, nBits=881)
    pubchem_fp2 = AllChem.GetHashedAtomPairFingerprintAsBitVect(mol2, nBits=881)

    # Add Avalon fingerprint
    avalon_fp1 = pyAvalonTools.GetAvalonFP(mol1)
    avalon_fp2 = pyAvalonTools.GetAvalonFP(mol2)

    # Calculate similarities for each fingerprint type
    morgan_sim = DataStructs.TanimotoSimilarity(morgan_fp1, morgan_fp2)
    rdkit_sim = DataStructs.TanimotoSimilarity(rdkit_fp1, rdkit_fp2)
    maccs_sim = DataStructs.TanimotoSimilarity(maccs_fp1, maccs_fp2)
    pubchem_sim = DataStructs.TanimotoSimilarity(pubchem_fp1, pubchem_fp2)
    avalon_sim = DataStructs.TanimotoSimilarity(avalon_fp1, avalon_fp2)

    return {
        'morgan': morgan_sim,
        'rdkit': rdkit_sim,
        'maccs': maccs_sim,
        'pubchem': pubchem_sim,
        'avalon': avalon_sim
    }


def gen_unique_smiles_for_df():
    df = pd.read_pickle('data/aligned_feature_table_all.pkl')

    all_inchikeys = set()

    # cols: InChIKey, ms1_dda_inchikeys, ms1_0ev_inchikeys, ms1_10ev_inchikeys, ms1_20ev_inchikeys
    for col in ['InChIKey', 'ms1_dda_inchikeys', 'ms1_0ev_inchikeys', 'ms1_10ev_inchikeys', 'ms1_20ev_inchikeys']:
        print(f"Processing column: {col}")
        # Drop NA values and get unique values
        values = df[col].dropna()

        for value in values:
            if isinstance(value, list):
                all_inchikeys.update(value)
            else:
                all_inchikeys.add(value)

    # remove nan inchikey and stereochemistry
    all_inchikeys = [i[:14] for i in all_inchikeys if not pd.isnull(i)]
    all_inchikeys = list(set(all_inchikeys))

    print(f"Total unique InChIKeys: {len(all_inchikeys)}")

    ########################################################
    # Convert InChIKeys to SMILES, using GNPS DB
    # load gnps db metadata df
    gnps = pd.read_pickle('/data/ms2db/gnps.pkl')
    gnps = gnps[['inchikey_14', 'smiles']]
    # remove nan rows
    gnps = gnps[(gnps['inchikey_14'].notnull()) & (gnps['smiles'].notnull()) & (gnps['smiles'] != 'N/A')].reset_index(
        drop=True)
    # Group by inchikey_14 and find the most common SMILES for each
    gnps_grouped = gnps.groupby('inchikey_14')['smiles'].agg(lambda x: Counter(x).most_common(1)[0][0]).reset_index()

    # Convert to dictionary for faster lookup
    gnps_dict = dict(zip(gnps_grouped['inchikey_14'], gnps_grouped['smiles']))

    # create a dictionary to store InChIKey to SMILES
    inchikey_to_smiles_dict = {}
    for inchikey in tqdm(all_inchikeys):
        if inchikey in gnps_dict:
            inchikey_to_smiles_dict[inchikey] = gnps_dict[inchikey]
        else:
            print(f"Could not find SMILES for InChIKey: {inchikey}")
            smiles = inchikey_to_smiles(str(inchikey) + '-UHFFFAOYSA-N')
            if smiles is not None:
                inchikey_to_smiles_dict[inchikey] = smiles
            else:
                inchikey_to_smiles_dict[inchikey] = None

    # save, inchikeys are first 14 characters
    pickle.dump(inchikey_to_smiles_dict, open('data/inchikey_to_smiles_dict.pkl', 'wb'))
    print(f"Total unique SMILES: {len(inchikey_to_smiles_dict)}")


def get_structure_similarity(ms2_inchikey, inchikey_ls, inchikey_to_smiles_dict):
    if not inchikey_ls:
        return None

    if ms2_inchikey in inchikey_ls:  # identical compounds found
        return [1.0, 1.0, 1.0, 1.0, 1.0]

    ms2_smiles = inchikey_to_smiles_dict[ms2_inchikey]
    if ms2_smiles is None:
        return None

    smiles_ls = [inchikey_to_smiles_dict[inchikey] for inchikey in inchikey_ls]
    smiles_ls = [smiles for smiles in smiles_ls if smiles is not None]

    if len(smiles_ls) == 0:
        return None

    for smiles in smiles_ls:
        similarity = calculate_similarity_metrics(ms2_smiles, smiles)
        if similarity is not None:
            return [similarity['morgan'], similarity['rdkit'], similarity['maccs'], similarity['pubchem'], similarity['avalon']]

    return None


def main():
    df = pd.read_pickle('data/aligned_feature_table_all.pkl')
    inchikey_to_smiles_dict = pickle.load(open('data/inchikey_to_smiles_dict.pkl', 'rb'))

    df['ms1_dda_struct_sim'] = [None] * df.shape[0]
    df['ms1_0ev_struct_sim'] = [None] * df.shape[0]
    df['ms1_10ev_struct_sim'] = [None] * df.shape[0]
    df['ms1_20ev_struct_sim'] = [None] * df.shape[0]

    for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
        if pd.isnull(row['InChIKey']):
            continue

        ms2_inchikey = row['InChIKey'][:14]
        ms1_dda_inchikeys = [i[:14] for i in row['ms1_dda_inchikeys'] if pd.notnull(i)] if row['ms1_dda_inchikeys'] else []
        ms1_0ev_inchikeys = [i[:14] for i in row['ms1_0ev_inchikeys'] if pd.notnull(i)] if row['ms1_0ev_inchikeys'] else []
        ms1_10ev_inchikeys = [i[:14] for i in row['ms1_10ev_inchikeys'] if pd.notnull(i)] if row['ms1_10ev_inchikeys'] else []
        ms1_20ev_inchikeys = [i[:14] for i in row['ms1_20ev_inchikeys'] if pd.notnull(i)] if row['ms1_20ev_inchikeys'] else []

        ms1_dda_inchikeys = list(set(ms1_dda_inchikeys))
        ms1_0ev_inchikeys = list(set(ms1_0ev_inchikeys))
        ms1_10ev_inchikeys = list(set(ms1_10ev_inchikeys))
        ms1_20ev_inchikeys = list(set(ms1_20ev_inchikeys))

        df.at[idx, 'ms1_dda_struct_sim'] = get_structure_similarity(ms2_inchikey, ms1_dda_inchikeys,
                                                                    inchikey_to_smiles_dict)
        df.at[idx, 'ms1_0ev_struct_sim'] = get_structure_similarity(ms2_inchikey, ms1_0ev_inchikeys,
                                                                    inchikey_to_smiles_dict)
        df.at[idx, 'ms1_10ev_struct_sim'] = get_structure_similarity(ms2_inchikey, ms1_10ev_inchikeys,
                                                                     inchikey_to_smiles_dict)
        df.at[idx, 'ms1_20ev_struct_sim'] = get_structure_similarity(ms2_inchikey, ms1_20ev_inchikeys,
                                                                     inchikey_to_smiles_dict)

    df.to_pickle('data/aligned_feature_table_all_struct_sim.pkl')


def print_stats():
    df = pd.read_pickle('data/aligned_feature_table_all_struct_sim.pkl')

    print('ms1_dda:')
    print('morgan:', df['ms1_dda_struct_sim'].apply(lambda x: x[0] if x is not None else None).mean())
    print('rdkit:', df['ms1_dda_struct_sim'].apply(lambda x: x[1] if x is not None else None).mean())
    print('maccs:', df['ms1_dda_struct_sim'].apply(lambda x: x[2] if x is not None else None).mean())
    print('pubchem:', df['ms1_dda_struct_sim'].apply(lambda x: x[3] if x is not None else None).mean())
    print('avalon:', df['ms1_dda_struct_sim'].apply(lambda x: x[4] if x is not None else None).mean())

    print('morgan:', df['ms1_dda_struct_sim'].apply(lambda x: x[0] if x is not None else None).median())
    print('rdkit:', df['ms1_dda_struct_sim'].apply(lambda x: x[1] if x is not None else None).median())
    print('maccs:', df['ms1_dda_struct_sim'].apply(lambda x: x[2] if x is not None else None).median())
    print('pubchem:', df['ms1_dda_struct_sim'].apply(lambda x: x[3] if x is not None else None).median())
    print('avalon:', df['ms1_dda_struct_sim'].apply(lambda x: x[4] if x is not None else None).median())

    print('ms1_0ev:')
    print('morgan:', df['ms1_0ev_struct_sim'].apply(lambda x: x[0] if x is not None else None).mean())
    print('rdkit:', df['ms1_0ev_struct_sim'].apply(lambda x: x[1] if x is not None else None).mean())
    print('maccs:', df['ms1_0ev_struct_sim'].apply(lambda x: x[2] if x is not None else None).mean())
    print('pubchem:', df['ms1_0ev_struct_sim'].apply(lambda x: x[3] if x is not None else None).mean())
    print('avalon:', df['ms1_0ev_struct_sim'].apply(lambda x: x[4] if x is not None else None).mean())

    print('morgan:', df['ms1_0ev_struct_sim'].apply(lambda x: x[0] if x is not None else None).median())
    print('rdkit:', df['ms1_0ev_struct_sim'].apply(lambda x: x[1] if x is not None else None).median())
    print('maccs:', df['ms1_0ev_struct_sim'].apply(lambda x: x[2] if x is not None else None).median())
    print('pubchem:', df['ms1_0ev_struct_sim'].apply(lambda x: x[3] if x is not None else None).median())
    print('avalon:', df['ms1_0ev_struct_sim'].apply(lambda x: x[4] if x is not None else None).median())

    print('ms1_10ev:')
    print('morgan:', df['ms1_10ev_struct_sim'].apply(lambda x: x[0] if x is not None else None).mean())
    print('rdkit:', df['ms1_10ev_struct_sim'].apply(lambda x: x[1] if x is not None else None).mean())
    print('maccs:', df['ms1_10ev_struct_sim'].apply(lambda x: x[2] if x is not None else None).mean())
    print('pubchem:', df['ms1_10ev_struct_sim'].apply(lambda x: x[3] if x is not None else None).mean())
    print('avalon:', df['ms1_10ev_struct_sim'].apply(lambda x: x[4] if x is not None else None).mean())

    print('morgan:', df['ms1_10ev_struct_sim'].apply(lambda x: x[0] if x is not None else None).median())
    print('rdkit:', df['ms1_10ev_struct_sim'].apply(lambda x: x[1] if x is not None else None).median())
    print('maccs:', df['ms1_10ev_struct_sim'].apply(lambda x: x[2] if x is not None else None).median())
    print('pubchem:', df['ms1_10ev_struct_sim'].apply(lambda x: x[3] if x is not None else None).median())
    print('avalon:', df['ms1_10ev_struct_sim'].apply(lambda x: x[4] if x is not None else None).median())

    print('ms1_20ev:')
    print('morgan:', df['ms1_20ev_struct_sim'].apply(lambda x: x[0] if x is not None else None).mean())
    print('rdkit:', df['ms1_20ev_struct_sim'].apply(lambda x: x[1] if x is not None else None).mean())
    print('maccs:', df['ms1_20ev_struct_sim'].apply(lambda x: x[2] if x is not None else None).mean())
    print('pubchem:', df['ms1_20ev_struct_sim'].apply(lambda x: x[3] if x is not None else None).mean())
    print('avalon:', df['ms1_20ev_struct_sim'].apply(lambda x: x[4] if x is not None else None).mean())

    print('morgan:', df['ms1_20ev_struct_sim'].apply(lambda x: x[0] if x is not None else None).median())
    print('rdkit:', df['ms1_20ev_struct_sim'].apply(lambda x: x[1] if x is not None else None).median())
    print('maccs:', df['ms1_20ev_struct_sim'].apply(lambda x: x[2] if x is not None else None).median())
    print('pubchem:', df['ms1_20ev_struct_sim'].apply(lambda x: x[3] if x is not None else None).median())
    print('avalon:', df['ms1_20ev_struct_sim'].apply(lambda x: x[4] if x is not None else None).median())


import matplotlib.pyplot as plt
import seaborn as sns


def plot_density():
    # Load the data
    df = pd.read_pickle('data/aligned_feature_table_all_struct_sim.pkl')

    # Define colors
    colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95', '#ca9a96', '#facaa9']

    # Set the font to Arial
    plt.rcParams['font.family'] = 'Arial'

    # Create the plot
    fig, ax = plt.subplots(figsize=(5.2, 2.0))

    # Prepare legend labels with counts
    legend_labels = []
    medians = []
    for i, col in enumerate(['ms1_dda_struct_sim', 'ms1_0ev_struct_sim', 'ms1_10ev_struct_sim', 'ms1_20ev_struct_sim']):
        data = df[col].apply(lambda x: x[2] if x is not None else None).dropna()
        count = len(data)
        label = f'MS1 ({col.split("_")[1].upper().replace("EV", " eV")}) (n = {count})'
        # label = f'MS1 ({col.split("_")[1].upper().replace("EV", " eV")})'
        legend_labels.append(label)

        sns.kdeplot(data, fill=False, color=colors[i], ax=ax, bw_adjust=0.2)

        median = data.median()
        medians.append(median)

    # Set labels and title
    ax.set_xlabel('Structure similarity (compared to MS/MS annotations)', color='0.2', fontsize=13, labelpad=3)
    ax.set_ylabel('Density', color='0.2', fontsize=13, labelpad=4)

    # Adjust tick parameters
    ax.tick_params(axis='x', which='major', labelsize=10, colors='0.2', length=2, pad=3)
    ax.tick_params(axis='y', which='major', labelsize=10, colors='0.2', length=2, pad=3)

    # Set frame color
    for spine in ax.spines.values():
        spine.set_edgecolor('0.4')

    # Create legend inside the plot
    legend = ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(0.05, 0.95), borderaxespad=0, fontsize=10)
    legend.get_frame().set_linewidth(0.15)  # Set a thin line around the legend
    legend.get_frame().set_facecolor('none')  # Make legend background transparent

    # Change legend text color to 0.2
    for text in legend.get_texts():
        text.set_color('0.2')

    # Add median value texts
    y_positions = [8, 6.5, 5, 3.5]  # Adjust these values to position the text vertically
    for i, (median, color) in enumerate(zip(medians, colors)):
        ax.text(0.85, y_positions[i], f'Median: {median:.2f}', color=color,
                ha='center', va='center', fontsize=9.5)

    # Set x-axis limits
    ax.set_xlim(0, 1.002)

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    # save
    plt.savefig('data/structure_similarity_density.svg', transparent=True)

    # Show the plot
    plt.show()


def plot_similarity_pie_charts():
    # Load the data
    df = pd.read_pickle('data/aligned_feature_table_all_struct_sim.pkl')

    # Set the font to Arial
    plt.rcParams['font.family'] = 'Arial'

    # Create the plot
    fig, axs = plt.subplots(1, 4, figsize=(5, 2.0))

    # Define the ranges
    # colors = ['#56648a', '#6280a5', '#8ca5c0', '#8d7e95']
    # ranges = [(0, 0.5), (0.5, 0.7), (0.7, 0.95), (0.95, 1.0)]
    # range_labels = ['0.00-0.50', '0.50-0.70', '0.70-0.95', '0.95-1.00']

    colors = ['#56648a', '#6280a5', '#8d7e95']
    ranges = [(0, 0.5), (0.5, 0.7), (0.7, 1.0)]
    range_labels = ['0.00-0.50', '0.50-0.70', '0.70-1.00']

    for i, col in enumerate(['ms1_dda_struct_sim', 'ms1_0ev_struct_sim', 'ms1_10ev_struct_sim', 'ms1_20ev_struct_sim']):
        data = df[col].apply(lambda x: x[2] if x is not None else None).dropna()

        # Calculate percentages for each range
        percentages = [
            (data[(data > r[0]) & (data <= r[1])].count() / len(data)) * 100
            for r in ranges
        ]

        # Create pie chart without labels
        axs[i].pie(percentages, colors=colors, autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
                   startangle=90, textprops={'fontsize': 6.5, 'color': '0.95'})
        axs[i].set_title(f'MS1 ({col.split("_")[1].upper().replace("EV", " eV")})\nn = {len(data)}', fontsize=10)

    # Create a common legend
    fig.legend(range_labels, loc='lower center', bbox_to_anchor=(0.5, 0.1), frameon=False,
               ncol=4, fancybox=False, shadow=False, fontsize=9)

    # Adjust layout
    plt.tight_layout()

    plt.savefig('data/structure_similarity_pie_charts.svg', transparent=True)

    # Show the plot
    plt.show()


if __name__ == "__main__":
    # gen_unique_smiles_for_df()
    # #
    # main()

    print_stats()

    plot_density()
    #
    # plot_similarity_pie_charts()
