'''
This functions use a LaTeX template to dynamically add data for the report and generate it for the given
period of time. There are three templates, one for each period option.

Take default images and take new graphs from the `images` directory.
Save the reports into the `reports` folder.
'''

import seaborn
import pandas as pd

def conditionStatistics() -> tuple:
    '''
    Reads the appropriate file, creates the plots for the report and calculates the 
    '''
    pass

def generatePDF(alertCount:int, numBatches:int, goodBatches:int, badBatches:int, startDate, endDate) -> None:
    '''
    Takes the appropriate template, adds the dynamic data, compiles into a `.pdf` document.
    '''
    
    
    pass