import sys
from . import helpers
from ..Objects.network import Network
import click
from . import save_network
from ..scripts.cross_referencing.find_potential_connections import find_potential_connections
from ..scripts.cross_referencing.add_connections_to_network import add_connections_to_network


def load_network(load_path):
    try:
        network = Network.load_json(load_path)
    except Exception as e:
        click.echo('Failed to load network')
        click.echo(e)
        sys.exit()

    return network


def setconfig(normal_key, uri, username, pw):
    config_dict = {'normal_key': normal_key,
                   'uri': uri,
                   'username': username,
                   'pw': pw
                   }

    helpers.set_config(config_dict)


def createnetwork(officer_ids=None, company_numbers=None, layers=0, appointments_limit=100, save_json_path='',
                  save_csvs_path='',
                  save_xlsx_path='', save_neo4j='', overwrite_neo4j=False):

    officer_ids = [] if officer_ids is None else officer_ids
    company_numbers = [] if company_numbers is None else company_numbers

    config = helpers.check_and_init_config()
    requests_counter = 0

    network, requests_counter = Network.start(officer_ids=officer_ids, company_numbers=company_numbers,
                                              appointments_limit=appointments_limit, requests_count=requests_counter)

    if layers > 0:
        network.expand_network(requests_count=requests_counter, layers=layers, appointments_limit=appointments_limit)

    if save_json_path != "":
        try:
            save_network.save_json(network=network, path=save_json_path)
        except Exception as e:
            click.echo("failed to save json")
            click.echo(e)

    if save_csvs_path != "":
        try:
            save_network.save_csvs(network=network, path=save_csvs_path)
        except Exception as e:
            click.echo("failed to save csvs. REMINDER to save csvs provide path to existing directory not to a .csv "
                       "file")
            click.echo(e)

    if save_xlsx_path != "":
        try:
            save_network.save_xlsx(network=network, path=save_xlsx_path)
        except Exception as e:
            click.echo("failed to save xlsx")
            click.echo(e)

    if save_neo4j:
        try:
            save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j, group_officers=False)
        except Exception as e:
            click.echo("Failed to save neo4j graph db")
            click.echo(e)


def loadjsoncreategraph(load_path, overwrite_neo4j, group_officers=True):
    config = helpers.check_and_init_config()

    network = load_network(load_path)

    save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j,
                            group_officers=group_officers)


    # try:
    #     save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j,
    #                             group_officers=group_officers)
    # except Exception as e:
    #     click.echo("Failed to save neo4j graph db")
    #     click.echo(e)


def loadjsonsavecsvs(load_path, save_path):
    network = load_network(load_path)

    try:
        save_network.save_csvs(network=network, path=save_path)
    except Exception as e:
        click.echo("failed to save csvs. REMINDER to save csvs provide path to existing directory not to a .csv "
                   "file")
        click.echo(e)


def loadjsonsavexlsx(load_path, save_path):
    network = load_network(load_path)

    try:
        save_network.save_xlsx(network=network, path=save_path)
    except Exception as e:
        click.echo("failed to save xlsx")
        click.echo(e)


def find_potential_political_influence_connections(load_path, connections_directory):
    network = Network.load_json(load_path)
    find_potential_connections(network, connections_directory)
    print('check potential connections, keep ones that you think match, and save file in same directory but remove'
          ' \'potential\' from file name')


def add_political_influence_connections_to_network(load_path, updated_network_save_path, connections_directory):
    network = Network.load_json(load_path)
    add_connections_to_network(network, connections_directory)
    print('Saving updated network to ' + updated_network_save_path)
    network.save_json(updated_network_save_path)


def create_officer_group(load_path, officer_ids, group_name, save_path=''):
    print('Grouping nodes for ' + group_name)

    network = Network.load_json(load_path)

    network.group_officers(officer_ids, group_name=group_name)

    if save_path == '':
        network.save_json(load_path)
    else:
        network.save_json(save_path)
