# Analysis

The analysis of the data and prediction of the state of the medicines or vaccines is done by using XGboost.

XGBoost (Extreme Gradient Boosting) is a powerful machine learning algorithm known for its exceptional predictive performance. It's an ensemble learning method that combines the strengths of decision trees with a gradient boosting framework, making it highly efficient and accurate. XGBoost minimizes prediction errors by iteratively training weak decision tree models and adding them to an ensemble. It handles both regression and classification tasks, is resistant to overfitting, and allows fine-tuning of hyperparameters. XGBoost is widely used in various applications, such as data science competitions, financial modeling, and natural language processing, and is a popular choice for building robust machine learning models.

## Training and Testing

Use the following scripts to train the model on a large dataset and make necessary adjustments to achieve the desired performance with the data:

- Test data located in `../test/data/test_data.csv` can be used to verify the dimensionality and compatibility of the model with the data, but it should not be used for training.

- Utilize real or accurately simulated data within `./data` for training.

## Evaluation and Deployment

Use these scripts to evaluate the performance of the trained model. Some of the scripts are also designed for evaluating real data during deployment on AWS EC2 instances. This results in a streamlined version of the code, producing a model ready to be set up on the cloud.
