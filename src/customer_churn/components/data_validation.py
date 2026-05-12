import pandas as pd
df = pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df.head())