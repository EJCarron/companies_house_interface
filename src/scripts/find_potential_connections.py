from data.political_influence_lists.political_influence_lists_params import lists
import pandas as pd
from thefuzz import fuzz

strip_strings = ['plc', 'ltd', 'limited', 'llp']


def find_potential_connections(network, fuzz_threshold=70):
    def clean_str_for_fuzz(dirty_str):
        for stripper in strip_strings:
            dirty_str = dirty_str.lower().replace(stripper, '')
        return dirty_str

    clean_officers = {officer_id: clean_str_for_fuzz(network.officers[officer_id].name) for officer_id in
                      network.officers.keys()}
    clean_companies = {company_number: clean_str_for_fuzz(network.companies[company_number].company_name) for
                       company_number in network.companies.keys()}

    for influence_list in lists:
        def determine_fuzz(str1, str2):
            return fuzz.token_set_ratio(str1, str2)

        def find_closest_officer(row):
            print(row.name)
            closest_officer = {'fuzz': 0,
                               'id': '',
                               'name': ''
                               }

            potential_name = clean_str_for_fuzz(row[influence_list['reference_col']])

            for officer_id, name in clean_officers.items():
                fuzz_score = determine_fuzz(potential_name, name)

                if fuzz_score > closest_officer['fuzz']:
                    closest_officer = {'fuzz': fuzz_score, 'id': officer_id, 'name': network.officers[officer_id].name}

            row['fuzz'] = closest_officer['fuzz']
            row['potential_officer_id'] = closest_officer['id']
            row['potential_officer_name'] = closest_officer['name']

            return row

        def find_closest_company(row):
            print(row.name)
            closest_company = {'fuzz': 0,
                               'id': '',
                               'name': ''
                               }

            potential_name = clean_str_for_fuzz(row[influence_list['reference_col']])

            for company_number, name in clean_companies.items():

                fuzz_score = fuzz.token_set_ratio(potential_name, name)

                if fuzz_score > closest_company['fuzz']:
                    closest_company = {'fuzz': fuzz_score, 'id': company_number, 'name':
                        network.companies[company_number].company_name}

            row['fuzz'] = closest_company['fuzz']
            row['potential_company_id'] = closest_company['id']
            row['potential_company_name'] = closest_company['name']

            return row

        def make_potential_connections_df(raw_df, apply_function):
            pc_df = raw_df.apply(apply_function, axis=1)
            pc_df = pc_df.loc[pc_df['fuzz'] > fuzz_threshold].sort_values(
                by=['fuzz'], ascending=False)

            return pc_df

        df = pd.read_csv(influence_list['path'])

        df = df.dropna(subset=[influence_list['reference_col']])

        company_df = make_potential_connections_df(df, find_closest_company)
        officer_df = make_potential_connections_df(df, find_closest_officer)

        officer_df.to_csv(influence_list['potential_officer_path'], index=False)
        company_df.to_csv(influence_list['potential_company_path'], index=False)
