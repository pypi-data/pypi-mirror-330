import os

LAMBDAUTIL_ROLE = os.environ.get('LAMBDAUTIL_ROLE', None)
LAMBDAUTIL_BUCKET = os.environ.get('LAMBDAUTIL_BUCKET', None)
LAMBDAUTIL_TMP = os.environ.get('LAMBDAUTIL_TMP', '/tmp')

if __name__ == "__main__":
    print(f'{LAMBDAUTIL_BUCKET=}')
    print(f'  {LAMBDAUTIL_ROLE=}')
    print(f'   {LAMBDAUTIL_TMP=}')
