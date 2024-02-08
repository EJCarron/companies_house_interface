import json
import sys
from . import config
import click





def check_and_init_config():
    try:
        with open("config.json", "r") as f:
            config_dict = json.load(f)
    except():
        click.echo("config json file doesn't exist. Use \'chi set_config\' command")
        sys.exit()

    if config_dict is None:
        click.echo('config file broken.')
        sys.exit()

    config_pass = True

    for key, value in config_dict.items():
        if value is None or value == '':
            click.echo('{key} is not set.')
            config_pass = False

    if config_pass:
        return config.Config(**config_dict)
    else:
        click.echo('Use set_config command to set.')
        sys.exit()


def set_config(config_dict):
    try:
        with open("config.json", "w") as f:
            json.dump(config_dict, f)
    except Exception as e:
        click.echo('failed to write config file.')
        click.echo(e)


def get_config():
    return check_and_init_config()
