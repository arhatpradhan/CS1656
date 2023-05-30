import json
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
from sklearn import linear_model, tree, metrics
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Task(object):
    def __init__(self, bike_df, bank_df):
        np.random.seed(31415)
        self.bike_data = bike_df.sample(1000).copy()
        self.bank_data = bank_df.copy()

    def t1(self):
        train = self.bike_data.iloc[0:900]
        train_x = train[['weekday']].values
        train_y = train[['cnt']].values

        test=self.bike_data.iloc[900:]
        test_x = test[['weekday']].values
        test_y = test[['cnt']].values
        print (type(train_x), type(train_y), type(test_x), type(test_y))

        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(train_x, train_y)

        predict_y = regr.predict(test_x)
        # Printing  predicted and actual values side by side fro comparison
        np.column_stack((predict_y,test_y))

        mse = np.mean((predict_y - test_y) ** 2)
        return mse

    def t2_1(self):
        # Select all columns except 'instant'
        bike_data_filtered = self.bike_data.drop('instant', axis=1)

        # Split the data into training and testing sets
        train = bike_data_filtered.iloc[:900]
        test = bike_data_filtered.iloc[900:]

        # Extract the input features and target variable from the training set
        train_x = train.drop('cnt', axis=1).values
        train_y = train[['cnt']].values

        # Extract the input features and target variable from the testing set
        test_x = test.drop('cnt', axis=1).values
        test_y = test[['cnt']].values

        # Fit a linear regression model to the training data
        model = linear_model.LinearRegression()
        model.fit(train_x, train_y)

        # Use the model to make predictions on the testing data
        y_pred = model.predict(test_x)

        # Calculate the mean squared error
        mse = np.mean((y_pred - test_y) ** 2)

        return mse
        #comparing the 2 mse values it is better to use less attributes due to the lower mse values when using
        #fewer attributes
    
    def t3(self):
        #change male/female to numerical values
        self.bank_data['sex'] = self.bank_data['sex'].apply(lambda x: 1 if x == 'MALE' else 0)
        #change married to numerical values
        self.bank_data['married'] = self.bank_data['married'].apply(lambda x: 1 if x == 'YES' else 0)
        #change catagorical values to numerical values: "Town, Suburban, Inner_City, Rural"
        self.bank_data['region'] = pd.factorize(self.bank_data['region'])[0]

        dt_train_x = self.bank_data.iloc[:500][['region','sex','married']].values
        dt_train_y = self.bank_data.iloc[:500][['mortgage']].values

        dt_test_x = self.bank_data.iloc[500:][['region','sex','married']].values
        dt_test_y = self.bank_data.iloc[500:][['mortgage']].values

        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(dt_train_x, dt_train_y)

        dt_predict_y = clf.predict(dt_test_x)

        accuracy = metrics.accuracy_score(dt_test_y,dt_predict_y)
        
        return accuracy

if __name__ == "__main__":
    t = Task(pd.read_csv('http://data.cs1656.org/bike_share.csv'), pd.read_csv('http://data.cs1656.org/bank-data.csv'))
    print("---------- Task 1 ----------")
    print(t.t1())
    print("--------- Task 2.1 ---------")
    print(t.t2_1())
    print("---------- Task 3 ----------")
    print(t.t3())
