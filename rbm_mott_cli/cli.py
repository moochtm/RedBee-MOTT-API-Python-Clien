# built in
import json
import logging
import os
import time
from datetime import datetime

# third party
from click_shell import shell  # https://click-shell.readthedocs.io/en/latest/index.html
import click  # https://pypi.org/project/click/
from decouple import config  # https://pypi.org/project/python-decouple/

# this package
from api_client.mott_client import MottClient
from utils.pprinting import pprint_and_color
import utils.ingest_metadata as ingest_metadata
from utils.dict_utils import Dict2Obj
from utils.logging_utils import log_function_call
import utils.excel_utils as excel_utils

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

separator_length = 60
major_separator = ''.join([char * separator_length for char in ['=']])
minor_separator = ''.join([char * separator_length for char in ['-']])


##########################################################################################
# CLI built using click
# https://click.palletsprojects.com/en/7.x/
##########################################################################################

@shell(prompt='mott > ')
@click.option('--mgmt-api-key-id', help="Management API Key ID", envvar='MGMT_API_KEY_ID', required=True)
@click.option('--mgmt-api-key-secret', help="Management API Key ID", envvar='MGMT_API_KEY_SECRET', required=True)
@click.option('--cp-api-session-auth', help="Customer Portal API Session Auth Token", envvar='CP_API_SESSION_AUTH',
              required=True)
@click.option('--debug', help="Enable debug logging", envvar='DEBUG', is_flag=True)
@click.option('--working-dir', help="Working directory for the CLI", envvar='WORKING_DIR', default='.')
@click.option('--write-log', help="Log to file in Working Dir", envvar='WRITE_LOG', is_flag=True)
@click.option('-cu', help="Name of Managed OTT Customer", required=True)
@click.option('-bu', help="Name of Managed OTT Business Unit")
@click.pass_context
def cli(ctx, mgmt_api_key_id, mgmt_api_key_secret, cp_api_session_auth, debug, working_dir, write_log, cu, bu):
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

    echo(f"Working dir for this session: {working_dir}")

    # setup logging
    # if write-log enabled, enable writing log to working dir
    if write_log:
        file_handler = logging.FileHandler(os.path.join(working_dir, 'mott_cli.log'))
        p = os.path.join(os.getcwd(), 'mott_cli.log')
        if os.path.exists(p):
            os.remove(p)
        file_handler2 = logging.FileHandler(p)
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(name)-28s : %(message)s')
        file_handler.setFormatter(formatter)
        file_handler2.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        file_handler2.setLevel(logging.INFO)
        if debug:
            file_handler.setLevel(logging.DEBUG)
            file_handler2.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(file_handler2)

    # create mgmt api client
    try:
        mott_client = MottClient(cu=cu, bu=bu, mgmt_api_key_id=mgmt_api_key_id,
                                 mgmt_api_key_secret=mgmt_api_key_secret, cp_api_session_auth=cp_api_session_auth)
    except Exception as e:
        echo(e, logging.ERROR)
        echo("Sorry. Need to quit.")
        quit()

    # create context object that gets passed between command functions
    ctx.obj = {'mott_client': mott_client,
               'working_dir': working_dir}


#########################################################################
# TESTING
#########################################################################

@cli.command()
@click.pass_context
@log_function_call
def test(ctx):
    pass


#########################################################################
# INGEST
#########################################################################

# ingest group
# option -i input file
# option -it input file type
# option excel options
# option template file
# option verbose
# option simulate
# option ignore-fails (carry on regardless) - could act at INGEST

# An INGEST BATCH is made up of one or more INGEST JOBs. A BATCH handles ingest of multiple assets. An INGEST JOB is
# made up of one or more INGEST TASKS. A JOB can handle all objects associated with an asset (tags, series,
# etc.) An INGEST TASK handles one obj / one API Post call (e.g. post tag, post asset, ...)

@cli.command("ingest")
@click.option('-i', help="Local input file for ingest", type=click.File('r', encoding='utf8'), required=True)
@click.option('-it', help="input file type", type=click.Choice(['excel', 'json'], case_sensitive=False),
              default='json', required=True)
@click.option('-xlwi', help="Excel worksheet index", type=int, default=0)
@click.option('-xlkr', help="Excel key row index", type=int, multiple=True, default=1)
@click.option('-xljsr', help="Excel jobs start row index", type=int, default=2)
@click.option('-xljer', help="Excel jobs end row index", type=int)
@click.option('-xljidc', help="Excel job id column index", type=int, default=1)
@click.option('-xljigc', help="Excel job ignore column index", type=int)
@click.option('-t', help="Local template file for ingest", type=click.File('r', encoding='utf8'))
@click.option('-u', help="Base URL to add to file locations")
@click.option('-e', help="Things to exclude from ingest, e.g. material, tag", multiple=True)
@click.option('-l', help="Default language, 2 letter code", default='en')
@click.option('-s', help="Simulation mode", default=False, is_flag=True)
@click.option('-v', help="Verbose mode", default=False, is_flag=True)
@click.pass_context
@log_function_call
def ingest(ctx, i, it, xlwi, xlkr, xljsr, xljer, xljidc, xljigc, t, u, e, l, s, v):
    # GET EXTERNAL DATA JSON TO DRIVE METADATA RENDER
    # get items json
    if it == 'excel':
        external_json = excel_utils.list_of_dicts_from_excel(excel_filepath=i.name,
                                                             worksheet_index=xlwi,
                                                             key_rows=xlkr,
                                                             first_item_row=xljsr,
                                                             ingest_job_id_column=xljidc,
                                                             ingest_job_ignore_column=xljigc)
    else:
        external_json = json.load(i)
    if not isinstance(external_json, list):
        external_json = [external_json]

    # if max number of jobs specified, trim list of job jsons
    if xljer and xljer - xljsr < len(external_json):
        external_json = external_json[:xljer - xljsr]

    # if 'ingest_job_ignore' exists in json, and is true for an item, remove that item
    for item in external_json:
        if 'ingest_job_ignore' in item and item['ingest_job_ignore'] == True:
            external_json.remove(item)

    if v:
        echo(external_json)

    # GET COMPLETE LIST OF INGEST TASKS (SUM OF ALL OBJS)
    # get template filepath
    template_fp = None
    if t:
        template_fp = t.name

    # create render input
    ctx.obj['ingest_jobs'] = [
        {
            'render_input': {
                'job_data': item,
                'base_url': u,
                'exclude': e,
                'default_language': l,
            },
        } for item in external_json
    ]

    # for each item
    # get complete ingest metadata, and save as file
    for job in ctx.obj['ingest_jobs']:
        job['render_output'] = ingest_metadata.create(job['render_input'], template_fp=template_fp)

        # save metadata to file
        ingest_metadata_fn = "ingest_xml-"
        ingest_metadata_fn += datetime.now().strftime("%Y-%m-%d-%H-%M-%S-")
        ingest_metadata_fn += job['render_input']['job_data']['ingest_job_id'] + '.xml'
        with open(os.path.join(ctx.obj['working_dir'], ingest_metadata_fn), 'w', encoding='utf8') as f:
            f.write(job['render_output'])
            echo("Saved ingest metadata: {}".format(f.name))
            f.close()

    # set up ingest job task types, with appropriate ingest API client calls
    job_ingest_task_functions = {
        'tag': ctx.obj['mott_client'].post_tags,
        'series': ctx.obj['mott_client'].post_series,
        'season': ctx.obj['mott_client'].post_seasons,
        'asset': ctx.obj['mott_client'].post_assets,
        'publicationList': ctx.obj['mott_client'].post_publications,
        'material': ctx.obj['mott_client'].post_materials
    }

    # for each job
    # break metadata down into individual ingest tasks (e.g. tags, series, assets, etc...)a
    for job in ctx.obj['ingest_jobs']:
        job['tasks'] = []
        for task_type in job_ingest_task_functions:
            # skip this task_type if it's in the exclude list
            if task_type in e:
                continue
            job['tasks'] += [
                {
                    'type': task_type,
                    'render_output': output
                }
                for output in ingest_metadata.split_ingest_metadata(
                    job['render_output'], task_type
                )
            ]

    if v:
        echo(job['tasks'])

    # get all tasks so we know the total number
    all_tasks = []
    for job in ctx.obj['ingest_jobs']:
        for task in job['tasks']:
            all_tasks.append(task)

    # DO INGEST JOBS WITH PROGRESS BAR
    # for each job, track success/fail: ingest type, ingest obj title or id, error message
    # work out number of tasks for progress bar
    label = "Processing {} ingest jobs...".format(len(ctx.obj['ingest_jobs']))
    with click.progressbar(length=len(all_tasks),
                           label=label,
                           show_percent=True,
                           show_eta=True) as progress:
        for job in ctx.obj['ingest_jobs']:
            job_continue_processing = True
            for task in job['tasks']:
                progress.update(1)
                if not job_continue_processing:
                    continue
                if not s:
                    result = job_ingest_task_functions[task['type']](data=task['render_output'])
                    if not result:
                        job_continue_processing = False

    # TODO: add tracking for job status and report at end


#########################################################################
# PRODUCTS
#########################################################################

@cli.group(chain=True)
@click.pass_context
def product(ctx):
    ctx.obj['focus'] = 'assets'


@product.command("get")
@click.pass_context
@log_function_call
def product_get(ctx):
    # API call and response
    response = ctx.obj['mott_client'].get_product()
    if response.status_code != 200:
        echo('Command Failed', logging.ERROR)
        echo(response.text)
        return

    # store only the items (the assets) in click context
    ctx.obj['products'] = response.json()

    # report what happened
    echo('Stored {} products/s in context'.format(len(ctx.obj['products'])), color='green')


@product.command("print")
@click.option('-i', help='Fields to include.', multiple=True)
@click.option('-e', help='Fields to exclude.', multiple=True)
@click.pass_context
@log_function_call
def product_print(ctx, i, e):
    click_print(ctx, i, e)


#########################################################################
# ASSETS
#########################################################################

@cli.group(chain=True)
@click.pass_context
def asset(ctx):
    ctx.obj['focus'] = 'assets'


@asset.command("get")
@click.option('-m', '--inc-materials', help="Include asset materials", type=bool)
@click.option('-t', '--tag-id', help="Tag ID with which to filter assets", multiple=True)
@click.pass_context
@log_function_call
def asset_get(ctx, inc_materials, tag_id):
    # setup params for API call
    params = {}
    if tag_id:
        params.update({'tagFilter': ','.join(tag_id)})

    # get initial response
    assets = ctx.obj['mott_client'].get_assets(params=params)

    # optionally add Material details to each asset found
    if inc_materials:
        # work out number of tasks for progress bar
        tasks = len(assets)
        label = "Getting materials for {} assets...".format(tasks)
        with click.progressbar(length=tasks,
                               label=label,
                               show_percent=True,
                               show_eta=True) as progress:
            for item in assets:
                response = ctx.obj['mott_client'].get_asset_materials(asset_id=item['id'])
                response = response.json()
                if 'materials' in response.keys():
                    item['materials'] = response['materials']
                progress.update(1)

    # store only the items (the assets) in click context
    ctx.obj['assets'] = assets
    # report what happened
    echo('Stored {} asset/s in context'.format(len(assets)), color='green')


@asset.command("print")
@click.option('-i', help='Fields to include.', multiple=True)
@click.option('-e', help='Fields to exclude.', multiple=True)
@click.pass_context
@log_function_call
def asset_print(ctx, i, e):
    click_print(ctx, i, e)


@asset.command("delete")
@click.option('-id', help="Asset ID")
@click.pass_context
@log_function_call
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
            response = ctx.obj['mott_client'].delete_asset(asset_id=asset_id)
            progress.update(1)


@asset.command("export")
@click.option('-d', help="Target folder for export")
@click.pass_context
@log_function_call
def assets_export(ctx, d):
    # check if any asset details stored.
    if 'assets' not in ctx.obj.keys():
        echo('No asset details stored in context.')
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
    echo('{} items exported. {} errors.'.format(success_count, len(error_list)), color='green')
    for err in error_list:
        echo('Could not export: {}'.format(err), color='red')


@asset.command("add")
@click.option('-t', '--tag', 'tags', help="Add Tag", multiple=True)
# @click.option('-tid', '--tag-id', 'tag_ids', help="Add Tag ID", multiple=True)
@click.option('-p', '--publication', help="Add to Publications")
@click.option('-l', help="Default language, 2 letter code", default='en')
@click.pass_context
@log_function_call
def assets_add(ctx, tags, publication, l):
    # check if any asset details stored.
    if 'assets' not in ctx.obj.keys():
        echo('No asset details stored in context.')
        return
    assets = ctx.obj['assets']

    # get jinja2 template text
    tfp = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'utils/publish_metadata_template.xml')
    with open(tfp, 'r', encoding='utf8') as t:
        template_text = t.read()
        t.close()

    # get progress bar ready
    tasks = len(assets)
    label = "Adding to {} asset/s...".format(tasks)
    with click.progressbar(length=tasks,
                           label=label,
                           show_percent=True,
                           show_eta=True) as progress:
        # do tasks
        results = Dict2Obj({
            'success': 0,
            'fail': 0,
            'fail_msgs': []
        })
        for asset in assets:
            # construct data to render
            asset = Dict2Obj(asset)
            data = Dict2Obj({})
            data.default_language = l
            data.assets = [Dict2Obj({})]
            data.assets[0].id = asset.id
            data.assets[0].type = asset.type
            if tags is not None:
                data.tags = [dict(text=t) for t in tags]
                data.assets[0].tag_list = tags

            # render metadata
            metadata = ingest_metadata.create(data, template_text=template_text)
            ingest_metadata_fn = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f-")
            ingest_metadata_fn += asset['id'] + '.xml'

            # save metadata to file
            with open(os.path.join(ctx.obj['working_dir'], ingest_metadata_fn), 'w', encoding='utf8') as f:
                f.write(metadata)
                f.close()

            # get response
            if data.assets[0].type.lower() == 'tv_show':
                response = ctx.obj['mott_client'].post_series(metadata)
            else:
                response = ctx.obj['mott_client'].post_asset(metadata)
            if response.status_code == 200:
                results.success += 1
            else:
                results.fail += 1
                results.fail_msgs.append(response.json())
            progress.update(1)
    echo(results)


#########################################################################
# TAGS
#########################################################################

@cli.group(chain=True)
@click.pass_context
def tag(ctx):
    ctx.obj['focus'] = 'tags'


@tag.command("ingest")
@click.option('-i', help="Local input file for ingest", type=click.File('r', encoding='utf8'), required=True)
@click.option('-t', help="Local template file for ingest", type=click.File('r', encoding='utf8'))
@click.option('-l', help="Default language, 2 letter code", default='en')
@click.pass_context
@log_function_call
def tags_ingest(ctx, i, t, l):
    echo("Tags Ingest")
    # create data object to render template
    ingest_json = json.load(i)
    data = {
        'tags': [ingest_json],
        'default_language': l
    }

    # create metadata
    metadata = ingest_metadata.create(data)
    ingest_metadata_fn = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-")
    ingest_metadata_fn += os.path.splitext(os.path.basename(i.name))[0] + '.xml'

    # save metadata to file
    with open(os.path.join(ctx.obj['working_dir'], ingest_metadata_fn), 'w', encoding='utf8') as f:
        f.write(metadata)
        echo("Saved ingest metadata: {}".format(f.name))

    # get response
    response = ctx.obj['mott_client'].post_tags(metadata)
    echo("Request response:")
    echo(response)


@tag.command("get")
@click.option('-id', help="Tag ID with which to filter assets")
@click.pass_context
@log_function_call
def tag_get(ctx, id):
    # setup params for API call
    params = {}

    # get initial response
    response = ctx.obj['mott_client'].get_tags(params=params)

    if response:
        # store only the items (the assets) in click context
        ctx.obj['tags'] = response
        # report what happened
        echo('Stored {} tag/s in context'.format(len(ctx.obj['tags'])), color='green')
    else:
        echo(msg='Command failed.', level=logging.ERROR, color='red')


@tag.command("export")
@click.option('-d', help="Target folder for export")
@click.option('-sf/-mf', help="Export to a single file or multiple files", is_flag=True)
@click.pass_context
@log_function_call
def tags_export(ctx, d, sf):
    # check if any asset details stored.
    if 'tags' not in ctx.obj.keys():
        echo('No tag details stored in context.')
        return
    items = ctx.obj['tags']

    # check and set target dir
    if not d:
        d = os.path.join(ctx.obj['working_dir'], 'tag_export')
    if not os.path.exists(d):
        try:
            os.makedirs(d)
        except Exception as e:
            echo("Could not create dir: {0}".format(d))
            echo(e)
            quit()

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
    echo('{} items exported. {} errors.'.format(success_count, len(error_list)), color='green')
    for err in error_list:
        echo('Could not export: {}'.format(err), color='red')


@tag.command("print")
@click.option('-i', help='Fields to include.', multiple=True)
@click.option('-e', help='Fields to exclude.', multiple=True)
@click.pass_context
@log_function_call
def tag_print(ctx, i, e):
    click_print(ctx, i, e)


@tag.command("delete")
@click.option('-item_id', help="Tag ID")
@click.pass_context
@log_function_call
def tag_delete(ctx, item_id):
    # create list of items to act on
    if id is None:
        item_ids = [item['id'] for item in ctx.obj['tags']]
        click.confirm('Delete all {} tag/s in context?'.format(len(item_ids)), abort=True)
    else:
        item_ids = [item_id]

    # get progress bar ready
    tasks = len(item_ids)
    label = "Deleting {} tag/s...".format(tasks)
    with click.progressbar(length=tasks,
                           label=label,
                           show_percent=True,
                           show_eta=True) as progress:
        # do tasks
        for item_id in item_ids:
            response = ctx.obj['mott_client'].delete_tag(tag_id=item_id)
            progress.update(1)


#########################################################################
# HELPER FUNCTIONS
#########################################################################

def click_print(ctx, i, e):
    # check if any item details stored.
    items_key = ctx.obj['focus']
    if items_key not in ctx.obj.keys():
        echo('Nothing to print. No details stored in context.')
        return

    items = ctx.obj[items_key]
    if type(items) is not list:
        items = [items]

    # if no filters then print everything
    if not i and not e:
        echo(items)
        return

    # continue if there are filters
    i = list(i)
    e = list(e)
    i.append('id')
    filtered_items = [
        {key: value for (key, value) in item.items() if key in i}
        for item in items
    ]

    echo(filtered_items)
    return


def echo(msg, level=logging.INFO, color=None):
    if color is None:
        if level is logging.ERROR:
            color = 'red'
    click.secho(pprint_and_color(msg), fg=color)
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
               'CP_API_SESSION_AUTH',
               'DEBUG',
               'WORKING_DIR',
               'WRITE_LOG'
               ]
    for var in envvars:
        if config(var, default=None) is not None:
            os.environ[var] = config(var)

    # run click application
    cli()
