# built in
import os, json
# third party
import click  # https://pypi.org/project/click/
from decouple import config  # https://pypi.org/project/python-decouple/
# this package
from mgmt_api_client.mgmt_api import ManagementApiClient
from exp_api_client.exp_api import ExposureApiClient
from request_maker import RequestMaker
# logging
import logging

logging.basicConfig(level=logging.INFO)


##########################################################################################
# CLI built using click
# https://click.palletsprojects.com/en/7.x/
##########################################################################################
# examples...
# RBM_MOTT env >> gets and prints environment variables
# RBM_MOTT asset new -vf hello.mp4 -md "medium description" -ts "horror, 2010, musical"
# RBM_MOTT asset new -vf hello.mp4 -md "medium description" -ts "horror, 2010, musical"
# RBM_MOTT -cu Matt -bu MattTV products list - DONE!
# RBM_MOTT -cu Matt -bu MattTV assets list - DONE!
# RBM_MOTT -cu Matt -bu MattTV assets list --assetType TV_SHOW export --metadata --dir C:/mydir
# RBM_MOTT -cu Matt -bu MattTV assets list --assetType TV_SHOW update --drm True --this-is-not-a-test


@click.group()
@click.option('-cu', help="Name of Managed OTT Customer", required=True)
@click.option('-bu', help="Name of Managed OTT Business Unit")
@click.pass_context
def cli(ctx, cu, bu):
    logging.debug("CLI")
    ctx.obj = {'cu': cu,
               'bu': bu,
               'mgmt_api_client': ManagementApiClient(api_key_id=config('RBM_MOTT_API_KEY_ID', default=None),
                                                      api_key_secret=config('RBM_MOTT_API_KEY_SECRET', default=None),
                                                      request_maker=RequestMaker()),
               'exp_api_client': ExposureApiClient(request_maker=RequestMaker()),
               'selection': []}


@cli.command()
def env():
    logging.debug("ENV")
    logging.info("Listing Environment Variables...")
    logging.info('RBM_MOTT_API_KEY_ID: {0}'.format(API_KEY_ID))
    logging.info('RBM_MOTT_API_KEY_SECRET: {0}'.format(API_KEY_SECRET))


@cli.group(chain=True, invoke_without_command=True)
def assets():
    pass


@assets.command("list")
@click.pass_context
# TODO: add parameter options
def assets_list(ctx):
    logging.info("ASSETS LIST")
    if ctx.obj['bu'] is None:
        pass
        # response = ctx.obj['exp_api_client'].customer(ctx.obj['cu']).asset().get_assets()
    else:
        response = ctx.obj['exp_api_client'].customer(ctx.obj['cu']).business_unit(ctx.obj['bu']).asset().get_assets()
    ctx.obj['selection'] = response
    click.echo(ctx.obj['selection'])


@assets.command("export")
@click.option('-md', help="Export metadata")
# @click.option('-i', help="Export images")
@click.option('-d', help="Target folder for export")
@click.pass_context
# TODO: add parameter options
def assets_export(ctx, md, d):
    logging.info("ASSETS EXPORT")

    # check and set target dir
    if d:
        if not os.path.exists(d):
            try:
                os.mkdirs(d)
            except:
                click.echo("Could not create dir: {0}".format(d))
    else:
        d = ""

    for item in ctx.obj['selection']:
        click.echo("Exporting Asset: {0}".format(item['assetId']))
        export_path = os.path.join(d, "{0}.{1}".format(item['assetId'], 'json'))
        with open(export_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(item, indent=4, ensure_ascii=False))
            f.close()


@cli.group()
def products():
    pass


@products.command("list")
@click.pass_context
def products_list(ctx):
    logging.info("PRODUCTS LIST")
    if ctx.obj['bu'] is None:
        response = ctx.obj['mgmt_api_client'].customer(ctx.obj['cu']).product().get_products()
    else:
        response = ctx.obj['mgmt_api_client'].customer(ctx.obj['cu']).business_unit(
            ctx.obj['bu']).product().get_products()
    click.echo(response)


if __name__ == '__main__':
    API_KEY_ID = config('RBM_MOTT_API_KEY_ID', default=None)
    API_KEY_SECRET = config('RBM_MOTT_API_KEY_SECRET', default=None)
    CUSTOMER = config('RBM_MOTT_CUSTOMER', default=None)
    BUSINESS_UNIT = config('RBM_MOTT_BUSINESS_UNIT', default=None)
    cli()
