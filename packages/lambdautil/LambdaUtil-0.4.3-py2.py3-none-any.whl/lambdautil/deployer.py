'''
Deploy a Lambda Function
'''
import os
import sys
import logging
import uuid
import shutil
import zipfile
import json
import copy
import time

import boto3

from lambdautil.config_parser import CaseSensitiveConfigParser
from lambdautil.cfg import LAMBDAUTIL_TMP
from lambdautil.aws_clients import get_api_client
from lambdautil.template import starter
from lambdautil.template import lambda_schedule
from lambdautil.template import trusted_service
from lambdautil.template import the_api
from lambdautil.template import the_deployment
from lambdautil.template import the_outputs
from lambdautil.template import white_list
from lambdautil.utility import date_converter
from lambdautil.stack import StackUtility 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TOOL_FILE = '.lambdautil'
IGNORED_STUFF = ('config', '.git', 'requirements.txt', TOOL_FILE)
TMP_DIR = os.environ.get('LAMBDAUTIL_TMP', '/tmp')
IMPORT_HEADER = '[import:'
SSM_HEADER = '[ssm:'

VALID_ENDPOINT_CONFIG = [
    'REGIONAL',
    'EDGE',
    'PRIVATE'
]

class LambdaDeployer:
    def __init__(self, parameters):
        '''
        arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:{self.account}:function:baz-svc-dev/invocations
        '''
        try:
            self.ssm_client = None
            self.verbose = parameters.get('verbose', False)
            if self.verbose:
                logger.setLevel(logging.DEBUG)
            else:
                logger.setLevel(logging.INFO)

            if not os.path.isfile(TOOL_FILE):
                logger.error('your lambda function is not in the current directory')
                sys.exit(1)

            self.deployment_id = str(uuid.uuid4())[24:]
            self.config_file = parameters.get('config_file')
            if self.config_file is not None and os.path.isfile(self.config_file):
                logger.info(f'{self.config_file} exists')
            else:
                logger.error(f'can not grok {self.config_file} as a config file')
                sys.exit(1)

            tmp = parameters.get('directory')
            wrk = tmp if tmp is not None else LAMBDAUTIL_TMP
            if wrk is not None and os.path.isdir(wrk):
                self.directory = f'{wrk}/lambdautil/{self.deployment_id}'
                logger.info(f'scratch directory is {self.directory}')
            else:
                logger.error(f'can not grok {wrk} as a base directory')
                sys.exit(1)

            self.package_file = f'{wrk}/lambdautil/{self.deployment_id}.zip'
            self.profile = parameters.get('profile')
            self.account = boto3.client('sts').get_caller_identity()['Account']
            self.region = parameters.get('region')
            if self.region is None:
                self.region = boto3.session.Session().region_name

            self.s3_client = get_api_client(self.profile,
                                            self.region,
                                            's3',
                                            self.verbose)

            self.cf_client = get_api_client(self.profile,
                                            self.region,
                                            'cloudformation',
                                            self.verbose)

            self.lambda_client = get_api_client(self.profile,
                                                self.region,
                                                'lambda',
                                                self.verbose)

            self.scheduled = False
            self.package_key = None
            self._read_config_info()
            self._read_network_info()
            self._read_tags()
            self.stage = f"{self.config['config']['stage']}"
            self.name = f"{self.config['config']['name']}-{self.config['config']['stage']}"
            self.uri = f'arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:{self.account}:function:{self.name}/invocations'

            try:
                self.is_service = self.config['config']['apig'].lower() == 'true'
            except Exception:
                self.is_service = False

            if self.is_service:
                self.endpoint_config = self.config.get('network', {}).get('endpoint_config', 'EDGE').upper()

                if self.endpoint_config not in VALID_ENDPOINT_CONFIG:
                    logger.error(f'Network endpoint_config must be one of {VALID_ENDPOINT_CONFIG}')
                    sys.exit(1)
                else:
                    logger.info(f'Network endpoint_config is {self.endpoint_config}')

        except Exception as wtf:
            logger.error(wtf, exc_info=self.verbose)
            logger.error(f'deployer initialization failed with: {wtf}')

    def deploy(self):
        if not self.image_packaging:
            if not self._create_package():
                return False

        if not self._create_cloud_formation():
            return False

        if not self._upsert_function():
            return False

        if self.image_packaging:
            logger.info(f'updating code from {self.image_uri}')
            try:
                response = self.lambda_client.update_function_code(
                    FunctionName=self.name,
                    ImageUri=self.image_uri
                )

                if self.verbose:
                    logger.info(json.dumps(response, indent=2, default=date_converter))

                response_code = response.get('ResponseMetadata', {}).get('HTTPStatusCode', '-1')
                logger.info(f'updating code returned response_code={response_code}')
            except Exception as wtf:
                logger.error(str(wtf), exc_info=self.verbose)
                return False

        return True

    def _copy_stuff(self):
        try:
            shutil.copytree(
                '.',
                self.directory,
                ignore=shutil.ignore_patterns(*IGNORED_STUFF),
                dirs_exist_ok=True
            )

            return True
        except Exception as wtf:
            logging.error(wtf, exc_info=self.verbose)
            return False

    def _find_data(self, the_dir):
        tree = []
        package_file_name = (self.package_file.split('/'))[-1]
        try:
            for folder, _, files in os.walk(the_dir):
                for file in files:
                    if file != package_file_name:
                        tree.append('{}/{}'.format(folder, file))
        except Exception:
            pass

        return tree

    def _create_package_file(self):
        try:
            os.chdir(self.directory)
            logger.debug(f'creating package file: {self.package_file}')
            zf = zipfile.ZipFile(self.package_file, mode='w')

            for f in self._find_data('.'):
                zf.write(f, compress_type=zipfile.ZIP_DEFLATED)

            logger.info(f'created package file: {self.package_file}')
            return True
        except Exception as wtf:
            logging.error(wtf, exc_info=self.verbose)
            return False

    def _store_package_file(self):
        try:
            logger.debug(f'storing package file: {self.package_file}')
            key = f'artifacts/lambdautil/{self.deployment_id}/function.zip'
            self.package_key = key

            with open(self.package_file, 'rb') as the_data:
                bucket = self.config['config']['bucket']
                self.s3_client.upload_fileobj(the_data,
                                              bucket,
                                              key)

            self.s3_bucket = bucket
            self.s3_key = key
            logger.info(f'package file uploaded to s3://{bucket}/{key}')
            return True
        except Exception as wtf:
            logging.error(wtf, exc_info=self.verbose)
            return False

    def _read_config_info(self):
        try:
            config = CaseSensitiveConfigParser()
            config.read(self.config_file)
            the_stuff = {}
            for section in config.sections():
                the_stuff[section] = {}
                for option in config.options(section):
                    the_stuff[section][option] = config.get(section, option)

            self.config = the_stuff
            self.image_packaging = self.config.get('config').get('image_uri') is not None
            if self.image_packaging:
                logger.info('the Lambda function will deployed using the given image')
                self.image_uri = self.config.get('config').get('image_uri')
            else:
                logger.info('the Lambda function will be packaged and deployed from a zip file in AWS S3')
            logger.debug(json.dumps(the_stuff, indent=2))

            if not self._verify_config_info():
                logger.error('invalid config file, exiting')
                sys.exit(1)

            return the_stuff
        except Exception as wtf:
            logger.error(f'reading {self.config_file} failed with: {wtf}')
            return sys.exit(1)

    def _verify_config_info(self):
        try:
            logger.debug(json.dumps(self.config, indent=2))
            return True
        except Exception as wtf:
            logger.error(f'verifying {self.config_file} failed with: {wtf}')
            return sys.exit(1)

    def _read_network_info(self):
        try:
            self._add_vpc_config = False
            subnets = self.config.get('network', {}).get('subnets')
            security_group = self.config.get('network', {}).get('security_group')

            whitelist = self.config.get('network', {}).get('whitelist')
            if whitelist:
                self.whitelist = [wrk.strip() for wrk in whitelist.split(',')]
                logger.info('adding CIDR whitelist to deployment')
            else:
                self.whitelist = None
                logger.debug('not adding CIDR whitelist to deployment')

            if subnets is None and security_group is None:
                return True
            elif None in [subnets, security_group]:
                logger.error('network section requires both "subnets" and "security_group"')
                sys.exit(1)
            else:
                logger.info('adding VPC configuration to deployment')

            if security_group.find(IMPORT_HEADER) > -1:
                self.security_group = []
                wrk = security_group.replace(IMPORT_HEADER, '').replace(']', '')
                for sg in wrk.split(','):
                    tmp = {
                        'Fn::ImportValue': sg.strip()
                    }
                    self.security_group.append(tmp)
            else:
                parts = security_group.split(',')
                self.security_group = [sg.strip() for sg in parts]

            if subnets.find(IMPORT_HEADER) > -1:
                self.subnets = []
                wrk = subnets.replace(IMPORT_HEADER, '').replace(']', '')
                for sn in wrk.split(','):
                    tmp = {
                        'Fn::ImportValue': sn.strip()
                    }
                    self.subnets.append(tmp)
                pass
            else:
                parts = subnets.split(',')
                self.subnets = [subnet.strip() for subnet in parts]

            self._add_vpc_config = True
            return self._add_vpc_config
        except Exception as wtf:
            logger.error(f'reading network config failed with: {wtf}')
            return sys.exit(1)

    def _read_tags(self):
        try:
            self.tags = []

            for k in self.config.get('tags', {}).keys():
                v = self.config.get('tags', {})[k]
                wrk = { 'Key': k, 'Value': v }
                self.tags.append(wrk)

            k = 'FUNCTION_UPSERT_TIME'
            v = str(int(time.time()))
            wrk = { 'Key': k, 'Value': v }
            self.tags.append(wrk)
        except Exception as wtf:
            logger.error(f'reading tags from {self.config_file} failed with: {wtf}')
            return sys.exit(1)

    def _create_package(self):
        try:
            os.makedirs(self.directory, mode=0o700, exist_ok=False)
            if self.verbose:
                command = f'pip install -Ur requirements.txt --target {self.directory}'
            else:
                command = f'pip install -Ur requirements.txt --quiet --target {self.directory}'

            rv = os.system(command)
            if rv != 0:
                logger.error(f'installing requirements failed {rv=}')
                sys.exit(1)

            if not self._copy_stuff():
                logger.error('copying to deployment directory failed')
                sys.exit(1)

            if not self._create_package_file():
                logger.error('creating package failed')
                sys.exit(1)

            if not self._store_package_file():
                logger.error('storing package failed')
                sys.exit(1)

            return True
        except Exception as wtf:
            logger.error(f'error while creating the package [{wtf}]', exc_info=self.verbose)
            sys.exit(1)

    def _create_cloud_formation(self):
        try:
            self.template = copy.deepcopy(starter)

            if self.image_packaging:
                self.template['Parameters']['imageUri'] = { 'Type': 'String' }
                self.template['Resources']['LambdaFunction']['Properties']['Code']['ImageUri'] = { 'Ref': 'imageUri' }
                self.template['Resources']['LambdaFunction']['Properties']['PackageType'] = 'Image'
            else:
                self.template['Parameters']['handler'] = { 'Type': 'String' }
                self.template['Parameters']['runTime'] = { 'Type': 'String' }
                self.template['Parameters']['s3Bucket'] = { 'Type': 'String' }
                self.template['Parameters']['s3Key'] = { 'Type': 'String' }
                self.template['Resources']['LambdaFunction']['Properties']['Code']['S3Bucket'] = { 'Ref': 's3Bucket' }
                self.template['Resources']['LambdaFunction']['Properties']['Code']['S3Key'] = { 'Ref': 's3Key' }
                self.template['Resources']['LambdaFunction']['Properties']['Handler'] = { 'Ref': 'handler' }
                self.template['Resources']['LambdaFunction']['Properties']['Runtime'] = { 'Ref': 'runTime' }

            if self.is_service:
                api_part = copy.deepcopy(the_api)
                api_part['Properties']['EndpointConfiguration']['Types'][0] = self.endpoint_config
                api_part['Properties']['Body']['info']['title'] = self.name
                api_part['Properties']['Body']['basePath'] = f'/{self.stage}'
                api_part['Properties']['Body']['paths']['/']['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['uri'] = self.uri
                api_part['Properties']['Body']['paths']['/{proxy+}']['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['uri'] = self.uri

                deployment_part = copy.deepcopy(the_deployment)
                deployment_part['Properties']['Description'] = self.stage
                deployment_part['Properties']['StageName'] = self.stage

                if self.whitelist:
                    whitelist_part = copy.deepcopy(white_list)
                    whitelist_part['Policy']['Statement'][0]['Condition']['IpAddress']['aws:SourceIp'] = self.whitelist
                    api_part['Properties']['Policy'] = whitelist_part['Policy']

                self.template['Resources']['theAPI'] = api_part
                self.template['Resources']['theDeployment'] = deployment_part
                self._trust_service('apigateway.amazonaws.com')

            if self._add_vpc_config:
                self.template['Resources']['LambdaFunction']['Properties']['VpcConfig'] = {}
                self.template['Resources']['LambdaFunction']['Properties']['VpcConfig']['SecurityGroupIds'] = self.security_group
                self.template['Resources']['LambdaFunction']['Properties']['VpcConfig']['SubnetIds'] = self.subnets

            for k in self.config.get('parameters', {}).keys():
                wrk = self.config.get('parameters', {})[k]
                if wrk.startswith(SSM_HEADER):
                    v = self._read_ssm_thing(wrk)
                else:
                    v = wrk

                self.template['Resources']['LambdaFunction']['Properties']['Environment']['Variables'][k] = v

            self.name = f"{self.config['config']['name']}-{self.config['config']['stage']}"
            logger.debug(json.dumps(self.template, indent=2))
            stack_parameters = []

            if self.image_packaging:
                wrk = {
                    'ParameterKey': 'imageUri',
                    'ParameterValue': self.image_uri
                }
                stack_parameters.append(wrk)
            else:
                wrk = {
                    'ParameterKey': 'runTime',
                    'ParameterValue': self.config['config']['runtime']
                }
                stack_parameters.append(wrk)

                wrk = {
                    'ParameterKey': 's3Bucket',
                    'ParameterValue': self.config['config']['bucket']
                }
                stack_parameters.append(wrk)

                wrk = {
                    'ParameterKey': 's3Key',
                    'ParameterValue': self.package_key
                }
                stack_parameters.append(wrk)

                wrk = {
                    'ParameterKey': 'handler',
                    'ParameterValue': 'main.lambda_handler'
                }
                stack_parameters.append(wrk)

            wrk = {
                'ParameterKey': 'functionName',
                'ParameterValue': self.name
            }
            stack_parameters.append(wrk)

            wrk = {
                'ParameterKey': 'logGroupName',
                'ParameterValue': self.name
            }
            stack_parameters.append(wrk)

            wrk = {
                'ParameterKey': 'retentionDays',
                'ParameterValue': '30'
            }
            stack_parameters.append(wrk)

            wrk = {
                'ParameterKey': 'memorySize',
                'ParameterValue': self.config['config']['memory']
            }
            stack_parameters.append(wrk)

            wrk = {
                'ParameterKey': 'ephemeralStorage',
                'ParameterValue': self.config.get('config', {}).get('ephemeral_storage', 512)
            }
            stack_parameters.append(wrk)

            wrk = {
                'ParameterKey': 'runTime',
                'ParameterValue': self.config.get('config', {}).get('runtime', 'python3.12')
            }
            stack_parameters.append(wrk)

            wrk = {
                'ParameterKey': 'timeOut',
                'ParameterValue': self.config['config']['timeout']
            }
            stack_parameters.append(wrk)

            wrk = {
                'ParameterKey': 'role',
                'ParameterValue': self.config['config']['role']
            }
            stack_parameters.append(wrk)

            cron_expression = self.config['config'].get('schedule', None)
            if cron_expression is not None:
                if self._add_scheduling(cron_expression):
                    logger.info('successfully added schedule rule')
                else:
                    logger.error('failed to add schedule rule')
                    sys.exit(1)

            trusted_account = self.config['config'].get('trustedAccount', None)

            trusted_services = self.config['config'].get('trustedService', None)
            if trusted_services is not None:
                parts = trusted_services.split(',')
                services = [service.strip() for service in list(set(parts))]
                for service in services:
                    if self._trust_service(service, trusted_account):
                        logger.info(f'successfully trusted {service=}')
                    else:
                        logger.error(f'failed to trust {service}')
                        sys.exit(1)

            logger.debug(json.dumps(stack_parameters, indent=2))
            self.stack_parameters = stack_parameters

            self._add_exports()
            if self.verbose or True:
                logger.info(f'writing template to /tmp/{self.deployment_id}.json')
                with open(f'/tmp/{self.deployment_id}.json', 'w') as t:
                    json.dump(self.template, t, indent=2)

            return True
        except Exception as wtf:
            logger.error(f'error while creating the CloudFormation components [{wtf}]', exc_info=self.verbose)
            sys.exit(1)

    def _add_exports(self):
        try:
            short_name = self.config['config']['name']
            wrk = copy.deepcopy(the_outputs)
            wrk['LambdaFunction']['Export']['Name'] = f'{short_name}-Name'
            wrk['LambdaFunctionARN']['Export']['Name'] = f'{short_name}-Arn'
            if self.is_service:
                wrk['RestAPIid']['Export']['Name'] = f'{short_name}-RestAPI'
            else:
                del(wrk['RestAPIid'])

            self.template['Outputs'] = wrk
        except Exception as wtf:
            logger.error(f'error while add the CloudFormation exports [{wtf}]', exc_info=self.verbose)
            sys.exit(1)

    def _add_scheduling(self, cron_expression):
        try:
            wrk = copy.deepcopy(lambda_schedule)
            schedule_id = f"schedule-{self.config['config']['name']}-{self.config['config']['stage']}"
            wrk['Properties']['Targets'][0]['Id'] = schedule_id
            wrk['Properties']['ScheduleExpression'] = cron_expression
            self.template['Resources']['LambdaSchedule'] = wrk

            wrk = copy.deepcopy(trusted_service)
            wrk['Properties']['Principal'] = 'events.amazonaws.com'
            self.template['Resources']['TrustEventsPermission'] = wrk

            self.scheduled = True
            return True
        except Exception as wtf:
            logger.warning(f'problem adding schedule: [{wtf}]')

        return False

    def _trust_service(self, service, trusted_account=None):
        try:
            if self.scheduled and service == 'events.amazonaws.com':
                logger.warning('events.amazonaws.com already trusted implicitly')
                return True

            parts = service.split('.')
            resource_name = f'Trust{parts[0].capitalize()}Permission'
            wrk = copy.deepcopy(trusted_service)
            wrk['Properties']['Principal'] = service

            if trusted_account:
                wrk['Properties']['SourceAccount'] = trusted_account

            self.template['Resources'][resource_name] = wrk

            return True
        except Exception as wtf:
            logger.warning(f'problem adding schedule: [{wtf}]')

        return False

    def _read_ssm_thing(self, complete_value):
        try:
            if self.ssm_client is None:
                self.ssm_client = boto3.client('ssm')

            ssm_key = complete_value.replace('[', '').replace(']', '').replace('ssm:', '').replace(' ', '')
            response = self.ssm_client.get_parameter(Name=ssm_key, WithDecryption=True)
            return response.get('Parameter', {}).get('Value', None)
        except Exception as wtf:
            logger.warning(f'problem adding schedule: [{wtf}]')

        return None

    def _upsert_function(self):
        try:
            tool = StackUtility(verbose=self.verbose,
                                stack_name=self.name,
                                parameters=self.stack_parameters,
                                cf_client=self.cf_client,
                                tags=self.tags,
                                region=self.region,
                                stage=self.stage,
                                template=json.dumps(self.template))
            if tool.upsert():
                tool.print_stack_info()
                return True
            else:
                tool.print_stack_events()
                return False
        except Exception as wtf:
            logger.error(f'error while upserting the CloudFormation stack: [{wtf}]', exc_info=self.verbose)
            sys.exit(1)
