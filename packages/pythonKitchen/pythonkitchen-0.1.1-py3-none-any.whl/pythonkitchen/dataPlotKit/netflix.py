import time, os
from fuzzywuzzy import fuzz, process
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from tqdm import tqdm

class Netflix:
    def __init__(self, netflix_dataset: str, tmdb_dataset: str, tmdb_top_1000: str, threshold: int = 90, force_cache: bool = False, cache_path: str = None):
        self.netflix_dataset: pd.DataFrame = pd.read_csv(netflix_dataset)
        self.tmdb_dataset:pd.DataFrame = pd.read_csv(tmdb_dataset)
        self.tmdb_top_1000:pd.DataFrame = pd.read_csv(tmdb_top_1000)
        self.threshold = threshold
        self.force_cache = force_cache
        netflix_col_ren_mapping = {
                column: f'{column}_netflix' for column in self.netflix_dataset.columns if column != 'title'
                }
        tmdb_col_ren_mapping = {
                column: 'title' if column == 'names' else f'{column}_tmdb' 
                for column in self.tmdb_dataset.columns
                }
        tmdb_top_1000_mapping = {
                column: f'{column}_top_1000' for column in self.tmdb_top_1000.columns if column != 'title'
                }
        self.netflix_dataset = self.netflix_dataset.rename(columns=netflix_col_ren_mapping)
        self.tmdb_dataset = self.tmdb_dataset.rename(columns=tmdb_col_ren_mapping)
        self.tmdb_top_1000 = self.tmdb_top_1000.rename(columns=tmdb_top_1000_mapping)
        self.tmdb_dataset_combined = self._merge_datasets(self.tmdb_dataset, self.tmdb_top_1000, on='title', similarity_score=90)
        self.tmdb_dataset_combined.to_csv(f'{os.environ.get('PROJECT_ROOT')}/data/fuzzy_matched_merged_titles.csv')
               
    def _merge_datasets(self, left_dataset, right_dataset, on: str = 'title', similarity_score: int = 90):
        inner_join_dataset = pd.merge(left_dataset, right_dataset, on=on, how='inner')
        inner_join_dataset = inner_join_dataset.drop_duplicates(subset=on, keep='first')
        left_mismatches_titles = left_dataset[~left_dataset[on].isin(inner_join_dataset[on].unique())][on]
        right_mismatches_titles = right_dataset[~right_dataset[on].isin(inner_join_dataset[on].unique())][on]
        fuzzy_matched_titles = self._fuzzy_find_mismatches(left_mismatches_titles, right_mismatches_titles, on, similarity_score)
        
        # Merge fuzzy matched titles with the main inner join dataframe
        fuzzy_matched_titles = pd.merge(fuzzy_matched_titles, left_dataset, left_on='left_title', right_on=on, how='inner')
        fuzzy_matched_titles = pd.merge(fuzzy_matched_titles, right_dataset, left_on='right_title', right_on=on, how='inner', suffixes=('_x', '_y'))
        fuzzy_matched_titles = fuzzy_matched_titles.drop_duplicates(subset='left_title', keep='first')
        fuzzy_matched_titles.drop(columns=['left_title', 'right_title', 'similarity_score', f'{on}_y'], inplace=True)
        fuzzy_matched_titles.rename(columns={f'{on}_x':on}, inplace=True)
        inner_join_dataset = pd.concat([inner_join_dataset, fuzzy_matched_titles], ignore_index=True)
        return inner_join_dataset



    def _fuzzy_find_mismatches(self, left_dataset_titles, right_dataset_titles, inner_join_dataset_titles, on: str = 'title', similarity_score: int = 90):
        fuzzy_matched_titles = []
        for left_title in left_dataset_titles:
            for right_title in right_dataset_titles:
                ratio = fuzz.ratio(left_title, right_title)
                if ratio>=similarity_score:
                    fuzzy_matched_titles.append({'left_title':left_title, 'right_title': right_title, 'similarity_score':ratio})
        return pd.DataFrame(fuzzy_matched_titles)




def main():
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_dataset = f'{project_root}/data/netflix_titles.csv'
    tmdb_dataset = f'{project_root}/data/imdb_movies.csv'
    tmdb_top_1000 = f'{project_root}/data/TMDb_top_1000.CSV'
    n = Netflix(netflix_dataset, tmdb_dataset, tmdb_top_1000, 90, False)

if __name__=='__main__':
    main()


