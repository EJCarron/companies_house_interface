from src.data.political_influence_lists.political_influence_lists_params import lists
import pandas as pd
from thefuzz import fuzz
import sys

strip_strings = ['plc', 'ltd', 'limited', 'llp']


def find_potential_connections(network, connections_directory, fuzz_threshold=80):
    def clean_str_for_fuzz(dirty_str):
        for stripper in strip_strings:
            dirty_str = dirty_str.lower().replace(stripper, '')
        return dirty_str

    def make_dict_of_fuzz_clean_nodes(nodes):
        cleaned = {}
        for node in nodes:
            cleaned[node.node_id] = clean_str_for_fuzz(node.name)
        return cleaned

    clean_officers = make_dict_of_fuzz_clean_nodes(network.officers.values())
    clean_companies = make_dict_of_fuzz_clean_nodes(network.companies.values())

    for influence_list in lists:
        def determine_fuzz(str1, str2):
            return fuzz.token_set_ratio(str1, str2)

        def find_closest(row, clean_nodes, main_nodes_dict):
            print(row.name)
            closest_node = {'fuzz': 0,
                            'id': '',
                            'name': ''
                            }

            potential_name = clean_str_for_fuzz(row[influence_list['reference_col']])

            for node_id, name in clean_nodes.items():
                fuzz_score = determine_fuzz(potential_name, name)

                if fuzz_score > closest_node['fuzz']:
                    closest_node = {'fuzz': fuzz_score, 'id': node_id, 'name': main_nodes_dict[node_id].name}

            row['fuzz'] = closest_node['fuzz']
            row['connection_id'] = closest_node['id']
            row['connection_name'] = closest_node['name']

            return row

        def make_potential_connections_df(raw_df, find_officers=False, find_companies=False):

            if find_officers:
                pc_df = raw_df.apply(find_closest, clean_nodes=clean_officers, main_nodes_dict=network.officers,
                                     axis=1)
            elif find_companies:
                pc_df = raw_df.apply(find_closest, clean_nodes=clean_companies, main_nodes_dict=network.companies,
                                     axis=1)
            else:
                print('Internal error, improper use of function. No potential node selected')
                sys.exit()

            pc_df = pc_df.loc[pc_df['fuzz'] > fuzz_threshold].sort_values(
                by=['fuzz'], ascending=False)

            return pc_df

        df = pd.read_csv(influence_list['path'])

        df = df.dropna(subset=[influence_list['reference_col']])

        company_df = make_potential_connections_df(df, find_companies=True)
        officer_df = make_potential_connections_df(df, find_officers=True)

        potential_officer_path = connections_directory + influence_list['potential_officer_path']
        potential_company_path = connections_directory + influence_list['potential_company_path']

        print('Saving potential connections at')
        print(potential_officer_path)
        print(potential_company_path)
        officer_df.to_csv(potential_officer_path, index=False)
        company_df.to_csv(potential_company_path, index=False)
