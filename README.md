<p align="center">
  <img src="./images/Medway2_slimSlim.png" width="1000">
</p>

# MedWay

MedWay: An IoT system for tracking medicines and vaccines from production to use, ensuring their safety and integrity, promoting global health security through transparency and accountability.

## Problem at hand

Ensuring the optimal preservation of medicines and vaccines necessitates strict control over various factors such as temperature and humidity. It is crucial to maintain these conditions to guarantee the products reach their final destination in optimal condition. For pharmaceuticals, particularly those from smaller organizations with limited budgets, effective regulation and tracking become essential to identify instances of mishandling and eliminate potentially compromised batches.

Our proposed system addresses the challenges associated with the mismanagement of vaccines and pharmaceutical drugs, especially prevalent in smaller organizations lacking extensive monitoring infrastructure for their cold chain.

The developed system offers a cost-effective and scalable solution for monitoring batch conditions during transportation. It generates insightful reports to assess potential issues in the transportation process, facilitating the identification and segregation of potentially compromised batches from the rest.

<p align="center">
We combine several technologies and tools in order to produce a valuable and useful system.
</p>

<p align="center">
<a href="https://www.python.org" target="_blank" rel="noreferrer">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" height="40"> 
</a>
<a href="https://aws.amazon.com/" target="_blank" rel="noreferrer">
<img src="./images/aws.png" alt="python" height="40"/> 
</a>
<a href="https://flet.dev/" target="_blank" rel="noreferrer">
<img src="https://res.cloudinary.com/practicaldev/image/fetch/s--C80QgetH--/c_fill,f_auto,fl_progressive,h_320,q_auto,w_320/https://dev-to-uploads.s3.amazonaws.com/uploads/user/profile_image/623522/e8798261-dd5f-44d2-a612-32cecae334b6.png" alt="python" height="40"/> 
</a>
<a href="https://platformio.org/" target="_blank" rel="noreferrer">
<img src="https://cdn.freebiesupply.com/logos/large/2x/platformio-logo-png-transparent.png" alt="python" height="40"/> 
</a>
<a href="https://xgboost.readthedocs.io/en/stable/#" target="_blank" rel="noreferrer">
<img src="./images/xgboost.png" alt="python" height="40"/> 
</a>
<a href="https://www.mysql.com/" target="_blank" rel="noreferrer">
<img src="https://1.bp.blogspot.com/-TNexKzkEY8M/Xk_d5jtWiAI/AAAAAAAAAqk/9GMEeX7Vuj8qK3YkOJHae3YHAzE1P-2PwCPcBGAYYCw/s1600/mysql-logo.png" alt="python" height="40"/>
</a>
</p>

<!-- <a target="_blank" rel="noopener noreferrer nofollow" href="https://camo.githubusercontent.com/2ecad22021fc13e37458a8d2b508a47352c096930f163927cb191353106f9309/68747470733a2f2f74656368737461636b2d67656e657261746f722e76657263656c2e6170702f646f636b65722d69636f6e2e737667">
<img src="https://camo.githubusercontent.com/2ecad22021fc13e37458a8d2b508a47352c096930f163927cb191353106f9309/68747470733a2f2f74656368737461636b2d67656e657261746f722e76657263656c2e6170702f646f636b65722d69636f6e2e737667" alt="icon" width="40" height="40">
</a> -->


## Subparts of the system

### Data acquisition

Explain the data acquisition module...

### Databases

There are two main types of databases used in this system. The main one is based on MySQL, and is made to be set up on AWS and on a local server. The second one is for storing the reports, result of the daily analysis of data; we use S3 AWS service for this purpose.

### Analysis

The data is analyzed using Lambda functions inside AWS, which run an XGBoost model created via Python. **XGBoost**, short for eXtreme Gradient Boosting, is a powerful and efficient machine learning algorithm that belongs to the ensemble learning category.

<p align="center">
  <img src="./images/xgboost_decisionTree.webp" width="400">
</p>

The model fits the dataset particularly well, as well as the decisions involved in analyzing the relationships between the main data points of temperature, humidity and UV-light, and its connection to the state of a batch of drugs. Since the connections between the conditions that the batch experiences and the state of the batch itself may be though as a decision tree, where one observes which conditions have been met and which have not, then XGBoost, apart from its robustness, is a good tool for the job.

<!-- Include image of the sensing module, once done -->

### Webapp

Describe the app...

## Quick-start guide

To be able to use the implementation developed in this repository you will need to do several things. 

1. Set up your AWS account with the appropriate connections between RDS, S3 and Lambda, in order to run everything on the cloud.

2. Build the physical sensor and receiving modules, from the provided diagram.

3. Install Python3 and all the requirements, via the following command:
```bash
pip3 install -r requirements.txt
```

4. (Optional) Download Flet to your phone (via [AppStore](https://apps.apple.com/mx/app/flet/id1624979699) or PlayStore) in order to be able to access the application from you mobile. Scan the following image to download the app:
<p align="center">
  <img src="./images/downloadFletQR.png" width="200">
</p>

5. Create `.env` files for saving your passwords and the rest of the variables necessary for connecting to the database services, something with the following type of format:
```python
CLOUD_HOST = 'aws.host.access_point/...'
CLOUD_USER = 'user'
CLOUD_PASSWORD = '123ABC'
# continue declaring the variables
```

6. Create the database for temporary data saving.

7. Create the necessary tables inside the two databases.
```bash
cd databases
python3 createSQL.py
```
8. Set up the WiFi connection to the sensing module and start pulling data. 

9. Wait for the main actions to occur, sending information to the cloud database, generating the reports and seeing the results via the web/mobile app.

To familiarize yourself with the whole system, use the tests inside the `./test/` directory. Also, use the tests to try your local set-up before trying to run the complete system.
