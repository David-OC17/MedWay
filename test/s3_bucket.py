'''
Test the connection to S3 by uploading an empty (blank) .pdf file.
'''

import boto3
import sys
from ..databases.config import cloud_database

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_REGION = 'us-east-1'  # Replace with your desired region
BUCKET_NAME = AWS_ACCESS_KEY_ID.lower() + '-dump'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

# Blank .pdf file
testfile = './testfile.pdf'

print(f'Uploading {testfile} to Amazon S3 bucket {BUCKET_NAME}')

def upload_progress_callback(bytes_transferred):
    sys.stdout.write('.')
    sys.stdout.flush()

s3.upload_file(testfile, BUCKET_NAME, 'my_test_file', Callback=upload_progress_callback)
input("Click enter to continue to download file from bucket.")

input("Click enter to continue to delete file from bucket.")