# Library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from shutil import copyfile
from sklearn import tree

score_lst = []
score_file = open("Model/Decision_Tree/DTree_model_file.txt","w")

warnings.filterwarnings("ignore")

# Reading the train and test file 
train = pd.read_csv('Dataset/train_ctrUa4K.csv')
test = pd.read_csv('Dataset/test_lAUu6dG.csv')

train_og = train
test_og = test

# Filtering Loan defaulters

new_dataset = train[train['Loan_Status']=='N']
print(new_dataset)

# Checking for missing values in train dataset
train['Gender'].fillna(train['Gender'].mode()[0], inplace=True)
train['Married'].fillna(train['Married'].mode()[0], inplace=True)
train['Self_Employed'].fillna(train['Self_Employed'].mode()[0], inplace=True)
train['Credit_History'].fillna(train['Credit_History'].mode()[0], inplace=True)
train['Dependents'].fillna(train['Dependents'].mode()[0], inplace=True)
train['Loan_Amount_Term'].fillna(train['Loan_Amount_Term'].mode()[0],inplace=True)

train['LoanAmount'].fillna(train['LoanAmount'].median(),inplace=True)

# Checking for missing values in test dataset
test['Gender'].fillna(test['Gender'].mode()[0], inplace=True)
test['Self_Employed'].fillna(test['Self_Employed'].mode()[0], inplace=True)
test['Credit_History'].fillna(test['Credit_History'].mode()[0], inplace=True)
test['Loan_Amount_Term'].fillna(test['Loan_Amount_Term'].mode()[0], inplace=True)
test['Dependents'].fillna(test['Dependents'].mode()[0], inplace=True)

test['LoanAmount'].fillna(test['LoanAmount'].median(),inplace=True)

# Smooting out the data curve 
train['LoanAmount_log'] = np.log(train['LoanAmount'])
test['LoanAmount_log'] = np.log(test['LoanAmount'])

# Adding more features/details about applicants
train['Total_Income']=train['ApplicantIncome']+train['CoapplicantIncome']
test['Total_Income']=test['ApplicantIncome']+test['CoapplicantIncome']

train['EMI']=train['LoanAmount']/train['Loan_Amount_Term']
test['EMI']=test['LoanAmount']/test['Loan_Amount_Term']

train['Balanced_Income']=train['Total_Income']-train['EMI']
test['Balanced_Income']=test['Total_Income']-test['EMI']

# Building a Model
train = train.drop(['Loan_ID','LoanAmount','ApplicantIncome','CoapplicantIncome','Loan_Amount_Term'],axis=1)
test = test.drop(['Loan_ID','LoanAmount','ApplicantIncome','CoapplicantIncome','Loan_Amount_Term'],axis=1)

X = train.drop('Loan_Status',axis=1)
Y = train.Loan_Status

X = pd.get_dummies(X)
train = pd.get_dummies(train)
test = pd.get_dummies(test)

# creating a model from already existing data of 
for i in range (100):
    x_train, x_cv, y_train, y_cv = train_test_split(X,Y,test_size=0.3)
    model_rfc = tree.DecisionTreeClassifier(random_state=1)
    model_rfc.fit(x_train,y_train)
    pred_cv = model_rfc.predict(x_cv)
    score=accuracy_score(y_cv,pred_cv)
    score_lst.append(score)
    path = ('Model/Decision_Tree/dTree_model_'+str(i)+'.sav')
    pickle.dump(model_rfc,open(path,"wb"))
    print(i+1,'of 5')
    print(score)
    score_file.write(str(i+1)+' of 100 : '+str(score)+"\n")



print("\nMax Score: "+str(max(score_lst))+"\nMin Score: "+str(min(score_lst))+"\nMean Score: "+str(sum(score_lst)/len(score_lst))+'\nBest Model: dTree_model_'+str(score_lst.index(max(score_lst))))
score_file.write("\n\nMax Score: "+str(max(score_lst))+"\nMin Score: "+str(min(score_lst))+"\nMean Score: "+str(sum(score_lst)/len(score_lst))+'\nBest Model: dTree_model_'+str(score_lst.index(max(score_lst))))
src = ('Model/Decision_Tree/dTree_model_'+str(score_lst.index(max(score_lst)))+'.sav')
dst = ('Model/final_models/dTree_model.sav')
copyfile(src,dst)