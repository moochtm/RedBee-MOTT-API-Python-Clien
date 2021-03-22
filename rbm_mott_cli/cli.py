# built in
import os, json, time
# third party
import click  # https://pypi.org/project/click/
from decouple import config  # https://pypi.org/project/python-decouple/
from click_shell import shell  # https://click-shell.readthedocs.io/en/latest/index.html
# this package
from mgmt_api_client.mgmt_api import ManagementApiClient
from exp_api_client.exp_api import ExposureApiClient
from request_maker import RequestMaker
from helpers import pprint_json_obj, pprint_and_color_json_obj
# logging
import logging

logging.basicConfig(level=logging.INFO)

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


@shell(prompt='mott > ', intro='Starting RMB MOTT API client...')
# @click.group() is replaced by @shell
@click.option('-cu', help="Name of Managed OTT Customer", required=True)
@click.option('-bu', help="Name of Managed OTT Business Unit")
@click.pass_context
def cli(ctx, cu, bu):
    logging.debug("CLI")
    try:
        mgmt_client = ManagementApiClient(api_key_id=config('RBM_MOTT_API_KEY_ID', default=None),
                                          api_key_secret=config('RBM_MOTT_API_KEY_SECRET', default=None),
                                          request_maker=RequestMaker(),
                                          cu=cu,
                                          bu=bu)
    except Exception as e:
        click.echo(e)
        click.echo("Quitting due to error.")
        quit()

    ctx.obj = {'mgmt_api_client': ManagementApiClient(api_key_id=config('RBM_MOTT_API_KEY_ID', default=None),
                                                      api_key_secret=config('RBM_MOTT_API_KEY_SECRET', default=None),
                                                      request_maker=RequestMaker(),
                                                      cu=cu,
                                                      bu=bu),
               'exp_api_client': ExposureApiClient(request_maker=RequestMaker(),
                                                   cu=cu,
                                                   bu=bu)}


@cli.command()
def env():
    logging.debug("ENV")
    logging.info("Listing Environment Variables...")
    click.echo('RBM_MOTT_API_KEY_ID: {0}'.format(API_KEY_ID))
    click.echo('RBM_MOTT_API_KEY_SECRET: {0}'.format(API_KEY_SECRET))


@cli.group(chain=True)
def products():
    pass


@products.command("get")
@click.pass_context
def products_get(ctx):
    # get initial response
    response = ctx.obj['mgmt_api_client'].get_product()

    # report what happened
    click.echo('Got {} products/s'.format(len(response)))
    # store only the items (the assets) in click context
    ctx.obj['products'] = response


@products.command("print")
@click.option('-i', help='Fields to include.', multiple=True)
@click.option('-e', help='Fields to exclude.', multiple=True)
@click.pass_context
def products_print(ctx, i, e):
    # check if any details stored.
    if 'products' not in ctx.obj.keys():
        click.echo('Nothing to print. No details stored.')
        return
    items = ctx.obj['products']
    if type(items) is not list:
        items = [items]

    # if no filters then print everything
    if not i and not e:
        click.echo(pprint_and_color_json_obj(items))
        return

    # continue if there are filters
    i = list(i)
    e = list(e)
    filtered_items = []
    i.append('id')
    for item in items:
        filtered_items.append({key: value for (key, value) in item.items() if key in i})
    click.echo(pprint_and_color_json_obj(filtered_items))
    return


@cli.group(chain=True)
def assets():
    pass


@assets.command("get")
@click.option('-m', '--inc-materials', help="Include asset materials", type=bool)
@click.option('-t', '--tag-id', help="Tag ID with which to filter assets", multiple=True)
@click.pass_context
def assets_get(ctx, inc_materials, tag_id):
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

    inc_materials = True
    if inc_materials:
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
    click.echo('Got {} asset/s'.format(len(response_buffer)))
    # store only the items (the assets) in click context
    ctx.obj['assets'] = response_buffer


@assets.command("print")
@click.option('-i', help='Fields to include.', multiple=True)
@click.option('-e', help='Fields to exclude.', multiple=True)
@click.pass_context
def assets_print(ctx, i, e):
    # check if any asset details stored.
    if 'assets' not in ctx.obj.keys():
        click.echo('Nothing to print. No asset details stored.')
        return
    assets = ctx.obj['assets']
    if type(assets) is not list:
        assets = [assets]

    # if no filters then print everything
    if not i and not e:
        click.echo(pprint_and_color_json_obj(assets))
        return

    # continue if there are filters
    i = list(i)
    e = list(e)
    filtered_assets = []
    i.append('id')
    for asset in assets:
        filtered_assets.append({key: value for (key, value) in asset.items() if key in i})
    click.echo(pprint_and_color_json_obj(filtered_assets))
    return


@assets.command("new")
@click.pass_context
def assets_new(ctx):
    logging.info("ASSETS NEW")

    data = {
        'data': {
            'asset': {
                'id': '1231231231',
                'titleList': {
                    'title': [
                        {'@language': 'en', '$': 'Title Text'}
                    ]
                },
                'assetType': 'movie'
            },
            'material': {
                'materialRef': [{
                    '$': 'https://emptestdata.blob.core.windows.net/sources/Sintel/sintel.mp4'
                }]
            }
        }
    }
    response = ctx.obj['mgmt_api_client'].ingest().post_asset(data)
    click.echo(response)


@assets.command("export")
@click.option('-d', help="Target folder for export")
@click.pass_context
def assets_export(ctx, d):
    # check if any asset details stored.
    if 'assets' not in ctx.obj.keys():
        click.echo('Nothing to export. No asset details stored.')
        return
    items = ctx.obj['assets']

    # check and set target dir
    if d:
        if not os.path.exists(d):
            try:
                os.makedirs(d)
            except Exception as e:
                click.echo("Could not create dir: {0}".format(d))
                click.echo(e)
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
                f.write(pprint_json_obj(item))
                f.close()
        except:
            error_list.append(item['id'])
            continue
    success_count = len(items) - len(error_list)
    click.echo('{} items exported. {} errors.'.format(success_count, len(error_list)))
    for err in error_list:
        click.echo('Could not export: {}'.format(err))






@cli.group()
def configuration():
    pass


@configuration.command("list")
@click.pass_context
# TODO: add parameter options
def config_list(ctx):
    logging.info("CONFIG LIST")
    response = ctx.obj['mgmt_api_client'].config().list()


@cli.group()
def system():
    pass


@system.command("config")
@click.pass_context
def system_config(ctx):
    logging.info("SYSTEM CONFIG")
    ctx.obj['system_config'] = ctx.obj['exp_api_client'].system().system_config()


@cli.group()
def tag():
    pass


@tag.command("list")
@click.pass_context
def tag_list(ctx):
    logging.info("LIST TAGS")
    click.echo(ctx.obj['exp_api_client'].tag().get_tags())


if __name__ == '__main__':
    API_KEY_ID = config('RBM_MOTT_API_KEY_ID', default=None)
    API_KEY_SECRET = config('RBM_MOTT_API_KEY_SECRET', default=None)
    cli()
