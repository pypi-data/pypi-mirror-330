import time, os
from fuzzywuzzy import fuzz, process
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from tqdm import tqdm

class Netflix:
    def __init__(self, netflix_dataset: str, other_dataset: str, threshold: int = 90, force_cache: bool = False, cache_path: str = None):
        self.netflix_data = pd.read_csv(netflix_dataset)
        self.other_data = pd.read_csv(other_dataset)
        self.threshold = threshold
        self.force_cache = force_cache
        netflix_col_ren_mapping = {
                column: f'{column}_netflix' for column in self.netflix_data.columns if column!='title'
                }

        other_col_ren_mapping = {
                column: f'{column}_other' for column in self.other_data.columns if column!='title'
                }
        self.netflix_data = self.netflix_data.rename(columns=netflix_col_ren_mapping)
        self.other_data = self.other_data.rename(columns=other_col_ren_mapping)
        self.cache_path = cache_path or os.path.realpath(__file__)  # If cache_path is not provided, use a default cache location
        self.combined_data = pd.merge(self.netflix_data, self.other_data, on='title', how='inner')
        self.find_mismatches(97)

    def find_mismatches(self, similarity_score_filter):
        if self.force_cache or not os.path.exists(self.cache_path):
            self._cache_mismatches()
            self._append_cache_data(similarity_score_filter)
            self.force_cache = False
        else:
            self._append_cache_data(similarity_score_filter)

    def _cache_mismatches(self):
        merged_titles = self.combined_data['title'].unique()
        unmatched_titles = self.netflix_data[~self.netflix_data['title'].isin(merged_titles)]['title']
        other_titles = self.other_data['title'].unique()
        mismatches = []
        with tqdm(total=len(unmatched_titles)) as pbar:
            for title in unmatched_titles:
                matches = process.extractOne(title, other_titles, scorer=fuzz.ratio)
                if matches and matches[1] >= self.threshold:
                    mismatches.append((title, matches[0], matches[1]))
                pbar.update(1) # update process bar
            mismatches_df = pd.DataFrame(mismatches, columns=['Netflix Title', 'IMDb Title', 'Similarity Score'])
            mismatches_df.to_pickle(self.cache_path)

    def _append_cache_data(self, min_similarity_score):
        while not os.path.exists(self.cache_path):
            time.sleep(1)
        mismatches_df = pd.read_pickle(self.cache_path)
        mismatch_other_data = pd.merge(self.other_data, mismatches_df, left_on='title', right_on='IMDb Title', how='inner')
        mismatch_netflix_data = pd.merge(self.netflix_data, mismatches_df, left_on='title', right_on='Netflix Title', how='inner')
        mismatch_combined_data = pd.merge(mismatch_netflix_data, mismatch_other_data, left_on='title', right_on='Netflix Title', how='inner', suffixes=('_netflix', '_other'))
        mismatch_combined_data.rename(columns={'title_netflix':'title'}, inplace=True)
        mismatch_combined_data=mismatch_combined_data[mismatch_combined_data['Similarity Score_other']>=min_similarity_score]
        self.combined_data = pd.concat([self.combined_data, mismatch_combined_data], axis=0, join='inner', ignore_index=True)

    def generate_line_plots(self):
        pass

if __name__ == "__main__":
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_path = f'{project_root}/data/netflix_titles.csv'
    tmdb_path = f'{project_root}/data/TMDb_top_1000.CSV'
    cache_path = f'{project_root}/data/netflix_cache.pkl'
    
    n = Netflix(netflix_path, tmdb_path, 90, False, cache_path)
    n.combined_data.to_csv(f'{project_root}/data/combined_data.csv')
