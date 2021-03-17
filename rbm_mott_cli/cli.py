# built in
import os
# third party
import click  # https://pypi.org/project/click/
from decouple import config  # https://pypi.org/project/python-decouple/
# this package
from mgmt_api_client.mgmt_api import ManagementApiClient
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
# RBM_MOTT -cu Matt -bu MattTV asset --assetType TV_SHOW export --metadata C:/mydir
# RBM_MOTT -cu Matt -bu MattTV asset --assetType TV_SHOW update --drm True --this-is-not-a-test



@click.group()
@click.pass_context
def cli(ctx):
    logging.debug("CLI")
    ctx.obj = {'api': ManagementApiClient(api_key_id=config('RBM_MOTT_API_KEY_ID', default=None),
                                          api_key_secret=config('RBM_MOTT_API_KEY_SECRET', default=None))}


@cli.command()
def env():
    logging.debug("ENV")
    logging.info("Listing Environment Variables...")
    logging.info('RBM_MOTT_API_KEY_ID: {0}'.format(API_KEY_ID))
    logging.info('RBM_MOTT_API_KEY_SECRET: {0}'.format(API_KEY_SECRET))
    logging.info('RBM_MOTT_CUSTOMER: {0}'.format(CUSTOMER))
    logging.info('RBM_MOTT_BUSINESS_UNIT: {0}'.format(BUSINESS_UNIT))


@cli.group()
def products():
    pass


@products.command("list")
@click.pass_context
def products_list(ctx):
    logging.info("PRODUCTS LIST")
    cu = config('RBM_MOTT_CUSTOMER', default=None)
    bu = config('RBM_MOTT_BUSINESS_UNIT', default=None)
    response = ctx.obj['api'].customer(cu).business_unit(bu).product().get_products()
    click.echo(response)


if __name__ == '__main__':
    API_KEY_ID = config('RBM_MOTT_API_KEY_ID', default=None)
    API_KEY_SECRET = config('RBM_MOTT_API_KEY_SECRET', default=None)
    CUSTOMER = config('RBM_MOTT_CUSTOMER', default=None)
    BUSINESS_UNIT = config('RBM_MOTT_BUSINESS_UNIT', default=None)
    cli()
