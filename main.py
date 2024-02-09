from src.Objects.network import Network
from src.scripts.cross_referencing.find_potential_connections import find_potential_connections
from src.scripts.cross_referencing.add_connections_to_network import add_connections_to_network

save_directory = '/Users/edwardcarron/Desktop/chi_test'
save_json = save_directory + '/test.json'
save_xlsx = save_directory + '/test.xlsx'

network = Network.load_json(save_json)

# find_potential_connections(network)
add_connections_to_network(network)
network
