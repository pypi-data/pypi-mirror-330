import pandas as pd
import os
import itertools
from typing import List, Tuple


def process_files(base_dir: str) -> pd.DataFrame:
    all_dfs = []
    for k in ['_k0', '_k3', '_k5', '_k8', '_k9', '_k10', '_k13', '_k15', '_k18']:
        folder = os.path.join(base_dir, f'output{k}')
        files = [f for f in os.listdir(folder) if not f.startswith('.') and '_0eV' in f]

        for file in files:
            df = pd.read_csv(os.path.join(folder, file), sep='\t', low_memory=False)
            df = df[~df['MS1_similarity'].isnull()].reset_index(drop=True)
            df = df[(df['MS1_similarity'] >= 0.7) & (df['MS1_matched_peak'] >= 3)].reset_index(drop=True)
            df['library'] = f'std{k}.pkl'
            all_dfs.append(df)

    return pd.concat(all_dfs, ignore_index=True)


def analyze_library_combinations(data: pd.DataFrame, max_combo: int = 3) -> List[Tuple[List[str], int]]:
    library_counts = data['library'].value_counts()
    libraries = library_counts.index.tolist()
    counts = library_counts.values

    all_combinations = []
    k0_library = 'std_k0.pkl'

    for r in range(1, max_combo + 1):
        for combo in itertools.combinations(libraries, r):
            if k0_library in combo:
                count = len(data[data['library'].isin(combo)])
                all_combinations.append((list(combo), count))

    return sorted(all_combinations, key=lambda x: x[1], reverse=True)


def main(base_dir: str):
    # Process all files
    aggregated_data = process_files(base_dir)

    # Perform combination analysis
    top_combinations = analyze_library_combinations(aggregated_data, 2)

    print(f"Total unique annotations: {len(aggregated_data)}")
    print("\nTop 5 library combinations (including k0):")
    for libs, count in top_combinations[:5]:
        print(f"Libraries: {', '.join(libs)}")
        print(f"Annotations covered: {count}")
        print(f"Coverage percentage: {count / len(aggregated_data) * 100:.2f}%")
        print()

    # Additional analysis: unique annotations per library
    unique_per_library = aggregated_data.groupby('library').apply(
        lambda x: len(x[~x.index.isin(aggregated_data[aggregated_data['library'] != x.name].index)]))
    print("Unique annotations per library:")
    print(unique_per_library)


if __name__ == '__main__':
    base_dir = '/bin/ms1id/lcms/analysis/std'
    main(base_dir)