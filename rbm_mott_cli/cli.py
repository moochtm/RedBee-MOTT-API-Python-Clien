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
formatter = logging.Formatter(
    '%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
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
# RBM_MOTT env >> gets and prints environment variables - DONE!
# RBM_MOTT -cu Matt -bu MattTV products list - DONE!
# RBM_MOTT -cu Matt -bu MattTV assets list - DONE!
# RBM_MOTT -cu Matt -bu MattTV asset new -v hello.mp4 -md "medium description" -ts "horror, 2010, musical"
# RBM_MOTT -cu Matt -bu MattTV asset new -v hello.mp4 -md "medium description" -ts "horror, 2010, musical"
# RBM_MOTT -cu Matt -bu MattTV assets list --assetType TV_SHOW export --metadata --dir C:/mydir
# RBM_MOTT -cu Matt -bu MattTV assets list --assetType TV_SHOW update --drm True --this-is-not-a-test


@shell(prompt='mott > ')
# @click.group() is replaced by @shell
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
# PRODUCTS
#########################################################################

@cli.group(chain=True)
def product():
    pass


@product.command("get")
@click.pass_context
def product_get(ctx):
    # get initial response
    response = ctx.obj['mgmt_api_client'].get_product()

    # report what happened
    click.echo('Got {} products/s. Stored in context'.format(len(response)))
    # store only the items (the assets) in click context
    ctx.obj['products'] = response


@product.command("print")
@click.option('-i', help='Fields to include.', multiple=True)
@click.option('-e', help='Fields to exclude.', multiple=True)
@click.pass_context
def product_print(ctx, i, e):
    # check if any details stored.
    if 'products' not in ctx.obj.keys():
        echo('Nothing to print. No details stored.')
        return
    items = ctx.obj['products']
    if type(items) is not list:
        items = [items]

    # if no filters then print everything
    if not i and not e:
        echo(items)
        return

    # continue if there are filters
    i = list(i)
    e = list(e)
    filtered_items = []
    i.append('id')
    for item in items:
        filtered_items.append({key: value for (key, value) in item.items() if key in i})
    echo(filtered_items)
    return


#########################################################################
# ASSETS
#########################################################################

@cli.group(chain=True)
def asset():
    pass


@asset.command("ingest")
@click.option('-i', help="Local input file for ingest", type=click.File('r', encoding='utf8'), required=True)
@click.option('-t', help="Local template file for ingest", type=click.File('r', encoding='utf8'), required=True)
@click.option('-u', help="Base URL to add to file locations")
@click.option('-e', help="Things to exclude from injest, e.g. material, tag", multiple=True)
@click.option('-l', help="Default language, 2 letter code", default='en')
@click.pass_context
def assets_ingest(ctx, i, t, u, e, l):
    echo("Assets Ingest")
    # create data object to render template
    asset_json = json.load(i)
    data = {
        'base_url': u,
        'asset': asset_json,
        'exclude': e,
        'default_language': l
    }

    # create metadata
    metadata = ingest_metadata.create(data, template_file=t)
    ingest_metadata_fn = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-")
    ingest_metadata_fn += os.path.splitext(os.path.basename(i.name))[0] + '.xml'

    # save metadata to file
    with open(os.path.join(ctx.obj['working_dir'], ingest_metadata_fn), 'w', encoding='utf8') as f:
        f.write(metadata)
        echo("Saved ingest metadata: {}".format(f.name))
        f.close()

    # get response
    response = ctx.obj['mgmt_api_client'].post_asset(metadata)
    echo("Request response:")
    echo(response)


@asset.command("get")
@click.option('-m', '--inc-materials', help="Include asset materials", type=bool)
@click.option('-t', '--tag-id', help="Tag ID with which to filter assets", multiple=True)
@click.pass_context
def asset_get(ctx, inc_materials, tag_id):
    # setup params for API call
    params = {}
    if tag_id:
        params.update({'tagFilter': ','.join(tag_id)})

    # get initial response
    response = ctx.obj['mgmt_api_client'].get_assets(params=params)

    # getting ALL items in case of multiple pages
    response_buffer = response
    tasks = int(response['totalCount'] / response['pageSize']) - 1
    label = "Getting {} assets...".format(response['totalCount'])
    with click.progressbar(length=tasks,
                           label=label,
                           show_percent=True,
                           show_eta=True) as progress:
        while response['pageNumber'] * response['pageSize'] < response['totalCount']:
            progress.update(1)
            if 'pageNumber' not in params.keys():
                params.update({'pageNumber': 1})
            params['pageNumber'] = params['pageNumber'] + 1
            response = ctx.obj['mgmt_api_client'].get_assets(params=params)
            response_buffer['items'].extend(response['items'])
            response_buffer['pageSize'] = response_buffer['pageSize'] + response['pageSize']

    response_buffer = response_buffer['items']

    # optionally add Material details to each asset found
    if inc_materials:
        # work out number of tasks for progress bar
        tasks = len(response_buffer)

        label = "Getting materials for {} assets...".format(tasks)
        with click.progressbar(length=tasks,
                               label=label,
                               show_percent=True,
                               show_eta=True) as progress:
            for item in response_buffer:
                response = ctx.obj['mgmt_api_client'].get_asset_materials(asset_id=item['id'])
                if 'materials' in response.keys():
                    item['materials'] = response['materials']
                progress.update(1)

    # report what happened
    echo('Stored {} asset/s in context'.format(len(response_buffer)))
    # store only the items (the assets) in click context
    ctx.obj['assets'] = response_buffer


@asset.command("print")
@click.option('-i', help='Fields to include.', multiple=True)
@click.option('-e', help='Fields to exclude.', multiple=True)
@click.pass_context
def asset_print(ctx, i, e):
    # check if any asset details stored.
    if 'assets' not in ctx.obj.keys():
        echo('Nothing to print. No asset details stored.')
        return

    assets = ctx.obj['assets']
    if type(assets) is not list:
        assets = [assets]

    # if no filters then print everything
    if not i and not e:
        echo(assets)
        return

    # continue if there are filters
    i = list(i)
    e = list(e)
    filtered_assets = []
    i.append('id')
    for asset in assets:
        filtered_assets.append({key: value for (key, value) in asset.items() if key in i})
    echo(filtered_assets)
    return


@asset.command("delete")
@click.option('-id', help="Asset ID")
@click.pass_context
def asset_delete(ctx, id):
    # create list of asset_ids
    if id is None:
        asset_ids = [asset['id'] for asset in ctx.obj['assets']]
        click.confirm('Delete all {} asset/s in context?'.format(len(asset_ids)), abort=True)
    else:
        asset_ids = [id]

    # get progress bar ready
    tasks = len(asset_ids)
    label = "Deleting {} asset/s...".format(tasks)
    with click.progressbar(length=tasks,
                           label=label,
                           show_percent=True,
                           show_eta=True) as progress:
        # do tasks
        for asset_id in asset_ids:
            response = ctx.obj['mgmt_api_client'].delete_asset(asset_id=asset_id)
            progress.update(1)


@asset.command("export")
@click.option('-d', help="Target folder for export")
@click.pass_context
def assets_export(ctx, d):
    # check if any asset details stored.
    if 'assets' not in ctx.obj.keys():
        echo('Nothing to export. No asset details stored in context.')
        return
    items = ctx.obj['assets']

    # check and set target dir
    if d:
        if not os.path.exists(d):
            try:
                os.makedirs(d)
            except Exception as e:
                echo("Could not create dir: {0}".format(d))
                echo(e)
                quit()
    else:
        d = ""

    # if just a single item, put it in a list
    if type(items) is not list:
        items = [items]

    error_list = []
    for item in items:
        export_path = os.path.join(d, "{0}.{1}".format(item['id'], 'json'))
        try:
            with open(export_path, 'w', encoding='utf8') as f:
                f.write(json.dumps(item, indent=4, ensure_ascii=False))
                f.close()
        except:
            error_list.append(item['id'])
            continue
    success_count = len(items) - len(error_list)
    echo('{} items exported. {} errors.'.format(success_count, len(error_list)))
    for err in error_list:
        echo('Could not export: {}'.format(err))




#########################################################################
# TAGS
#########################################################################


@cli.group(chain=True)
def tag():
    pass


@tag.command("get")
@click.pass_context
def tag_list(ctx):
    pass


@tag.command("print")
@click.pass_context
def tag_list(ctx):
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
    envvars = ['MGMT_API_KEY_ID',
               'MGMT_API_KEY_SECRET',
               'DEBUG',
               'WORKING_DIR',
               'WRITE_LOG'
               ]
    for var in envvars:
        if config(var, default=None) is not None:
            os.environ[var] = config(var)

    # run click application
    cli()
