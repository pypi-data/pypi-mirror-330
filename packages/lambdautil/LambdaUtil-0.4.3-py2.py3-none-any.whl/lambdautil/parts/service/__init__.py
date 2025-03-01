main_code = '''import os
import json

from flask import request
from zevon import FlaskLambda

\'\'\'
The FlaskLambda object that is created is the entry point for the lambda. The
LambdaTool deployer expects this to be called \'lambda_handler\'
\'\'\'
lambda_handler = FlaskLambda(__name__)


def create_json_dump(o):
    \'\'\'
    Another helper function for JSON serialization
    \'\'\'
    if isinstance(o, datetime.datetime):
        return o.__str__()
    elif isinstance(o, datetime.date):
        return o.__str__()
    elif isinstance(o, bytes):
        return o.decode('utf-8')

    return None


@lambda_handler.route(\'/\', methods=[\'GET\'])
def OK():
    \'\'\'
    Redirect to the README doc

    Args:
        None

    Returns:
        tuple of (body, status code, content type) that API Gateway understands
    \'\'\'
    return (
        'OK',
        200,
        {'Content-Type': 'text/plain'}
    )


@lambda_handler.route(\'/doc\', methods=[\'GET\'])
def document():
    \'\'\'
    Redirect to the README doc

    Args:
        None

    Returns:
        tuple of (body, status code, content type) that API Gateway understands
    \'\'\'
    return (
        slash_html,
        200,
        {'Content-Type': 'text/html'}
    )


@lambda_handler.route(\'/answer\', methods=[\'GET\'])
def get_answer():
    \'\'\'
    Example of getting someething from function.properties

    Args:
        None

    Returns:
        tuple of (body, status code, content type) that API Gateway understands
    \'\'\'
    answer = os.environ.get(\'ANSWER\', \'0\')
    args = json.dumps(request.args.copy(), indent=2)
    msg = f\'answer = {answer}  args = {args}\'

    return (
        msg,
        200,
        {'Content-Type': 'text/plain'}
    )


@lambda_handler.route(\'/example\', methods=[\'GET\', \'POST\'])
def food():
    \'\'\'
    A contrived example function that will return some meta-data about the
    invocation.

    Args:
        None

    Returns:
        tuple of (body, status code, content type) that API Gateway understands
    \'\'\'
    data = {
        'form': request.form.copy(),
        'args': request.args.copy(),
        'json': request.json
    }
    return (
        json.dumps(data, indent=4, sort_keys=True),
        200,
        {'Content-Type': 'application/json'}
    )


@lambda_handler.route('/event', methods=['GET'])
def event():
    \'\'\'
    Return the event as application/json

    Args:
        None

    Returns:
        tuple of (body, status code, content type) that API Gateway understands
    \'\'\'
    return (
        json.dumps(lambda_handler.get_event(), default=create_json_dump, indent=2),
        200,
        {'Content-Type': 'application/json'}
    )

slash_html = \'\'\'<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Lambtool Readme</title>
    <meta http-equiv="refresh" content="0;URL='https://github.com/muckamuck/lambda-tool/blob/master/README.md'" />
  </head>
  <body></body>
</html>
\'\'\'

if __name__ == '__main__':
    lambda_handler.run(debug=True)
'''

requirements_txt = '''zevon>=0.3'''


if __name__ == '__main__':
    print(main_code)
