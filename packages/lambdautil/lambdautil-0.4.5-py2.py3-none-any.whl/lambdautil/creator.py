'''
Create the skeleton for new Lambda Functions
'''
import os
import sys
import logging
import json
import time

from lambdautil.parts.simple import main_code as simple_main_code
from lambdautil.parts.simple import requirements_txt as simple_requirements_txt
from lambdautil.parts.service import main_code as service_main_code
from lambdautil.parts.service import requirements_txt as service_requirements_txt
from lambdautil.parts import docker_file
from lambdautil.cfg import LAMBDAUTIL_BUCKET
from lambdautil.cfg import LAMBDAUTIL_ROLE

DEFAULT_STAGE = 'dev'
DEFAULT_TIMEOUT = 60
DEFAULT_MEMORY = 512

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LambdaCreator:
    '''
    name - name of the new Lambda Function
    directory - target directory for the new skeleton
    service - True or False indicating a REST API
    profile - AWS credential profile
    region - AWS region
    '''
    def __init__(self, parameters):
        self.verbose = parameters.get('verbose', False)
        if self.verbose:
            logger.setLevel(logging.DEBUG)

        self.valid = True
        self.name = parameters.get('name')

        wrk = parameters.get('directory')
        if wrk is None:
            wrk = '.'

        self.directory = (f'{wrk}/{self.name}')

        self.service = parameters.get('service')
        self.profile = parameters.get('profile')
        self.region = parameters.get('region')
        self.image_packaging = parameters.get('image')

        if None in [self.name]:
            self.valid = False
            logger.error(f'LambdaCreator valid={self.valid}, bye!')
            sys.exit(1)
        else:
            self.valid = True
            logger.debug(f'LambdaCreator valid={self.valid}')

    def create(self):
        if not self.valid:
            logger.error('LambdaCreator is not valid, bye')
            sys.exit(1)

        try:
            os.makedirs(f'{self.directory}/config', exist_ok=False)
            logger.info('LambdaCreator successfully created project directory')
        except Exception as wtf:
            logger.error(wtf, exc_info=self.verbose)
            logger.error('LambdaCreator failed to make target directory tree.')
            sys.exit(1)

        try:
            with open(f'{self.directory}/main.py', 'w') as f:
                if self.service:
                    f.write(service_main_code)
                else:
                    f.write(simple_main_code)

            with open(f'{self.directory}/requirements.txt', 'w') as f:
                if self.service:
                    f.write(service_requirements_txt)
                else:
                    f.write(simple_requirements_txt)

            with open(f'{self.directory}/.lambdautil', 'w') as f:
                msg = {
                    'tool-version': '0.4.5',
                    'init-time': int(time.time())
                }
                f.write(json.dumps(msg, indent=2))

            if self.image_packaging:
                with open(f'{self.directory}/Dockerfile', 'w') as f:
                    f.write(docker_file)

            logger.info('LambdaCreator successfully created source files.')

            if self._create_config():
                logger.info('LambdaCreator successfully created config INI file.')
                return True
            else:
                sys.exit(1)
        except Exception as wtf:
            logger.error(wtf, exc_info=self.verbose)
            logger.error('LambdaCreator failed to make skeleton files.')
            sys.exit(1)

        return True

    def _create_config(self):
        try:
            role_arn = input("Enter execution role ARN (smash enter to skip): ")
            if len(role_arn) == 0 and LAMBDAUTIL_ROLE is not None:
                role_arn = LAMBDAUTIL_ROLE
                logger.info(f'using default role {LAMBDAUTIL_ROLE}')

            parts = role_arn.split(':')
            if len(parts) == 6 and role_arn.startswith('arn:aws:iam'):
                logger.debug('{role_arn} looks like an IAM role ARN')
            else:
                logger.warning('{role_arn} does not look like an ARN')
                role_arn = ' ; TODO: ADD_YOUR_LAMBDA_IAM_ROLE'

            print('\n')

            if self.image_packaging:
                bucket_name = None
                image_uri = input("Enter the image URI (smash enter to skip): ").strip()

                if len(image_uri) == 0:
                    image_uri = 'INSERT_IMAGE_URI_HERE'
                else:
                    logger.info(f'using {image_uri} as the image')
            else:
                image_uri = None
                bucket_name = input("Enter artifact bucket (smash enter to skip): ").strip()
                if len(bucket_name) == 0 and LAMBDAUTIL_BUCKET is not None:
                    bucket_name = LAMBDAUTIL_BUCKET
                    logger.info(f'using default bucket {LAMBDAUTIL_BUCKET}')

                if len(bucket_name) == 0:
                    bucket_name = ' ; TODO: ADD_YOUR_ARTIFACT_BUCKET'
                else:
                    logger.info(f'using {bucket_name} as the artifacts bucket for deployment')

            print('\n')

            with open(f'{self.directory}/config/{DEFAULT_STAGE}.ini', 'w') as f:
                f.write('[config]\n')
                f.write(f'name = {self.name}\n')
                f.write(f'stage = {DEFAULT_STAGE}\n')
                f.write(f'apig = {self.service}\n')
                f.write(f'timeout = {DEFAULT_TIMEOUT}\n')
                f.write(f'memory = {DEFAULT_MEMORY}\n')

                if self.image_packaging:
                    f.write(f'image_uri = {image_uri}\n')
                else:
                    f.write(f'bucket = {bucket_name}\n')

                f.write(f'role = {role_arn}\n\n')

                f.write('[network]\n')
                f.write('; security_group = ; TODO: ask for security_group\n')
                f.write('; subnets =        ; TODO: ask for subnets\n\n')

                f.write('[tags]\n')
                f.write(f'tool = LambdaUtil 0.4.5\n\n')

                f.write('[parameters]\n')
                f.write('ANSWER = 42')
                return True
        except Exception as wtf:
            logger.error(wtf, exc_info=self.verbose)
            logger.error('LambdaCreator failed to create config file.')
            sys.exit(1)

if __name__ == '__main__':
    lc = LambdaCreator({})
