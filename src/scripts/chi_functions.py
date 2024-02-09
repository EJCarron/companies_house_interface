import sys
from . import helpers
from ..Objects.network import Network
import click
from . import save_network


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


def createnetwork(officer_ids, company_numbers, layers, appointments_limit, save_json_path, save_csvs_path,
                  save_xlsx_path, save_neo4j, overwrite_neo4j):
    config = helpers.check_and_init_config()
    requests_counter = 0

    network, requests_counter = Network.start(officer_ids=officer_ids, company_numbers=company_numbers,
                                              appointments_limit=appointments_limit, requests_count=requests_counter)

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
            save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j)
        except Exception as e:
            click.echo("Failed to save neo4j graph db")
            click.echo(e)


def loadjsoncreategraph(load_path, overwrite_neo4j):
    config = helpers.check_and_init_config()

    network = load_network(load_path)

    try:
        save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j)
    except Exception as e:
        click.echo("Failed to save neo4j graph db")
        click.echo(e)


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
