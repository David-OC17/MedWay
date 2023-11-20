'''
Use this script as the main file to run in order to analyze some batch of data and generate the corresponding report.
The options for the analysis are:
- Daily
- Weekly
- Monthly

The implementation uses a XGboost. See the `About.md` file for more information.
'''

from stateAnalysis import analyzeState, trainAnalyzeState
from reportGenerator import generatePDF
import subprocess

if __name__ == '__main__':
    # Make a query to the RDS database to pull the appropriate data and save to './temp/tempData.csv'
    
    # Train the model for a daily basis
    #trainAnalyzeState(True)
    
    # Generate the analysis for the given period
    results = analyzeState(testing=True)
    for item in results:
        print(type(item))
        
    # Generate the report from the results of the last analysis
    #generatePDF()
    
    # Send the last .pdf report to the S3 bucket of its appropriate type
    
    
    # Clean all the temp files
    #subprocess.run(['bash'], './cleanUp.sh')

