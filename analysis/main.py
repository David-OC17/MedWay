'''
Use this script as the main file to run in order to analyze some batch of data and generate the corresponding report.
The options for the analysis are:
- Daily
- Weekly
- Monthly

The implementation uses a XGboost. See the `About.md` file for more information.
'''

from stateAnalysis import analyzeState, trainAnalyzeState
from reportGenerator import generatePDF, conditionStatistics, createStateTable
import subprocess
import argparse

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
    
    
    #subprocess.run(['bash'], './removeReport')

