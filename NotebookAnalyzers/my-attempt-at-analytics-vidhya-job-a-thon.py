#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # **Rank in top 15% on Private Leader Board**

# ### Hope This Notebook Helps others prepare for the same 

# In[2]:


import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# pd.set_option('display.max_rows',None)
# pd.set_option('display.max_columns',None)

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import roc_auc_score


# In[3]:


train=pd.read_csv('/kaggle/input/jobathon-analytics-vidhya-health-insurance/Train.csv')
test=pd.read_csv('/kaggle/input/jobathon-analytics-vidhya-health-insurance/Test.csv')
sub=pd.read_csv('/kaggle/input/jobathon-analytics-vidhya-health-insurance/sample_submission.csv')


# In[4]:


sub.head()


# In[5]:


train.head()


# In[6]:


train['Diff']=train['Upper_Age']-train['Lower_Age']
test['Diff']=test['Upper_Age']-test['Lower_Age']

def set_range_age(x):
    if(x<15):
        return 1
    elif((x>=15) and (x<30)):
        return 2
    elif(x>=30 and x<45):
        return 3
    elif(x>=45):
        return 4
    
train['New']=train['Diff'].apply(set_range_age)
test['New']=test['Diff'].apply(set_range_age)


# In[7]:


train['New'].value_counts()


# In[8]:


train.isnull().sum()


# In[9]:


len(train)


# In[10]:


a = train.isnull().sum()/len(train)*100
a[a>0]


# In[11]:


a = test.isnull().sum()/len(test)*100
a[a>0]


# In[12]:


train.describe()


# In[13]:


train.info()


# In[14]:


train.columns


# In[15]:


print(len(train))


# In[16]:


for i in train.columns:
    print(f'Column :{i} Number of unique columns:{train[i].nunique()}')  


# In[17]:


plt.figure(figsize=(12,7))
sns.countplot(train['City_Code'])


# In[18]:


train['City_Code'].nunique()


# In[19]:


train['City_Code'].value_counts()


# In[20]:


# train['Region_Code'].value_counts()


# In[21]:


plt.figure(figsize=(10,7))
sns.distplot(train['Upper_Age'])


# In[22]:


plt.figure(figsize=(10,7))
sns.distplot(train['Lower_Age'])


# In[23]:


train['Health Indicator'].value_counts()


# In[24]:


train.groupby('City_Code')['Health Indicator'].value_counts()


# c28=x2
# c31=x2
# c35=x3
# c36=x2

# In[25]:


def set_health_indicator(x):
    city=x[0]
    health=x[1]
    if pd.isnull(health):
        if (city=='C28') | (city=='C31') | (city=='C36'):
            return 'X2'
        elif city=='C35':
            return 'X3'
        else:
            return 'X1'
    else:
        return health
train['Health Indicator']=train[['City_Code','Health Indicator']].apply(set_health_indicator,axis=1)
test['Health Indicator']=test[['City_Code','Health Indicator']].apply(set_health_indicator,axis=1)


# In[26]:


train.isnull().sum()


# In[27]:


train['Holding_Policy_Duration'].value_counts()


# In[28]:


train.isnull().sum()


# In[29]:


train['Holding_Policy_Duration']=train['Holding_Policy_Duration'].apply(lambda x:15.0 if x =='14+' else float(x))
test['Holding_Policy_Duration']=test['Holding_Policy_Duration'].apply(lambda x:15.0 if x =='14+' else float(x))


# In[30]:


train['Holding_Policy_Duration'].value_counts()


# In[31]:


train['Holding_Policy_Duration'].describe()


# In[32]:


# train['Holding_Policy_Duration'].fillna(5.0,inplace=)


# In[33]:


train['Holding_Policy_Duration'].fillna(5.0,inplace=True)
test['Holding_Policy_Duration'].fillna(5.0,inplace=True)


# In[34]:


train.isnull().sum()


# In[35]:


train['Holding_Policy_Type'].value_counts()


# In[36]:


train.groupby('City_Code')['Holding_Policy_Type'].value_counts().head()


# In[37]:


list_city=['c12','c15','c17','c18','c19','c24']
def set_Holding_Policy(x):
    city=x[0]
    policy=x[1]
    if pd.isnull(policy):
        if (city in list_city):
            return 1
        else:
            return 3
    return policy
train['Holding_Policy_Type']=train[['City_Code','Holding_Policy_Type']].apply(set_Holding_Policy,axis=1)
test['Holding_Policy_Type']=test[['City_Code','Holding_Policy_Type']].apply(set_Holding_Policy,axis=1)


# In[38]:


train.info()


# In[39]:


train['Response'].value_counts()


# In[40]:


for i in train.columns:
    print(f'Column :{i} Number of unique columns:{train[i].nunique()}')  


# In[ ]:





# In[41]:


train.head()


# In[42]:


plt.figure(figsize=(10,6))
sns.heatmap(train.corr(),cmap='coolwarm')


# In[43]:


columns_to_drop=['ID','Region_Code','Reco_Policy_Premium','Diff','Upper_Age','Lower_Age']
dummies_columns=['City_Code','Accomodation_Type','Reco_Insurance_Type','Is_Spouse'
                 ,'Holding_Policy_Type','Reco_Policy_Cat']
label_encode=['Health Indicator']


# In[44]:


# train[(train['Is_Spouse']=='Yes')&(train['Reco_Insurance_Type']=='Individual')]


# In[45]:


# a=train[(train['Is_Spouse']=='No')&(train['Reco_Insurance_Type']=='Joint')].index
# train.drop(a,inplace=True)


# In[46]:


train.drop(columns=columns_to_drop,inplace=True)
test.drop(columns=columns_to_drop,inplace=True)


# In[47]:


train_1=train.copy()
train_1=pd.get_dummies(train_1,drop_first=True,columns=dummies_columns)
test_1=test.copy()
test_1=pd.get_dummies(test_1,drop_first=True,columns=dummies_columns)

le=LabelEncoder()
for col in label_encode:
    train_1[col]=le.fit_transform(train_1[col])
    test_1[col]=le.transform(test_1[col])


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# In[48]:


train_1.shape


# In[49]:


X=train_1.drop(columns=['Response'])
y=train_1['Response']


# In[50]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


# In[51]:


scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)
test_1=scaler.transform(test_1)


# In[52]:


# cvs_random=cross_val_score(RandomForestClassifier(),X=X_train,y=y_train,cv=5,scoring='accuracy')
# print(cvs_random.mean())
# print(cvs_random.std())


# In[53]:


# cvs_random=cross_val_score(DecisionTreeClassifier(),X=X_train,y=y_train,cv=5,scoring='accuracy')
# print(cvs_random.mean())
# print(cvs_random.std())


# In[54]:


# cvs_random=cross_val_score(LogisticRegression(),X=X_train,y=y_train,cv=5,scoring='accuracy')
# print(cvs_random.mean())
# print(cvs_random.std())


# In[55]:


# cvs_random=cross_val_score(XGBClassifier(),X=X_train,y=y_train,cv=5)
# print(cvs_random.mean())
# print(cvs_random.std())


# In[56]:


# sm = SMOTE(random_state = 2) 
# X_train_res, y_train_res = sm.fit_resample(X_train, y_train.ravel()) 

# model=LogisticRegression(solver="liblinear")

# model.fit(X_train_res,y_train_res)
# pred_logistic=model.predict_proba(X_test)[:, 1]

# roc_auc_score(y_test,pred_logistic)


# In[57]:


# model=LogisticRegression(solver="liblinear")

# model.fit(X_train,y_train)
# pred_logistic=model.predict_proba(X_test)[:, 1]

# roc_auc_score(y_test,pred_logistic)


# In[58]:


# model=RandomForestClassifier()

# model.fit(X_train,y_train)
# pred_random=model.predict_proba(X_test)[:, 1]

# roc_auc_score(y_test,pred_random)


# In[59]:


# model=DecisionTreeClassifier()

# model.fit(X_train,y_train)
# pred_decision=model.predict_proba(X_test)[:, 1]

# roc_auc_score(y_test,pred_decision)


# In[60]:


# test_predictions=model.predict_proba(test_1)[:, 1]

# sub['Response']=test_predictions

# sub.to_csv('JOB-A-THON-LOGISTICS(PREDICTIONS)-1.csv',index=False)


# In[61]:


# from sklearn.model_selection import GridSearchCV
# param_test1 = {'n_estimators':range(20,81,10)}
# gsearch1 = GridSearchCV(estimator = XGBClassifier(learning_rate=0.1, min_samples_split=500,min_samples_leaf=50,max_depth=8,max_features='sqrt',subsample=0.8,random_state=10), 
# param_grid = param_test1, scoring='roc_auc',n_jobs=4, cv=5)
# gsearch1.fit(X_train,y_train)


# In[62]:


# gsearch1.get_params, gsearch1.best_params_, gsearch1.best_score_


# In[63]:


# from sklearn.model_selection import RandomizedSearchCV
# from sklearn.model_selection import StratifiedKFold
# params = {
#         'min_child_weight': [1, 5, 10],
#         'gamma': [0.5, 1, 1.5, 2, 5],
#         'subsample': [0.6, 0.8, 1.0],
#         'colsample_bytree': [0.6, 0.8, 1.0],
#         'max_depth': [3, 4, 5]
#         }
# xgb = XGBClassifier(learning_rate=0.02, n_estimators=600, objective='binary:logistic',
#                     silent=True, nthread=1)
# folds = 3
# param_comb = 5

# skf = StratifiedKFold(n_splits=folds, shuffle = True, random_state = 1001)

# random_search = RandomizedSearchCV(xgb, param_distributions=params, n_iter=param_comb, scoring='roc_auc', n_jobs=4, cv=skf.split(X_train,y_train), verbose=3, random_state=1001 )

# # Here we go
# # start_time = timer(None) # timing starts from this point for "start_time" variable
# random_search.fit(X_train, y_train)
# # timer(start_time) # timing ends here for "start_time" variable

# random_search.best_params_


# In[64]:


xgb1 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=1000,
 max_depth=5,
 min_child_weight=1,
 gamma=1.5,
 subsample=0.6,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)
xgb1.fit(X_train,y_train)

# model=XGBClassifier()

xgb1.fit(X_train,y_train)
pred_xgb=xgb1.predict_proba(X_test)[:, 1]

roc_auc_score(y_test,pred_xgb)


# In[65]:


# train[train['Diff']>0]['Diff'].describe()


# In[66]:


# train['Diff']=train['Upper_Age']-train['Lower_Age']
# pd.cut(train['Diff'],bins=4)


# In[67]:


# param_test1 = {
#  'max_depth':range(3,10,2),
#  'min_child_weight':range(1,6,2)
# }
# gsearch1 = GridSearchCV(estimator = XGBClassifier( learning_rate =0.1, n_estimators=140, max_depth=5,
#  min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
#  objective= 'binary:logistic', nthread=4, scale_pos_weight=1, seed=27), 
#  param_grid = param_test1, scoring='roc_auc',n_jobs=4, cv=5)
# gsearch1.fit(X_train,y_train)
# gsearch1.best_estimator_, gsearch1.best_params_, gsearch1.best_score_


# In[68]:


# sm = SMOTE(random_state = 2) 
# X_train_res, y_train_res = sm.fit_resample(X_train, y_train.ravel()) 
# from imblearn.under_sampling import NearMiss 
# nr = NearMiss() 
  
# X_train_res, y_train_res = nr.fit_resample(X_train, y_train.ravel())

# model=XGBClassifier()

# model.fit(X_train_res,y_train_res)
# pred_xgb=model.predict_proba(X_test)[:, 1]

# roc_auc_score(y_test,pred_xgb)


# In[69]:


# model.predict_proba(test_1)[:,1]


# In[70]:


test_predictions=xgb1.predict_proba(test_1)[:, 1]

sub['Response']=test_predictions

sub.to_csv('JOB-A-THON-XGB(PREDICTIONS)-1.csv',index=False)


# In[71]:


sub


# In[ ]:





# In[ ]:




