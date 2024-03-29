import click
import os
from cloudflareupdateip.application.runner import CloudflareUpdater
import subprocess

@click.group(chain=True, help="get current assoicated IP")
def gp_current():
    pass


@click.group(chain=True, help="update records IP address")
def gp_update():
    pass


@click.group(chain=True, help="setup the environment variables")
def gp_setup():
    pass


@gp_setup.command(help="setup the environment variables")
@click.option('--domain', default=None, help="the domain you wish to manage")
@click.option('--token', default=None, help="a valid CF api token")
def setup(domain, token):
    if domain is None:
        domain = click.prompt('Please enter a domain', type=str)
    os.environ['CURRENT_DOMAIN'] = domain

    if token is None:
        token = click.prompt('Please enter a valid cloudflare api token', type=str)
    os.environ['CF_TOKEN'] = token


@gp_current.command(help="get the current IP address")
def current():
    domain = os.getenv('CURRENT_DOMAIN')
    if domain is None:
        click.echo("Error: CURRENT_DOMAIN is not set")
        return
    runner = CloudflareUpdater()
    click.echo("The current IP for the A record of " + domain + " is: " + runner.get_cloudflare_current_ip())

@gp_update.command(help="update the IP address")
def update():
    domain = os.getenv('CURRENT_DOMAIN')
    if domain is None:
        click.echo("Error: CURRENT_DOMAIN is not set")
        return
    runner = CloudflareUpdater()
    runner.update(runner.get_local_ip())


cli = click.CommandCollection(sources=[gp_setup, gp_current, gp_update])

if __name__ == '__main__':
    cli()
