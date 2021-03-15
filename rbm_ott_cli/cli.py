# built in
import os
# third party
import click  # https://pypi.org/project/click/
from decouple import config  # https://pypi.org/project/python-decouple/
# logging
import logging
logging.basicConfig(level=logging.INFO)


##########################################################################################
# CLI built using click
# https://click.palletsprojects.com/en/7.x/
##########################################################################################
# examples...
# RMB_MOTT
# RBM_MOTT env set -i ... -s ... -cu Matt -bu MattTV >> sets environment variables
# RBM_MOTT env >> gets and prints environment variables
# RBM_MOTT asset new -vf hello.mp4 -md "medium description" -ts "horror, 2010, musical"
# RBM_MOTT asset new -vf hello.mp4 -md "medium description" -ts "horror, 2010, musical"


@click.group()
def cli():
    logging.debug("CLI")


@cli.command()
def env():
    logging.debug("ENV")
    logging.info("Listing Environment Variables...")
    logging.info('API_KEY_ID: {0}'.format(API_KEY_ID))
    logging.info('API_KEY_SECRET: {0}'.format(API_KEY_SECRET))
    logging.info('CUSTOMER: {0}'.format(CUSTOMER))
    logging.info('BUSINESS_UNIT: {0}'.format(BUSINESS_UNIT))


if __name__ == '__main__':
    API_KEY_ID = config('RBM_MOTT_API_KEY_ID', default='')
    API_KEY_SECRET = config('RBM_MOTT_API_KEY_SECRET', default='')
    CUSTOMER = config('RBM_MOTT_CUSTOMER', default='')
    BUSINESS_UNIT = config('RBM_MOTT_API_BUSINESS_UNIT', default='')
    cli()
