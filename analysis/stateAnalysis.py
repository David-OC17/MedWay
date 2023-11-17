from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def trainAnalyzeState(period:str) -> None:
    '''
    Generate an analysis of the state of the batches of medicine included in the given period information. 
    The function pulls the data from the appropriate database, trains the model and exports it to a file.
    The model is given the name of the selected period, plus 'model' (e.g. dailyModel).
    '''
    

def analyzeState(period:str) -> None:
    '''
    Use this function during deployment in order to use the generated model. Train and export the model using trainAnalyzeState(...).
    Specify the type of model to use. If the model is not trained, the function will raise an appropriate error.
    '''
    
    # Select the model from the files
    pass