import boto3
from time import strftime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
import os

load_dotenv()

periodType = 'daily'

if periodType == 'daily':
    day = strftime("%Y-%m-%d")
    object_key = f'daily/{day}.pdf'
    local_pdf_path = './reports/dailyReport.pdf'
    bucket_name = 'medway-reports-pdfs'

# elif periodType == 'monthly':
#     mes = datetime.now().strftime("%B")
#     local_pdf_path = './reports/monthlyReport.pdf'
#     pdf_key = mes

try:
    s3 = boto3.client('s3', 
                        aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
                        aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"))
    
    s3.upload_file(local_pdf_path, bucket_name, object_key)
    
    print(f"Upload of PDF to S3 Successful")
except NoCredentialsError:
    print("Credentials not available")
except PartialCredentialsError:
    print("Credentials not available")
except Exception as e:
    print(e)