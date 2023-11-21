from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

import pandas as pd
import pickle
import numpy as np

def trainAnalyzeState(testing:bool=False) -> None:
    '''
    Generate an analysis of the state of the batches of medicine included in the given period information. 
    The function pulls the data from the appropriate database, trains the model and exports it to a file.
    The model is given the name of the selected period, plus 'model' (e.g. dailyModel).
    '''
    
    '''
    1. Get the data and split it
    2. Purge the data and split it
    3. Create the model and fit it
    Optional: evaluate the performance of the evaluation inline
    4. Export the model
    '''
    
    # Load the data by Pandas and separate X from y
    # header = ["ID", "batch_number", "device_number", "date", "temperature", "humidity", "light_percentage", "state"]
    if testing:
        path = '../test/data/sensor_data_train.csv'
    else: 
        path = './temp/tempData.csv'
    
    data = pd.read_csv(path)
    X = data[['temperature', 'humidity', 'light_percentage']]
    y = data[['state']]
    
    # Split the dataset into training and testing sets
    # If testing, change this test size to above 0
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Create an XGBoost classifier
    model = XGBClassifier(objective="multi:softmax", num_class=3, seed=42)

    # Train the model
    model.fit(X_train, y_train)

    ############### Make predictions in order to test the model ###############
    # from sklearn.metrics import accuracy_score
    # Make predictions on the test set
    # y_pred = model.predict(X_test)

    # Evaluate the model accuracy
    # accuracy = accuracy_score(y_test, y_pred)
    # print(f"Accuracy: {accuracy * 100:.2f}%")
    
    # Getting around a 91 - 93 % Accuracy
    ###########################################################################
    
    # Save the model to a file
    with open('./models/xgboost_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

def analyzeState(testing:bool=False) -> tuple:
    '''
    Use this function during deployment in order to use the generated model. Train and export the model using trainAnalyzeState(...).
    Specify the type of model to use. If the model is not trained, the function will raise an appropriate error.
    Returns a tuple of simple statistics and data -> alertCount, numBatches, goodBatches, badBatches, startDate, endDate
    '''
    
    '''
    Steps of analysis:
    1. Load the model
    2. Load the temp data
    3. Separate the data by batch
    4. Make the predictions
    5. Evaluate if each batch is in good condition or not
        5.1 Save some of the statistics on variables, for the report
    6. Save the information of the results into temp files
    '''
    
    # General variables for basic statistics
    alertCount = 0
    goodBatches = 0
    badBatches = 0
    
    try:
        with open('./models/xgboost_model.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
    except:
        print('There is no model to import and use. Train one.')
        
    # Read the data to classify
    if testing:
        path = '../test/data/sensor_data_train.csv'
        data = pd.read_csv(path)
        columns_drop = ["ID", "device_number", "state"]
        analysisData = data.drop(columns=columns_drop, inplace=False)
        
    else: 
        path = './temp/tempData.csv'
        data = pd.read_csv(path)
        columns_drop = ["ID", "device_number"]
        analysisData = data.drop(columns=columns_drop, inplace=False)
    
    # Split the data into several dataframes, according to the batch number
    # ["ID", "batch_number", "device_number", "date", "temperature", "humidity", "light_percentage"]
    
    # Get the date beginning and end, then drop date
    startDate = analysisData.head(1)["date"]
    endDate = analysisData.tail(1)["date"]
    analysisData = data.drop(columns=["date"], inplace=False)
    
    grouped = analysisData.groupby('batch_number')
    
    #print(grouped.describe())
    #print(grouped.head())
    
    groups = grouped.groups
    
    # For each group, call the evaluation and save the results into a map of of lists
    results = {}
    for batch in groups:
        results[batch] = loaded_model.predict(grouped.get_group(batch)[["temperature", "humidity", "light_percentage"]])        
        
    # for i in results:
    #     print(results[i])
    
    # See if the batches passed the analysis
    passed = {}
    for batch in groups:
        num_ones = np.count_nonzero(results[batch])
        num_zeros = len(results[batch]) - num_ones
        alertCount +=  num_zeros
        
        # If the batch was in bad conditions for 10 minutes or more, it does not pass
        if num_zeros >= 10:
            passed[batch] = False
            badBatches += 1
        else:
            passed[batch] = True
            goodBatches += 1
    
    # Calculate some final basic statistics for the report
    numBatches = len(groups)
    
    # Return all the statistics for the report to be generated
    return (alertCount, numBatches, goodBatches, badBatches, startDate, endDate)