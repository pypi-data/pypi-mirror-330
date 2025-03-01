'''
The command line interface to Lambda Utility
'''
# pylint: disable=line-too-long
import sys
import json
import logging

import click

from lambdautil.creator import LambdaCreator
from lambdautil.deployer import LambdaDeployer

logging.basicConfig(
    level=logging.WARNING,
    stream=sys.stdout,
    format='[%(levelname)s] %(asctime)s (%(module)s) %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fresh_notes = '''A skeleton of the new lambda, {}, has been created.

In {}/{}/config you will find a config.ini file that you should
fill in with parameters for your own account.

Develop the lambda function as needed then you can deploy it with:
lambdatool deploy. The lambda has been started in main.py.
'''


@click.group()
@click.version_option(version='0.4.5')
def cli():
    '''
    The command line interface to Lambda Utility
    '''


@cli.command()
@click.option('-n', '--name', help='name of the new lambda skeleton', required=True)
@click.option('-d', '--directory', help='target directory for new Lambda, defaults to current directory')
@click.option('-s', '--service', help='create a flask like micro-service', is_flag=True)
@click.option('-v', '--verbose', help='turn the logging knob to \'leven', is_flag=True)
@click.option('-i', '--image', help='the new lambda will be packaged in a Docker image', is_flag=True)
def new(**kwargs):
    '''
    Make a new lambda skeleton
    '''
    if kwargs.get('verbose'):
        logger.setLevel(logging.DEBUG)

    logger.debug('kwargs: %s', json.dumps(kwargs, indent=2))
    lc = LambdaCreator(kwargs)

    if lc.create():
        logger.info('Lambda skeleton was successfully created')
        sys.exit(0)
    else:
        logger.error('Lambda skeleton creation did not go well')
        sys.exit(1)


@cli.command()
@click.option('-d', '--directory', help='scratch directory for deploy, defaults to /tmp')
@click.option('-f', '--config-file', help='config file that describes the deployment', required=True)
@click.option('-p', '--profile', help='AWS CLI profile to use in the deployment, more details at http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html')
@click.option('-r', '--region', help='target region, defaults to your credentials default region')
@click.option('-v', '--verbose', help='turn the logging knob to \'leven', is_flag=True)
@click.option('-e', '--environment', help='key/value pair for function env variable', multiple=True)
def deploy(**kwargs):
    '''
    Deploy a Lambda function
    '''
    if kwargs.get('verbose'):
        logger.setLevel(logging.DEBUG)

    logger.debug('kwargs: %s', json.dumps(kwargs, indent=2))
    ld = LambdaDeployer(kwargs)
    if ld.deploy():
        sys.exit(0)
    else:
        sys.exit(1)
