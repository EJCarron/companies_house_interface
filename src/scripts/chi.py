import sys
from . import helpers
from ..Objects.network import Network
import click
from . import save_network


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


@chi.command()
@click.option("--load_path", "-lp", prompt="path to the save location.")
def loadjsoncreategraph(load_path, overwrite_neo4j):
    config = helpers.check_and_init_config()

    network = helpers.load_network(load_path)

    try:
        save_network.save_neo4j(network=network, config=config, overwrite_neo4j=overwrite_neo4j)
    except Exception as e:
        click.echo("Failed to save neo4j graph db")
        click.echo(e)


@chi.command()
@click.option("--save_path", "-sp", prompt="path to the save location.")
@click.option("--load_path", "-lp", prompt="path to the saved json location.")
def loadjsonsavecsvs(load_path, save_path):
    network = helpers.load_network(load_path)

    try:
        save_network.save_csvs(network=network, path=save_path)
    except Exception as e:
        click.echo("failed to save csvs. REMINDER to save csvs provide path to existing directory not to a .csv "
                   "file")
        click.echo(e)


@chi.command()
@click.option("--save_path", "-sp", prompt="path to the save location.")
@click.option("--load_path", "-lp", prompt="path to the saved json location.")
def loadjsonsavexlsx(load_path, save_path):
    network = helpers.load_network(load_path)

    try:
        save_network.save_xlsx(network=network, path=save_path)
    except Exception as e:
        click.echo("failed to save xlsx")
        click.echo(e)

