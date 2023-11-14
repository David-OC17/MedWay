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

if __name__ == '__main__':
    # Selelect the period of the analysis
    # Options:
    # D -> Daily
    # W -> Weekly
    # M -> Monthly
    
    # Train the model for a daily basis
    trainAnalyzeState('D')
    
    # Generate the analysis for the given period
    analyzeState('D')
    
    # Generate the report from the results of the last analysis
    generatePDF('D')
    
    # Send the last .pdf report to the S3 bucket of its appropiate type

