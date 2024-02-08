
from src.Objects.network import Network
from src.scripts import find_potential_connections
from thefuzz import fuzz

# name1 = 'Aviva Employment Services Ltd'
# name2 = 'AVIVA PLC'

name1 = 'Aviva Employment Services'
name2 = 'AVIVA'

score1 = fuzz.ratio(name1, name2)
score2 = fuzz.partial_ratio(name1, name2)
score3 = fuzz.token_sort_ratio(name1, name2)
score4 = fuzz.token_set_ratio(name1, name2)





save_directory = '/Users/edwardcarron/Desktop/chi_test'
save_json = save_directory + '/test.json'
save_xlsx = save_directory + '/test.xlsx'





network = Network.load_json(save_json)


find_potential_connections.find_potential_connections(network)
