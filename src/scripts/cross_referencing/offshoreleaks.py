import pandas as pd

addresses_path = '/Users/edwardcarron/code/companies_house_interface/src/data/offshoreLeaks/nodes-addresses.csv'
entities_path = '/Users/edwardcarron/code/companies_house_interface/src/data/offshoreLeaks/nodes-entities.csv'
intermediaries_path = '/Users/edwardcarron/code/companies_house_interface/src/data/offshoreLeaks/nodes-intermediaries.csv'
officers_path = '/Users/edwardcarron/code/companies_house_interface/src/data/offshoreLeaks/nodes-officers.csv'
others_path = '/Users/edwardcarron/code/companies_house_interface/src/data/offshoreLeaks/nodes-others.csv'
relationships = '/Users/edwardcarron/code/companies_house_interface/src/data/offshoreLeaks/relationships.csv'

df = pd.read_csv(officers_path)
df

