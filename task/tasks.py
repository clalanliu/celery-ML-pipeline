from .worker import app
from celery.utils.log import get_task_logger
from celery.utils.log import get_task_logger
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split    #the tool for split the data 
from sklearn.linear_model import  LinearRegression      #and because we know we going to use linear regression for our prediction we import the class as well 
from sklearn.metrics import r2_score
import time
# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

@app.task(name='task.train_model')
def train_model(test_size):
    run_training(test_size)
    celery_log.info(f"Celery task completed!")
    return 'OK'



# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

def run_training(test_size):
    iris = datasets.load_iris()
    celery_log.info(f"Data prepared")
    print("here")
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.DataFrame(iris.target, columns=['target'])
    X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 0.20)
    lr = LinearRegression() 
    print("Sleeping ...")
    time.sleep(30)
    iris_model = lr.fit(X_train, y_train)
    predictions = iris_model.predict(X_test)

    #over here we split the data. into the x&y trainer and y&x tester
    r2 = r2_score(y_test, predictions)
    
    celery_log.info(f'r2 score: {r2}')
    celery_log.info('Training task completed')