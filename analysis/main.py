'''
Use this script as the main file to run in order to analyze some batch of data and generate the corresponding report.
The options for the analysis are:
- Daily
- Weekly
- Monthly

The implementation uses a XGboost. See the `About.md` file for more information.
'''

from stateAnalysis import analyzeState, trainAnalyzeState
from reportGenerator import generatePDF, conditionStatistics
import subprocess

if __name__ == '__main__':
    # Make a query to the RDS database to pull the appropriate data and save to './temp/tempData.csv'
    
    # Train the model for a daily basis
    #trainAnalyzeState(testing=True)
    
    
    # Generate the analysis for the given period
    stateResults = analyzeState(testing=True)
    # stateResults = (alertCount, numBatches, goodBatches, badBatches, groups)
    
    
    # Generate graphs and return some stats
    statResults = conditionStatistics(withStats=True, testing=True, show=False, maskOutliers=False)
    # statResults = (minTemp, maxTemp, minHum, maxHum, minLight, maxLight
    
    
    # Generate the report from the results of the last analysis
    # The function receives:
    # alertCount:int, numBatches:int, goodBatches:int, badBatches:int, groups:list, minTemp:float, maxTemp:float, minHum:float, maxHum:float, minLight:float, maxLight:float
    generatePDF(product='Insulin', alertCount=stateResults[0], numBatches=stateResults[1], goodBatches=stateResults[2], badBatches=stateResults[3], groups=stateResults[4],
                minTemp=statResults[0], maxTemp=statResults[1], minHum=statResults[2], maxHum=statResults[3], minLight=statResults[4], maxLight=statResults[5])
    
    
    # Send the last .pdf report to the S3 bucket of its appropriate type
    
    
    # Clean all the temp files
    #subprocess.run(['bash'], './cleanUp.sh')

