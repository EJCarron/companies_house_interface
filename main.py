
import src.scripts.chi_functions as chi_functions

save_directory = '/Users/edwardcarron/Desktop/chi_test'
save_json = save_directory + '/test.json'
save_xlsx = save_directory + '/test.xlsx'
influence_network_path_json_path = save_directory + '/influence_test.json'



chi_functions.add_political_influence_connections_to_network(save_json, influence_network_path_json_path)
chi_functions.loadjsoncreategraph(influence_network_path_json_path, overwrite_neo4j=True)
