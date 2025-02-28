import pandas as pd
import os


def merge_results():

    all_results = pd.DataFrame()

    # Walk through the directory
    for root, dirs, files in os.walk('/imaging/MTBLS313'):
        for file in files:
            # Check if the file ends with .tsv
            if file.endswith('_all.tsv'):
                # Construct the full file path
                full_path = os.path.join(root, file)

                # get its parent directory
                parent_dir = os.path.basename(os.path.dirname(full_path))

                # Read the file
                try:
                    result_df = pd.read_csv(full_path, sep='\t', low_memory=False)
                    result_df['sample'] = parent_dir
                except:
                    continue

                all_results = pd.concat([all_results, result_df])

    all_results.to_csv('all_brain_annotations.tsv', sep='\t', index=False)


if __name__ == '__main__':
    merge_results()

