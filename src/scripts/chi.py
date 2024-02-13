from . import chi_functions
import click


@click.group()
def chi():
    pass


@chi.command()
@click.option("--normal_key", "-nk", prompt='Your Companies House api Key',
              help="You need to make an account with Companies House to have a key.")
@click.option("--uri", "-uri", prompt='Your neo4j DB uri')
@click.option("--username", "-un", prompt="Your neo4j username", default='neo4j')
@click.option("--pw", "-pw", prompt="Your neo4j db password")
def setconfig(normal_key, uri, username, pw):
    chi_functions.setconfig(normal_key=normal_key, uri=uri, username=username, pw=pw)


@chi.command()
@click.option("--officer_ids", "-oid", multiple=True, default=[], required=False,
              help="Can be found in the url of the person\'s Companies House profile.")
@click.option("--company_numbers", "-cn", multiple=True, default=[], required=False,
              help="Can be found in the url of the company\'s Companies House profile.")
@click.option("--layers", "-l", default=1,
              help="Warning networks can quickly become extremely large, not recommended to exceed 2 to 3 layers.")
@click.option("--appointments_limit", "-al", default=100,
              help="If no limit wanted set to -1. NOT ADVISED some officers can have extremely large number of "
                   "appointments. "
              )
@click.option("--save_json_path", "-sjp", default="",
              help="Path to the json save location, will not save if left blank")
@click.option("--save_csvs_path", "-scp", default="", help="Path to the directory where you want to save your csvs,"
                                                           "directory must already exist. Will not save if left blank")
@click.option("--save_xlsx_path", "-sxp", default="",
              help="Path to the xlsx save location, will not save if left blank")
@click.option("--save_neo4j", "-sgdb", default=True, help="Bool for for whether to save the network as a graph DB."
                                                          "Defaults to True.")
@click.option("--overwrite_neo4j", "-own", default=False, help="Bool, set to True if you want to clear graph db "
                                                               "contents before writing new network")
def createnetwork(officer_ids, company_numbers, layers, appointments_limit, save_json_path, save_csvs_path,
                  save_xlsx_path, save_neo4j, overwrite_neo4j):
    chi_functions.createnetwork(officer_ids=officer_ids, company_numbers=company_numbers, layers=layers,
                                appointments_limit=appointments_limit, save_json_path=save_json_path,
                                save_csvs_path=save_csvs_path, save_xlsx_path=save_xlsx_path, save_neo4j=save_neo4j,
                                overwrite_neo4j=overwrite_neo4j)


@chi.command()
@click.option("--load_path", "-lp", prompt="path to the save location.")
def loadjsoncreategraph(load_path, overwrite_neo4j):
    chi_functions.loadjsoncreategraph(load_path=load_path, overwrite_neo4j=overwrite_neo4j)


@chi.command()
@click.option("--save_path", "-sp", prompt="path to the save location.")
@click.option("--load_path", "-lp", prompt="path to the saved json location.")
def loadjsonsavecsvs(load_path, save_path):
    chi_functions.loadjsonsavecsvs(load_path=load_path, save_path=save_path)


@chi.command()
@click.option("--save_path", "-sp", prompt="path to the save location.")
@click.option("--load_path", "-lp", prompt="path to the saved json location.")
def loadjsonsavexlsx(load_path, save_path):
    chi_functions.loadjsonsavexlsx(load_path=load_path, save_path=save_path)


@chi.command()
@click.option("--load_path", "-lp", prompt="path to the saved json location.")
@click.option("--connections_directory_path", "-cdp", prompt='path to directory where connections data will be stored')
def fppc(load_path, connections_directory_path):
    chi_functions.find_potential_political_influence_connections(load_path=load_path,
                                                                 connections_directory=connections_directory_path)


@chi.command()
@click.option("--load_path", "-lp", prompt="path to the saved json location.")
@click.option("--updated_network_save_path", "-unsp", prompt='save path to the json file of your new network with '
                                                             'political connections added.')
@click.option("--connections_directory_path", "-cdp", prompt='path to directory where connections data will be stored')
def apctn(load_path, updated_network_save_path, connections_directory_path):
    chi_functions.add_political_influence_connections_to_network(load_path=load_path,
                                                                 updated_network_save_path=updated_network_save_path,
                                                                 connections_directory=connections_directory_path)
