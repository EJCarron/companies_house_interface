import os

root = os.path.dirname(os.path.abspath(__file__))

donations = {'path': root + '/donations.csv',
             'potential_connections_path': root + '/donations_potential_connections.csv',
             'reference_col': 'Donor',
             'potential_officer_path': root + '/donations_potential_officer_connections.csv',
             'potential_company_path': root + '/donations_potential_company_connections.csv',
             'officer_connections_path': root + '/donations_officer_connections',
             'company_connections_path': root + '/donations_company_connections'
             }

lists = [donations]
