# Import necessary libraries
import xgboost as xgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

def createModel(X_train, X_test, y_train, y_test) -> None:
    # Create an XGBoost classifier
    model = xgb.XGBClassifier(objective="multi:softmax", num_class=3, seed=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")

    with open('test_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
        
def useModel(X_test, y_test) -> None:
    try:
        with open('test_model.pkl', 'rb') as model_file:
            loaded_model = pickle.load(model_file)
    except:
        print('There is no model to import and use. Train one.')
        
    # Make predictions on the test set
    y_pred = loaded_model.predict(X_test)

    # Evaluate the model accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy during loading: {accuracy * 100:.2f}%")
        

if __name__ == '__main__':
    # Load the Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create the model
    createModel(X_train, X_test, y_train, y_test)
    
    # Load and use the model again
    useModel(X_test, y_test)
    