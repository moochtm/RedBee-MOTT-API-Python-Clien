# built in
import json
import logging
import os
from datetime import datetime

# third party
from click_shell import shell  # https://click-shell.readthedocs.io/en/latest/index.html
import click  # https://pypi.org/project/click/
from decouple import config  # https://pypi.org/project/python-decouple/

# this package
from mgmt_api_client.mgmt_api import ManagementApiClient
from exp_api_client.exp_api import ExposureApiClient
from utils.pprinting import pprint_and_color
import utils.ingest_metadata as ingest_metadata
from request_maker import RequestMaker

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

separator_length = 60
major_separator = ''.join([char*separator_length for char in ['=']])
minor_separator = ''.join([char*separator_length for char in ['-']])

##########################################################################################
# CLI built using click
# https://click.palletsprojects.com/en/7.x/
##########################################################################################
# examples...
"""
get all assets
ASSETS -get

delete all assets
ASSETS -get -delete

delete filtered assets from *previous* GET call
ASSETS -filter ...

ingest a single object
ASSETS -ingest -t template -i input_file

batch ingest multiple objects
ASSETS -ingest -t template -i input_file -b

add a tag to asset with id
ASSETS -get -id 123 -update tags -add=123

add tags to filtered assets
ASSETS -get -filter 123 -update tags -add=[123, 456]

publish filtered assets
ASSETS -get -filter 123 -update publications 
<publication>
                <id>{{assetId}}</id>
                <startTime>2020-01-24T00:00:00.000Z</startTime>
                <endTime>2025-01-24T00:00:00.000Z</endTime>
                <publishTime>2019-12-01T00:00:00.000Z</publishTime>
                <publicationRights>
                    <productList>
                        <product>{{productId}}</product>
                    </productList>
                </publicationRights>
            </publication>

unpublish all assets
ASSETS -get -update publications -remove

find season in series and publish all episodes
SERIES FILTER --title 123
SEASON -id 123 PUBLICATIONS --dates --products ADD


EVENTS

"""


@shell(prompt='mott > ')
@click.group(chain=True) #  is replaced by @shell
@click.option('--mgmt-api-key-id', help="Management API Key ID", envvar='MGMT_API_KEY_ID', required=True)
@click.option('--mgmt-api-key-secret', help="Management API Key ID", envvar='MGMT_API_KEY_SECRET', required=True)
@click.option('--debug', help="Enable debug logging", envvar='DEBUG', is_flag=True)
@click.option('--working-dir', help="Working directory for the CLI", envvar='WORKING_DIR', default='.')
@click.option('--write-log', help="Log to file in Working Dir", envvar='WRITE_LOG', is_flag=True)
# @click.option('--sim/--no-sim', help="Simulation mode. Only executes GET calls.", is_flag=True)
@click.option('-cu', help="Name of Managed OTT Customer", required=True)
@click.option('-bu', help="Name of Managed OTT Business Unit")
@click.pass_context
def cli(ctx, mgmt_api_key_id, mgmt_api_key_secret, debug, working_dir, write_log, cu, bu):

    echo(major_separator)
    # setup working directory
    if not os.path.exists(working_dir):
        echo(f"Working Dir does not exist: {working_dir}", logging.ERROR)
        echo("Sorry. Need to quit.")
        quit()
    working_dir = os.path.join(working_dir, 'MOTT_CLI_SESSION_{0}'.format(
        datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
    try:
        os.makedirs(working_dir)
    except Exception as e:
        echo(e, logging.ERROR)
        echo("Sorry. Need to quit.")
        quit()

    echo(f"Working Dir: {working_dir}")

    # setup logging
    # if write-log enabled, enable writing log to working dir
    if write_log:
        log_path = os.path.join(working_dir, 'mott_cli.log')
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        if debug:
            file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        echo(f"Writing log file to: {log_path}")

    # create mgmt api client
    try:
        mgmt_client = ManagementApiClient(api_key_id=mgmt_api_key_id,
                                          api_key_secret=mgmt_api_key_secret,
                                          request_maker=RequestMaker(),
                                          cu=cu,
                                          bu=bu)
    except Exception as e:
        echo(e, logging.ERROR)
        echo("Sorry. Need to quit.")
        quit()

    # create context object that gets passed between command functions
    ctx.obj = {'mgmt_api_client': mgmt_client,
               'exp_api_client': ExposureApiClient(request_maker=RequestMaker(),
                                                   cu=cu,
                                                   bu=bu),
               'working_dir': working_dir}


#########################################################################
# TESTING
#########################################################################

@cli.command()
@click.pass_context
def test(ctx):
    response = ctx.obj['exp_api_client'].tag().get_tags()


#########################################################################
# OBJECTS
#########################################################################

@cli.command()
@click.pass_context
def products(ctx):
    pass


@cli.command()
@click.pass_context
def assets(ctx):
    pass


@cli.command()
@click.pass_context
def tags(ctx):
    pass


#########################################################################
# ACTIONS
#########################################################################

@cli.command()
@click.pass_context
def get(ctx):
    pass


@cli.command()
@click.option('-i', help='Fields to include.', multiple=True)
@click.option('-e', help='Fields to exclude.', multiple=True)
@click.pass_context
def print(ctx, i, e):
    pass


@cli.command()
@click.option('-i', help="Local input file for ingest", type=click.File('r', encoding='utf8'), required=True)
@click.option('-t', help="Local template file for ingest", type=click.File('r', encoding='utf8'), required=True)
@click.option('-u', help="Base URL to add to file locations")
@click.pass_context
def ingest(ctx, i, t, u):
    pass


@cli.command()
@click.pass_context
def delete(ctx):
    pass


@cli.command()
@click.option('-d', help="Target folder for export")
@click.pass_context
def export(ctx, d):
    pass


#########################################################################
# HELPER FUNCTIONS
#########################################################################

def echo(msg, level=logging.INFO):
    click.echo(pprint_and_color(msg))
    logger.log(level, msg)


def check_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError


#########################################################################
# MAIN
#########################################################################

if __name__ == '__main__':
    # load vars from .env file to environment variables for click option defaults
    env_vars = ['MGMT_API_KEY_ID',
               'MGMT_API_KEY_SECRET',
               'DEBUG',
               'WORKING_DIR',
               'WRITE_LOG'
                ]
    for var in env_vars:
        if config(var, default=None) is not None:
            os.environ[var] = config(var)

    # run click application
    cli()
