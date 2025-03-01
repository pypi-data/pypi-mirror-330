'''
Do all the CloudFormation work
'''
import os
import sys
import json
import logging
import time
import uuid

from tabulate import tabulate
from botocore.exceptions import ClientError

from lambdautil.utility import date_converter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

first_token = '__FIRST_TOKEN___'
deletable_states = [
    'REVIEW_IN_PROGRESS',
    'ROLLBACK_COMPLETE'
]

complete_states = [
    'CREATE_COMPLETE',
    'UPDATE_COMPLETE',
    'UPDATE_ROLLBACK_COMPLETE'
]

successful_states = [
    'CREATE_COMPLETE',
    'UPDATE_COMPLETE',
    'DELETE_COMPLETE'
]

try:
    POLL_INTERVAL = int(os.environ.get('CSU_POLL_INTERVAL', 30))
except:
    POLL_INTERVAL = 30

class StackUtility:
    def __init__(self, **kwargs):
        self.verbose = kwargs['verbose']
        if self.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        self.stack_name = kwargs['stack_name']
        self.template = kwargs['template']
        self.parameters = kwargs['parameters']
        self.cf_client = kwargs['cf_client']
        self.tags = kwargs['tags']
        self.region = kwargs['region']
        self.stage = kwargs['stage']
        self.stack_id = None
        self._set_update()

    def upsert(self):
        if self.update:
            return self._update_stack()
        else:
            return self._create_stack()

    def _update_stack(self):
        try:
            stack = self.cf_client.update_stack(
                StackName=self.stack_name,
                TemplateBody=self.template,
                Parameters=self.parameters,
                Tags=self.tags,
                Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND'],
                ClientRequestToken=str(uuid.uuid4())
            )
            self.stack_id = stack.get('StackId')
            logger.info(f'existing stack ID: {self.stack_id}')
            return self._poll_stack()
        except Exception as wtf:
            logger.error(f'problem while updating the stack [{wtf}]', exc_info=self.verbose)

        return False

    def _create_stack(self):
        try:
            stack = self.cf_client.create_stack(
                StackName=self.stack_name,
                TemplateBody=self.template,
                Parameters=self.parameters,
                Tags=self.tags,
                Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND'],
                ClientRequestToken=str(uuid.uuid4())
            )
            self.stack_id = stack.get('StackId')
            logger.info(f'new stack ID: {self.stack_id}')
            return self._poll_stack()
        except Exception as wtf:
            logger.error(f'problem while creating the stack [{wtf}]', exc_info=self.verbose)

        return False

    def _set_update(self):
        try:
            self.update= False
            response = self.cf_client.describe_stacks(StackName=self.stack_name)
            stack = response['Stacks'][0]
            stack_status = stack.get('StackStatus')
            if stack_status in deletable_states:
                logger.info(f'stack is in {stack_status} and should be deleted')
                del_stack_resp = self.cf_client.delete_stack(StackName=self.stack_name)
                logger.info(f'delete started for stack: {self.stack_name}')
                logger.debug('delete stack response:')
                logger.debug(json.dumps(del_stack_resp, default=date_converter, indent=2))
                stack_deleted = self._poll_stack()

                if not stack_deleted:
                    logger.error(f'failed to delete stack {self.stack_name}')
                    sys.exit(1)
            elif stack_status.endswith('IN_PROGRESS'):
                logger.error(f'the stack {self.stack_name} is in state {stack_status}')
                sys.exit(1)

            if stack['StackStatus'] in complete_states:
                self.update = True

        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ValidationError':
                self.update = False
            else:
                logger.error(f'failed to determine status of {self.stack_name}: [{ce}]')
                sys.exit(1)
        except Exception as wtf:
            logger.error(f'failed to determine status of {self.stack_name}: [{wtf}]')
            sys.exit(1)

        logger.info(f'update_stack: {self.update}')

    def _poll_stack(self):
        logger.info(f'polling stack status, POLL_INTERVAL={POLL_INTERVAL}')
        stack_name = self.stack_name
        while True:
            try:
                response = self.cf_client.describe_stacks(StackName=stack_name)
                stack = response['Stacks'][0]
                current_status = stack['StackStatus']
                logger.info(f'current status of {stack_name}: {current_status}')
                if current_status.endswith('COMPLETE') or current_status.endswith('FAILED'):
                    if current_status in successful_states:
                        return True
                    else:
                        return False

                time.sleep(POLL_INTERVAL)
            except ClientError as wtf:
                if str(wtf).find('does not exist') == -1:
                    logger.error(f'exception caught in polling: {wtf}', exc_info=self.verbose)
                    return False
                else:
                    logger.info(f'{stack_name} is gone')
                    return True
            except Exception as wtf:
                logger.error(f'exception caught in polling: {wtf}', exc_info=self.verbose)
                return False

    def print_stack_info(self):
        '''
        List resources from the given stack

        Args:
            None

        Returns:
            A dictionary filled resources or None if things went sideways
        '''
        try:
            rest_api_id = None
            deployment_found = False

            response = self.cf_client.describe_stack_resources(
                StackName=self.stack_name
            )

            print('\nThe following resources were created:')
            rows = []
            for resource in response['StackResources']:
                if resource['ResourceType'] == 'AWS::ApiGateway::RestApi':
                    rest_api_id = resource['PhysicalResourceId']
                elif resource['ResourceType'] == 'AWS::ApiGateway::Deployment':
                    deployment_found = True

                row = []
                row.append(resource['ResourceType'])
                row.append(resource['LogicalResourceId'])
                row.append(resource['PhysicalResourceId'])
                rows.append(row)
            print(tabulate(rows, headers=['Resource Type', 'Logical ID', 'Physical ID']))

            token = first_token
            stack_exports = []
            while token is not None:
                if token == first_token:
                    response = self.cf_client.list_exports()
                else:
                    response = self.cf_client.list_exports(NextToken=token)

                exports = response.get('Exports', [])
                wrk = [export for export in exports if export['ExportingStackId'] == self.stack_id]
                stack_exports.extend(wrk)
                token = response.get('NextToken')

            print('\nThe following CloudFormation exports were created:')
            rows = []
            for thing in stack_exports:
                row = []
                row.append(thing['Name'])
                row.append(thing['Value'])
                rows.append(row)

            print(tabulate(rows, headers=['Export Name', 'Value']))

            if rest_api_id and deployment_found:
                url = f'https://{rest_api_id}.execute-api.{self.region}.amazonaws.com/{self.stage}'
                print('\nThe deployed service can be found at this URL:')
                print(f'\t{url}\n')

            return response
        except Exception as wtf:
            print(wtf)
            return None

    def print_stack_events(self):
        '''
        List events from the given stack

        Args:
            None

        Returns:
            None
        '''
        first_token = '16e2d644940c9bbe1edea1de9e48fe95'
        keep_going = True
        next_token = first_token
        current_request_token = None
        rows = []
        try:
            while keep_going and next_token:
                if next_token == first_token:
                    response = self.cf_client.describe_stack_events(
                        StackName=self.stack_name
                    )
                else:
                    response = self.cf_client.describe_stack_events(
                        StackName=self.stack_name,
                        NextToken=next_token
                    )

                next_token = response.get('NextToken', None)
                for event in response['StackEvents']:
                    row = []
                    event_time = event.get('Timestamp')
                    request_token = event.get('ClientRequestToken', 'unknown')
                    if current_request_token is None:
                        current_request_token = request_token
                    elif current_request_token != request_token:
                        keep_going = False
                        break

                    row.append(event_time.strftime('%x %X'))
                    row.append(event.get('LogicalResourceId'))
                    row.append(event.get('ResourceStatus'))
                    row.append(event.get('ResourceStatusReason', ''))
                    rows.append(row)

            if len(rows) > 0:
                print('\nEvents for the current upsert:')
                print(tabulate(rows, headers=['Time', 'Logical ID', 'Status', 'Message']))
                return True

            print('\nNo stack events found\n')
        except Exception as wtf:
            print(wtf)

        return False
