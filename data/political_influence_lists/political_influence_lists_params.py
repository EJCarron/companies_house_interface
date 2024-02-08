import os

root = os.path.dirname(os.path.abspath(__file__))

donations = {'path': root + '/donations.csv',
             'potential_connections_path': root + '/donations_potential_connections.csv',
             'reference_col': 'Donor',
             'potential_officer_path': root + '/potential_officer_connections.csv',
             'potential_company_path': root + '/potential_company_connections.csv'
             }

lists = [donations]
