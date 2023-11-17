from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from databases.MySQLmanager import MySQLmanager

def loadDataWithPandas() -> None:
    '''
    Load the data from the sensor_data.csv file inside /test/data/ for testing only.
    The loading uses Pandas. We crop all the columns but temperature, humidity and light_percentage.
    '''
    
    import pandas as pd
    
    pathToTestData = '/home/david/Documents/UNI_S.3/IoT/MedWay/test/data'
    
    data = pd.read_csv(pathToTestData, delimiter=',')
    # The format of the line will be ID,batch_number,device_number,date,temperature,humidity,light_percentage and ,state if the data is for training of the model

def trainAnalyzeState(period:str) -> None:
    '''
    Generate an analysis of the state of the batches of medicine included in the given period information. 
    The function pulls the data from the appropriate database, trains the model and exports it to a file.
    The model is given the name of the selected period, plus 'model' (e.g. dailyModel).
    '''
    
    '''
    1. Get the data
    2. Purge the data and split it
    3. Create the model and fit it
    Optional: evaluate the performance of the evaluation inline
    4. Export the model
    '''
    
    # Load the data by using the MySQL manager and separate it into X and y
    #X, y = ...
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create an XGBoost classifier
    model = XGBClassifier(objective="multi:softmax", num_class=3, seed=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")

def analyzeState(period:str) -> None:
    '''
    Use this function during deployment in order to use the generated model. Train and export the model using trainAnalyzeState(...).
    Specify the type of model to use. If the model is not trained, the function will raise an appropriate error.
    '''
    
    # Select the model from the files
    pass