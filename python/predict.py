import pandas as pd
import pickle
import numpy as np
import sys

predictfile_path = sys.argv[1]

predict_file = pd.read_csv(predictfile_path)
predict_file_og = predict_file

predict_file['Gender'].fillna(predict_file['Gender'].mode()[0], inplace=True)
predict_file['Self_Employed'].fillna(predict_file['Self_Employed'].mode()[0], inplace=True)
predict_file['Credit_History'].fillna(predict_file['Credit_History'].mode()[0], inplace=True)
predict_file['Loan_Amount_Term'].fillna(predict_file['Loan_Amount_Term'].mode()[0], inplace=True)
predict_file['Dependents'].fillna(predict_file['Dependents'].mode()[0], inplace=True)
predict_file['LoanAmount'].fillna(predict_file['LoanAmount'].median(),inplace=True)

predict_file['LoanAmount_log'] = np.log(predict_file['LoanAmount'])
predict_file['Total_Income']=predict_file['ApplicantIncome']+predict_file['CoapplicantIncome']
predict_file['EMI']=predict_file['LoanAmount']/predict_file['Loan_Amount_Term']
predict_file['Balanced_Income']=predict_file['Total_Income']-predict_file['EMI']
predict_file = predict_file.drop(['Loan_ID','LoanAmount','ApplicantIncome','CoapplicantIncome','Loan_Amount_Term'],axis=1)

predict_file = pd.get_dummies(predict_file)

model_path = 'Model/final_models/lr_model.sav'
model = pickle.load(open(model_path,'rb'))
prediction = model.predict(predict_file)

submission = pd.read_csv('Dataset/sample_submission_49d68Cx.csv')
submission['Loan_Status']=prediction
submission['Loan_ID']=predict_file_og['Loan_ID']

submission['Loan_Status'].replace(0,'N',inplace=True)
submission['Loan_Status'].replace(1,'Y',inplace=True)
mean_rows = int(submission.shape[0]/2)
predsplit_1 = submission.iloc[:mean_rows].to_json(orient='records')
predsplit_2 = submission.iloc[mean_rows:].to_json(orient='records')
complete_str = (predsplit_1+predsplit_2)
complete_str = complete_str.replace("][",",")
print(complete_str)
sys.stdout.flush()