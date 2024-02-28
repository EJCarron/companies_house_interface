import src.scripts.chi_functions as chi_functions

save_directory = '/Users/edwardcarron/Desktop/chi_test'
save_json = save_directory + '/test.json'
save_xlsx = save_directory + '/test.xlsx'
influence_network_path_json_path = save_directory + '/influence_test.json'

connections_directory = save_directory + '/connections'


tice_ids =['f938yKbeBI1hfS51o9XyXUICCoM'
    , 'zXXCsFZE1SdB9XfTe9JEZ5Ye4Uc'
    , 'hVtfIH-BD0S3LP4UGaHgBFy0qv0'
    , 'xoEfkSUt7wAiToQj6HH5ZrG_GzQ'
    , 'OZf0xc_l-mU8A42IXdwGTOf2CTg'
    , '3w1cbDkNi2t0P7qEk6se88xRGj0'
    , 'd5VSX49JvOAKy-SuoITPFOv3t0g'
    , 'UmubCTUFXwFJ5IMNTZdKT7oW5ss'
    , 'wDJMaTgYIoIXM3F09k64L07Ik0M']

fox_ids = ['wWDVkC37wVABGMpHJ02ynYkhm2A', 'xwtkOFUUyiVQEBqC0f_nnQMIJxo']

lawson_ids = ['kJ55R2Al6e3XIbnQ7M4dXuSk7ow', 'Mvbul_En-TpPAmrbZowNYm_fP-I', 'Qsn7yIpJn-39QSleMXMGmOOlNw0']

farage_ids = ['tW56blTqOI_bXYCDkDghRy3LQtU']

bull_ids = ['ibw6rQom9RhVmQoj7yrAFYfrCIA', 'j1IdRKmRvRoz_ACgt_9lcVPxpoE']

hosking_ids = ['K4iN0E72aLPCaM_J-zeNG5OwJbc', 'ENGtXaf6LzkXXE8wU7EspcB9jYw', 'RgzRFcsZFUMFuyN_3IYyuKRLc74',
               'LHPkdrbeaLpru4nZrvbz2lSzEyc', 'rnGvAlS7h4P64m8F7RB9Sz04SMo']

oids = hosking_ids + bull_ids + farage_ids + lawson_ids + fox_ids + tice_ids


chi_functions.createnetwork(company_numbers=['00499482'], overwrite_neo4j=True, layers=1, appointments_limit=133)

# chi_functions.createnetwork(officer_ids=oids, company_numbers=['11694875', '13277309', '13007844', '09135232',
#                                                                '06962749'],
#                             overwrite_neo4j=True, save_json_path=save_json)
#
# chi_functions.create_officer_group(load_path=save_json, group_name='Richard Tice', officer_ids=tice_ids)
# chi_functions.create_officer_group(load_path=save_json, group_name='Lawrence Fox', officer_ids=fox_ids)
# chi_functions.create_officer_group(load_path=save_json, group_name='Nigel Lawson', officer_ids=lawson_ids)
# chi_functions.create_officer_group(load_path=save_json, group_name='David Bull', officer_ids=bull_ids)
# chi_functions.create_officer_group(load_path=save_json, group_name='Jeremy Hosking', officer_ids=hosking_ids)
#
#
# chi_functions.find_potential_political_influence_connections(load_path=save_json,
#                                                              connections_directory=connections_directory)

# chi_functions.add_political_influence_connections_to_network(save_json, influence_network_path_json_path,
#                                                              connections_directory=connections_directory)

# chi_functions.loadjsoncreategraph(influence_network_path_json_path, overwrite_neo4j=True, group_officers=True)
