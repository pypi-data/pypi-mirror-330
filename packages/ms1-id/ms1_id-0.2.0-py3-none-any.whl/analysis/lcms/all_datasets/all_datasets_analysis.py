import os
import pandas as pd
import pickle


def get_annotations():

    folders = os.listdir('.')
    folders = [f for f in folders if f.startswith('MSV')]

    out_dict = {} # file: [inchikeys]
    for folder in folders:
        print(folder)
        file = os.path.join(folder, 'aligned_feature_table.tsv')

        if not os.path.exists(file):
            print('File does not exist:', file)
            continue

        df = pd.read_csv(file, sep='\t', low_memory=False)
        inchikeys = list(df['MS1_inchikey'].unique())

        # remove null
        inchikeys = [i for i in inchikeys if pd.notnull(i)]
        inchikeys = [i[:14] for i in inchikeys]

        # remove duplicates
        inchikeys = list(set(inchikeys))

        print('Number of unique inchikeys:', len(inchikeys))
        out_dict[folder] = inchikeys

    # save
    pickle.dump(out_dict, open('lcms_datasets_annotations.pkl', 'wb'))



def add_class_info():
    ########################################################
    meta = pd.read_csv('/Users/shipei/Documents/projects/chemical_conjugate/main/gnps_lib/metadata_df_with_npclassifier_info.tsv', sep='\t', low_memory=False)
    # dict from inchikey to superclass
    inchikey_to_superclass = dict(zip(meta['INCHIKEY'], meta['SUPERCLASS']))
    # dict from inchikey to npsuperclass
    inchikey_to_npsuperclass = dict(zip(meta['INCHIKEY'], meta['npsuperclass']))
    # dict from inchikey to nppathway
    inchikey_to_nppathway = dict(zip(meta['INCHIKEY'], meta['nppathway']))

    # load annotations
    annotations = pickle.load(open('lcms_datasets_annotations.pkl', 'rb'))

    # create a dataframe for plotting (row: dataset, column: nppathway, counts recorded)
    out_df = pd.DataFrame(columns=['Alkaloids', 'Shikimates and Phenylpropanoids', 'Amino acids and Peptides',
                          'Fatty acids', 'Terpenoids', 'Carbohydrates', 'Polyketides', 'Others'])
    for dataset, inchikeys in annotations.items():
        print(dataset)
        row = {k: 0 for k in out_df.columns}
        for inchikey in inchikeys:
            superclass = inchikey_to_nppathway.get(inchikey, '')

            if pd.isnull(superclass):
                continue

            superclass = superclass.split(';')
            # if not a list, convert to list
            if not isinstance(superclass, list):
                superclass = [superclass]

            for s in superclass:
                if s == 'Alkaloids':
                    row['Alkaloids'] += 1
                elif s == 'Shikimates and Phenylpropanoids':
                    row['Shikimates and Phenylpropanoids'] += 1
                elif s == 'Amino acids and Peptides':
                    row['Amino acids and Peptides'] += 1
                elif s == 'Fatty acids':
                    row['Fatty acids'] += 1
                elif s == 'Terpenoids':
                    row['Terpenoids'] += 1
                elif s == 'Carbohydrates':
                    row['Carbohydrates'] += 1
                elif s == 'Polyketides':
                    row['Polyketides'] += 1
                else:
                    row['Others'] += 1
        out_df.loc[dataset] = row

    out_df.to_csv('lcms_datasets_annotations.tsv', sep='\t')


if __name__ == '__main__':
    # get_annotations()  # on server

    add_class_info()  # on local
