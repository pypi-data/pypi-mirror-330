docker_file = '''FROM public.ecr.aws/lambda/python:3.12

RUN dnf install -y git

COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY main.py ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

CMD [ "main.lambda_handler" ]
'''
