if __name__ == '__main__':
    import copy
    import json

starter = {
    'AWSTemplateFormatVersion': '2010-09-09',
    'Description': '42 is the answer',
    'Parameters': {
        'functionName': {
            'Type': 'String'
        },
        'logGroupName': {
            'Type': 'String'
        },
        'retentionDays': {
            'Type': 'String'
        },
        'memorySize': {
            'Type': 'String'
        },
        'timeOut': {
            'Type': 'String'
        },
        'ephemeralStorage': {
            'Type': 'Number'
        },
        'runTime': {
            'Type': 'String'
        },
        'role': {
            'Type': 'String'
        }
    },
    'Resources': {
        'LambdaLogGroup': {
            'Type': 'AWS::Logs::LogGroup',
            'Properties': {
                'LogGroupName': {
                    'Ref': 'logGroupName'
                },
                'RetentionInDays': {
                    'Ref': 'retentionDays'
                }
            }
        },
        'LambdaFunction': {
            'Type': 'AWS::Lambda::Function',
            'Properties': {
                'Code': {},
                'Environment': {
                    'Variables': {}
                },
                'EphemeralStorage': {
                    'Size': {
                        'Ref': 'ephemeralStorage'
                    }
                },
                'FunctionName': {
                    'Ref': 'functionName'
                },
                'MemorySize': {
                    'Ref': 'memorySize'
                },
                'Role': {
                    'Ref': 'role'
                },
                'Timeout': {
                    'Ref': 'timeOut'
                }
            }
        }
    }
}

lambda_schedule = {
    "Type": "AWS::Events::Rule",
    "DependsOn": "LambdaFunction",
    "Properties": {
        "Description": "Schedule for a fantastic function",
        "ScheduleExpression": {
            "Ref": "scheduleExpression"
        },
        "State": "ENABLED",
        "Targets": [
            {
                "Arn": {
                    "Fn::GetAtt": [
                        "LambdaFunction",
                        "Arn"
                    ]
                },
                "Id": "unknown-none"
            }
        ]
    }
}

trusted_service = {
    "Type": "AWS::Lambda::Permission",
    "DependsOn": "LambdaFunction",
    "Properties": {
        "FunctionName": {
            "Fn::GetAtt": [
                "LambdaFunction",
                "Arn"
            ]
        },
        "Action": "lambda:InvokeFunction",
        "Principal": {
            "Ref": "trustedService"
        }
    }
}

'''
aws:SourceIp is a list of CIDR blocks to let in. Sibling of
Properties.Body in the_api
'''
white_list = {
    "Policy": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "execute-api:Invoke",
                "Resource": "arn:aws:execute-api:*:*:*",
                "Condition": {
                    "IpAddress": {
                        "aws:SourceIp": []
                    }
                }
            }
        ]
    }
}

'''
Path: Properties|Body|info|title - value: xxx-title
Path: Properties|Body|basePath - value: xxx-base-path
Path: Properties|Body|paths|/|x-amazon-apigateway-any-method|x-amazon-apigateway-integration|uri - value: xxx-uri0
Path: Properties|Body|paths|/{proxy+}|x-amazon-apigateway-any-method|x-amazon-apigateway-integration|uri - value: xxx-uri1
'''
the_api = {
    "Type": "AWS::ApiGateway::RestApi",
    "DependsOn": "LambdaFunction",
    "Properties": {
        "Description": "LambdaUtil created this AWS ApiGateway RestApi thing",
        "EndpointConfiguration": {
            "Types": [
                "EDGE"
            ]
        },
        "Body": {
            "swagger": "2.0",
            "info": {
                "version": "2017-11-15T16:30:51Z",
                "title": "xxx-title",  # "baz-svc-dev"
            },
            "host": "ozi3yy5k9a.execute-api.us-east-1.amazonaws.com",
            "basePath": "xxx-base-path",  # "/dev",
            "schemes": [
                "https"
            ],
            "paths": {
                "/": {
                    "x-amazon-apigateway-any-method": {
                        "produces": [
                            "application/json"
                        ],
                        "responses": {
                            "200": {
                                "description": "200 response",
                                "schema": {
                                    "$ref": "#/definitions/Empty"
                                }
                            }
                        },
                        "x-amazon-apigateway-integration": {
                            "responses": {
                                "default": {
                                    "statusCode": "200"
                                }
                            },
                            "uri": "xxx-uri0",  # "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:018734038160:function:baz-svc-dev/invocations",
                            "passthroughBehavior": "when_no_match",
                            "httpMethod": "POST",
                            "contentHandling": "CONVERT_TO_TEXT",
                            "type": "aws_proxy"
                        }
                    }
                },
                "/{proxy+}": {
                    "options": {
                        "consumes": [
                            "application/json"
                        ],
                        "produces": [
                            "application/json"
                        ],
                        "responses": {
                            "200": {
                                "description": "200 response",
                                "schema": {
                                    "$ref": "#/definitions/Empty"
                                },
                                "headers": {
                                    "Access-Control-Allow-Origin": {
                                        "type": "string"
                                    },
                                    "Access-Control-Allow-Methods": {
                                        "type": "string"
                                    },
                                    "Access-Control-Allow-Headers": {
                                        "type": "string"
                                    }
                                }
                            }
                        },
                        "x-amazon-apigateway-integration": {
                            "responses": {
                                "default": {
                                    "statusCode": "200",
                                    "responseParameters": {
                                        "method.response.header.Access-Control-Allow-Methods": "'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'",
                                        "method.response.header.Access-Control-Allow-Headers": "'Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token'",
                                        "method.response.header.Access-Control-Allow-Origin": "'*'"
                                    }
                                }
                            },
                            "requestTemplates": {
                                "application/json": "{\"statusCode\": 200}"
                            },
                            "passthroughBehavior": "when_no_match",
                            "contentHandling": "CONVERT_TO_TEXT",
                            "type": "mock"
                        }
                    },
                    "x-amazon-apigateway-any-method": {
                        "produces": [
                            "application/json"
                        ],
                        "parameters": [
                            {
                                "name": "proxy",
                                "in": "path",
                                "required": True,
                                "type": "string"
                            }
                        ],
                        "responses": {},
                        "x-amazon-apigateway-integration": {
                            "responses": {
                                "default": {
                                    "statusCode": "200"
                                }
                            },
                            "uri": "xxx-uri1",  # "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:018734038160:function:baz-svc-dev/invocations",
                            "passthroughBehavior": "when_no_match",
                            "httpMethod": "POST",
                            "cacheNamespace": "fyc8uq",
                            "cacheKeyParameters": [
                                "method.request.path.proxy"
                            ],
                            "contentHandling": "CONVERT_TO_TEXT",
                            "type": "aws_proxy"
                        }
                    }
                }
            },
            "definitions": {
                "Empty": {
                    "type": "object",
                    "title": "Empty Schema"
                }
            },
            "x-amazon-apigateway-binary-media-types": [
                "*/*"
            ]
        }
    }
}

the_deployment = {
    "DependsOn": "theAPI",
    "Properties": {
        "Description": None,  # "dev",
        "RestApiId": {
            "Ref": "theAPI"
        },
        "StageName": None,  # "dev"
    },
    "Type": "AWS::ApiGateway::Deployment"
}

the_outputs = {
    "LambdaFunction": {
        "Description": "The name of a LambdaUtil function",
        "Value": {
            "Ref": "LambdaFunction"
        },
        "Export": {
            "Name": "XXX-Name"
        }
    },
    "LambdaFunctionARN": {
        "Description": "The ARN of a LambdaUtil function",
        "Value": {
            "Fn::GetAtt": [
                "LambdaFunction",
                "Arn"
            ]
        },
        "Export": {
            "Name": "XXX-Arn"
        }
    },
    "RestAPIid": {
        "Description": "The ID of the resulting RestAPI",
        "Value": {
            "Ref": "theAPI"
        },
        "Export": {
            "Name": "XXX-RestAPI"
        }
    }
}


def print_paths(dictionary, path=[]):
    for key, value in dictionary.items():
        new_path = path + [str(key)]

        if isinstance(value, dict):
            print_paths(value, new_path)
        else:
            leaf_path = '|'.join(new_path)
            print(f'Leaf node at path: {leaf_path}, Value: {value}')

if __name__ == '__main__':
    '''
    Path: Properties|Body|info|title - value: xxx-title
    Path: Properties|Body|basePath - value: xxx-base-path
    Path: Properties|Body|paths|/|x-amazon-apigateway-any-method|x-amazon-apigateway-integration|uri - value: xxx-uri0
    Path: Properties|Body|paths|/{proxy+}|x-amazon-apigateway-any-method|x-amazon-apigateway-integration|uri - value: xxx-uri1
    '''
    proxy = "/{proxy+}"
    print(proxy)
    print(proxy)
    print(proxy)
    print(proxy)
    print(proxy)
    a = copy.deepcopy(the_api)
    a['Properties']['Body']['info']['title'] = 'TEST_TITLE'
    a['Properties']['Body']['basePath'] = 'TEST_BASE'
    a['Properties']['Body']['paths']['/']['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['uri'] = 'TEST_URI0'
    a['Properties']['Body']['paths'][proxy]['x-amazon-apigateway-any-method']['x-amazon-apigateway-integration']['uri'] = 'TEST_URI1'

    with open('/tmp/api.json', 'w') as f:
        json.dump(a, f, indent=2)
