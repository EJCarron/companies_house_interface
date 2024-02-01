import click


@click.group()
def chi():
    pass


@chi.command()
def testes():
    click.echo("testes")
