# Analysis

The analysis of the data and prediction of the state of the medicines or vaccines is done by using XGboost.

XGBoost (Extreme Gradient Boosting) is a powerful machine learning algorithm known for its exceptional predictive performance. It's an ensemble learning method that combines the strengths of decision trees with a gradient boosting framework, making it highly efficient and accurate. XGBoost minimizes prediction errors by iteratively training weak decision tree models and adding them to an ensemble. It handles both regression and classification tasks, is resistant to overfitting, and allows fine-tuning of hyperparameters. XGBoost is widely used in various applications, such as data science competitions, financial modeling, and natural language processing, and is a popular choice for building robust machine learning models.

## Training and Testing

Use the following scripts to train the model on a large dataset and make necessary adjustments to achieve the desired performance with the data:

- Test data located in `../test/data/test_data.csv` can be used to verify the dimensionality and compatibility of the model with the data, but it should not be used for training.

- Utilize real or accurately simulated data within `./data` for training.


## Generating a report

In order to generate a report and save it into the appropiate folder, use the following line from the terminal when inside the templates directory:
```bash
pdflatex  -shell-escape -output-directory=../reports/ dailyReportTemplate.tex
```
And in order to delete all the extra files that are generated as output, logs, etc. from the compilation, use:
```bash
rm dailyReportTemplate.aux dailyReportTemplate.log dailyReportTemplate.out
# or
rm ../reports/dailyReportTemplate.aux ../reports/dailyReportTemplate.log ../reports/dailyReportTemplate.out
```

## Evaluation and Deployment

Use these scripts to evaluate the performance of the trained model. Some of the scripts are also designed for evaluating real data during deployment on AWS EC2 instances. This results in a streamlined version of the code, producing a model ready to be set up on the cloud.

---

# Notes to the developer

Things to do for evaluation of the values in Medway:

1. Build the simple model for classification, that considers temperature, humidity, light percentage.

The idea is to build a model that is able to make a good classification for each of the lines of data.
The model gives a binary prediction, trying to determine if the medicine is still in good condition, given the conditions it has gone through.
For each batch, we run the model on each line and if there are more than 20 readings that trigger a classification of BAD, then we consider the batch to be
	have gone bad, or to require further revision and separation from the rest.
	
The alerts are not used for the classification, but only for generating meaningful reports.

After the evaluation of each batch, the number is saved temporarly, some other statistics are run, and we generate the report from the template.
	(once the report is generated and saved, the temp. data is deleted, and the classification does not trigger until after 24 hrs)
	
 