import logging

import click

from sagecreator.configurator import Configurator
from sagecreator.provisioner import Provisioner

logging.basicConfig(level=logging.INFO, format='%(name)-12s: %(levelname)-8s: %(message)s')
log = logging.getLogger(__name__)

configurator = Configurator()


@click.group()
def cli():
    pass


def valid_instance_type(ctx, param, value):
    # valid_types = configurator.get_valid_instance_types()
    # if value not in valid_types:
    #     raise click.BadParameter("Invalid instance type {}. Should be one of {}".format(value, str(valid_types)))
    return value


@cli.command(help="Configure infrastructure settings")
@click.option('--access_key_id', prompt=True, required=True)
@click.option('--secret_access_key', prompt=True, required=True, hide_input=True, confirmation_prompt=True)
@click.option('--company', prompt=True, required=True, help="Company name")
@click.option('--owner', prompt=True, required=True, help="Owner / Team that owns the service")
@click.option('--key_pair_name', prompt='Key pair name (optional, if not provided it will be created with a new private key)', default='',
              help="Provide existing key pair name")
def configure(access_key_id, secret_access_key, company, owner, key_pair_name):
    try:
        private_key_file = None
        if key_pair_name:
            private_key_file = click.prompt("Private key file (required because Key pair name was provided)", default='')
            if not private_key_file:
                raise click.BadParameter("Private key file has to be provided because Key pair name was provided")
        configurator.persist(access_key_id, secret_access_key, company, owner, private_key_file, key_pair_name)
    except Exception as e:
        log.error("Failed to store configuration. {}".format(str(e)))


@cli.command(help="Provision instances")
@click.option('--service', prompt=True, required=True, help="Name of the service")
@click.option('--instance_type', prompt=True, default="t3.small", help="AWS instance type (default t3.small)", callback=valid_instance_type)
@click.option('--spot_price', prompt='Spot instance price', default=0.1, help="Price of the spot instance (default $0.1)")
@click.option('--cluster_size', prompt=True, default=1, type=int, help="Size of the cluster (default 1)")
def provision(service, instance_type, spot_price, cluster_size):
    try:
        click.echo("Provisioning cluster based on {}".format(configurator.get_config_path()))
        prov = Provisioner(configurator)
        prov.provision(service, instance_type, spot_price, cluster_size)
    except Exception as e:
        log.error("Failed to provision instance(s). {}".format(str(e)))


@cli.command(help="Terminate instance(s)")
@click.option('--service', prompt=True, required=True, help="Name of the service")
@click.confirmation_option(prompt='Are you sure you want to terminate the cluster?')
def terminate(service):
    prov = Provisioner(configurator)
    prov.terminate(service)


@cli.command(help="Full path to configuration file")
def pwd():
    click.echo(configurator.get_config_path())


if __name__ == "__main__":
    cli()
