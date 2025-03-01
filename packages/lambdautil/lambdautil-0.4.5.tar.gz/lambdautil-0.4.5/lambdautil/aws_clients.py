import sys
import logging

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_api_client(profile, region, aws_service, verbose):
    try:
        if verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        if profile and region:
            api_session = boto3.session.Session(profile_name=profile,
                                                region_name=region)
        elif profile:
            api_session = boto3.session.Session(profile_name=profile)
        elif region:
            api_session = boto3.session.Session(region_name=region)
        else:
            api_session = boto3.session.Session()

        api_client = api_session.client(aws_service)

        return api_client
    except Exception as x:
        logger.error(f'exception caught in get_api_client() [{x}]')
        sys.exit(1)
