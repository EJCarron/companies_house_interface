from . import helpers
from ..Objects.network import Network
import click
from neo4j import GraphDatabase


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
    config_dict = {'normal_key': normal_key,
                   'uri': uri,
                   'username': username,
                   'pw': pw
                   }

    helpers.set_config(config_dict)


@chi.command()
@click.option("--officer_ids", "-oid", multiple=True,
              prompt="the Companies House ID of the person that you want to find the "
                     "network of.",
              help="Can be found in the url of the person\'s Companies House profile.")
@click.option("--layers", prompt="The number of times you want to expand the network outwards", default=1,
              help="Warning networks can quickly become extremely large, not recommended to exceed 2 to 3 layers.")
@click.option("--appointments_limit", default=100,
              prompt="The limit for the number of appointments the program will pull. If the number exceeds the limit "
                     "the officer will still be pulled but without it\' related companies and appointments.",
              help="If no limit wanted set to -1. NOT ADVISED some officers can have extremely large number of "
                   "appointments. "
              )
def creategraph(officer_ids, layers, appointments_limit):
    config = helpers.check_and_init_config()

    requests_counter = 0

    network, requests_counter = Network.start(officer_ids=officer_ids,
                                              requests_count=requests_counter,
                                              appointments_limit=appointments_limit)

    network.expand_network(requests_count=requests_counter, layers=layers, appointments_limit=appointments_limit)
    create_cypher = network.render_create_cypher()

    graphDB_Driver = GraphDatabase.driver(config.uri, auth=(config.username, config.pw))

    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run(create_cypher)


@chi.command()
@click.option("--path", "-p", prompt="path to the save location.")
@click.option("--officer_ids", "-oid", multiple=True,
              prompt="the Companies House ID of the person that you want to find the "
                     "network of.",
              help="Can be found in the url of the person\'s Companies House profile.", default=[''])
@click.option("--layers", prompt="The number of times you want to expand the network outwards", default=1,
              help="Warning networks can quickly become extremely large, not recommended to exceed 2 to 3 layers.")
@click.option("--appointments_limit", default=100,
              prompt="The limit for the number of appointments the program will pull. If the number exceeds the limit "
                     "the officer will still be pulled but without it\' related companies and appointments.",
              help="If no limit wanted set to -1. NOT ADVISED some officers can have extremely large number of "
                   "appointments. "
              )
def savejson(officer_ids, layers, appointments_limit, path):
    helpers.check_and_init_config()
    requests_counter = 0

    network, requests_counter = Network.start(officer_ids=officer_ids,
                                              requests_count=requests_counter,
                                              appointments_limit=appointments_limit)

    network.expand_network(requests_count=requests_counter, layers=layers, appointments_limit=appointments_limit)

    network.save_json(path=path)


@chi.command()
@click.option("--path", "-p", prompt="path to the save location.")
def loadjsoncreategraph(path):
    config = helpers.check_and_init_config()
    network = Network.load_json(path)

    cypher = network.render_create_cypher()

    graphDB_Driver = GraphDatabase.driver(config.uri, auth=(config.username, config.pw))

    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run(cypher)


@chi.command()
@click.option("--officer_ids", "-oid", multiple=True,
              prompt="the Companies House ID of the person that you want to find the "
                     "network of.",
              help="Can be found in the url of the person\'s Companies House profile.", default=[''])
@click.option("--layers", prompt="The number of times you want to expand the network outwards", default=1,
              help="Warning networks can quickly become extremely large, not recommended to exceed 2 to 3 layers.")
@click.option("--appointments_limit", default=100,
              prompt="The limit for the number of appointments the program will pull. If the number exceeds the limit "
                     "the officer will still be pulled but without it\' related companies and appointments.",
              help="If no limit wanted set to -1. NOT ADVISED some officers can have extremely large number of "
                   "appointments. "
              )
@click.option("--path", "-p", prompt="path to the save directory (it must already exist).")
def savecsvs(officer_ids, layers, appointments_limit, path):
    helpers.check_and_init_config()
    requests_counter = 0

    network, requests_counter = Network.start(officer_ids=officer_ids,
                                              requests_count=requests_counter,
                                              appointments_limit=appointments_limit)

    network.expand_network(requests_count=requests_counter, layers=layers, appointments_limit=appointments_limit)

    network.save_csvs(directory_path=path)


@chi.command()
@click.option("--officer_ids", "-oid", multiple=True,
              prompt="the Companies House ID of the person that you want to find the "
                     "network of.",
              help="Can be found in the url of the person\'s Companies House profile.", default=[''])
@click.option("--layers", prompt="The number of times you want to expand the network outwards", default=1,
              help="Warning networks can quickly become extremely large, not recommended to exceed 2 to 3 layers.")
@click.option("--appointments_limit", default=100,
              prompt="The limit for the number of appointments the program will pull. If the number exceeds the limit "
                     "the officer will still be pulled but without it\' related companies and appointments.",
              help="If no limit wanted set to -1. NOT ADVISED some officers can have extremely large number of "
                   "appointments. "
              )
@click.option("--path", "-p", prompt="path to the save location.", help="must have name of new file (or existing file"
              " that you want to overwrite) with .xlsx at end. For example /Users/johndoe/Desktop/SugarNetwork.xlsx")
def savexlsx(officer_ids, layers, appointments_limit, path):
    requests_counter = 0

    network, requests_counter = Network.start(officer_ids=officer_ids,
                                              requests_count=requests_counter,
                                              appointments_limit=appointments_limit)

    network.expand_network(requests_count=requests_counter, layers=layers, appointments_limit=appointments_limit)

    network.save_xlsx(path=path)
