import os
import pandas as pd

def merge_data():
    project_root = os.environ.get('PROJECT_ROOT')
    netflix_path = f'{project_root}/data/netflix_titles.csv'
    tmdb_path = f'{project_root}/data/TMDb_updated.CSV'
    netflix_data = pd.read_csv(netflix_path)
    tmdb_data = pd.read_csv(tmdb_path)
    
    # Get column names from tmdb_data and prefix them with '_imdb'
    column_rename_mapping = {
        column: f'{column}_imdb' for column in tmdb_data.columns if column!='title'
    }
    
    # Rename columns in tmdb_data using the dynamically generated dictionary
    tmdb_data = tmdb_data.rename(columns=column_rename_mapping)
    
    # Merge the datasets
    merged_data = pd.merge(netflix_data, tmdb_data, on='title')
    print(merged_data.head())

merge_data()

