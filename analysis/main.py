'''
Use this script as the main file to run in order to analyze some batch of data and generate the corresponding report.
The options for the analysis are:
- Daily
- Weekly
- Monthly

The implementation uses a XGboost. See the `About.md` file for more information.
'''
from boto3.session import Session
from boto3 import client
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from stateAnalysis import analyzeState, trainAnalyzeState
from reportGenerator import generatePDF, conditionStatistics, createStateTable
import subprocess
import argparse

load_dotenv()

if __name__ == '__main__':
    # Select the type of analysis to run (daily or monthly)
    parser = argparse.ArgumentParser(description='Run analysis on a set of data, produce pdf.')
    parser.add_argument('--periodType', type=str, help='Select daily/monthly analysis.')
    args = parser.parse_args()
    
    periodType = args[0]
    
    # Make a query to the RDS database to pull the appropriate data and save to './temp/tempData.csv'
    
    # Train the model for a daily basis
    trainAnalyzeState(periodType=periodType, testing=True)
    
    
    # Generate the analysis for the given period
    stateResults = analyzeState(periodType=periodType, testing=True)
    # stateResults = (alertCount, numBatches, goodBatches, badBatches, passed)
    
    # Create table of state for each batch
    createStateTable(stateResults[4])
    
    # Generate graphs and return some stats
    statResults = conditionStatistics(withStats=True, testing=True, show=False, maskOutliers=False)
    # statResults = (minTemp, maxTemp, minHum, maxHum, minLight, maxLight)
    
    
    # Generate the report from the results of the last analysis
    # The function receives:
    # alertCount:int, numBatches:int, goodBatches:int, badBatches:int, groups:list, minTemp:float, maxTemp:float, minHum:float, maxHum:float, minLight:float, maxLight:float
    generatePDF(periodType=periodType, product='Insulin', passed=stateResults[4] ,alertCount=stateResults[0], numBatches=stateResults[1], goodBatches=stateResults[2], badBatches=stateResults[3],
                minTemp=statResults[0], maxTemp=statResults[1], minHum=statResults[2], maxHum=statResults[3], minLight=statResults[4], maxLight=statResults[5])
    
    #subprocess.run(['bash'], './cleanUp.sh')
    
    # Send the last .pdf report to the S3 bucket of its appropriate type
     if periodType == 'daily':
        dia = datetime.now().strftime("%B %d")
        local_pdf_path = './reports/dailyReport.pdf'
        pdf_key = dia

            
    elif periodType == 'monthly':
        mes = datetime.now().strftime("%B")
        local_pdf_path = './reports/monthlyReport.pdf'
        pdf_key = mes

    try:
        s3 = boto3.client('s3') 
        self._s3_connection: Session = client()
        self.db_config = {
            'aws_access_key_id': os.getenv("AWS_ACCESS_KEY_ID"),
            'aws_secret_access_key': os.getenv("AWS_SECRET_ACCESS_KEY"),
            'region_name': os.getenv("REGION_NAME"),
            'bucket_name' os.getenv: ("BUCKET_NAME")
            

            }

        s3.upload_file(local_pdf_path, bucket_name, pdf_key)
        print(f"Upload of PDF to S3 Successful")
    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(e)

    
    #subprocess.run(['bash'], './removeReport')

