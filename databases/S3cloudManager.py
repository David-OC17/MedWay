'''
Here we provide a manager class to administer the S3 instance in AWS.
The S3 bucket is used to store report .pdf files.
The bucket is divided into 3 main folders:
* daily-reports
* weekly-reports
* monthly-reports

Use the provided methods as appropiate to add and retreive files.
'''

class S3manager:
    '''
    Use this class in order to administer the remote (cloud based) AWS-S3 bucket for analytics reports.
    '''
    def __init__(self) -> None:
        pass
    
    #################### START -> Upload files ####################

    def uploadByName(self, filename:str, path: str) -> None:
        '''
        Upload one file by passing its name and location (file path).
        '''
        pass
    
    def uploadByName(self, filenames:tuple, path: str) -> None:
        '''
        Upload several files by passing their names and location (file path).
        '''
        pass
    
    #################### END -> Upload files ####################
    
    #################### START -> Download files ####################
    
    def downloadByName(self, filename: str, periodType: str) -> None:
        '''
        Download one file from S3 bucket by specifiying filename and the period type of the report.
        '''
        pass
    
    def downloadByName(self, filenames: tuple, periodType: str) -> None:
        '''
        Download several files from S3 bucket by specifiying filenames and the period type of the reports.
        Note: all the reports must be the same type for the download to be done.
        '''
        pass
    
    #################### END -> Download files ####################
    
    
    '''
    import boto3

    s3_client = boto3.client('s3')

    # we need the bucket name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object() # put the result report into the bucket
    # .put_object(key = key_name, Body = report )

    # configure accessible to other elements in AWS
        
    '''