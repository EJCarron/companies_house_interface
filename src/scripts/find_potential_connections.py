from data.political_influence_lists_params import lists
import pandas as pd


def find_potential_connections(network):
    for influence_list in lists:
        df = pd.read_csv(influence_list['path'])
        df
