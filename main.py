import src.scripts.chi_functions as chi_functions

save_directory = '/Users/edwardcarron/Desktop/chi_test'
save_json = save_directory + '/test.json'
save_xlsx = save_directory + '/test.xlsx'
influence_network_path_json_path = save_directory + '/influence_test.json'

chi_functions.createnetwork(officer_ids=['f938yKbeBI1hfS51o9XyXUICCoM'
    , 'zXXCsFZE1SdB9XfTe9JEZ5Ye4Uc'
    , 'hVtfIH-BD0S3LP4UGaHgBFy0qv0'
    , 'xoEfkSUt7wAiToQj6HH5ZrG_GzQ'
    , 'OZf0xc_l-mU8A42IXdwGTOf2CTg'
    , '3w1cbDkNi2t0P7qEk6se88xRGj0'
    , 'd5VSX49JvOAKy-SuoITPFOv3t0g'
    , 'UmubCTUFXwFJ5IMNTZdKT7oW5ss'
    , 'wDJMaTgYIoIXM3F09k64L07Ik0M'], company_numbers=['11694875', '13277309', '13007844'], overwrite_neo4j=True, save_json_path=save_json)
# chi_functions.find_potential_political_influence_connections(load_path=save_json)

# chi_functions.add_political_influence_connections_to_network(save_json, influence_network_path_json_path)
chi_functions.loadjsoncreategraph(save_json, overwrite_neo4j=True)
