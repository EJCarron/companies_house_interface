from . import helpers
from ..Objects.network import Network
import click
from neo4j import GraphDatabase
from .helpers import check_and_init_config
from .config import config


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
