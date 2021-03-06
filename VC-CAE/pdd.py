# -*- coding: utf-8 -*-
"""PDD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x7uCvijJIYuoNQBrOHbXqq8SCYoapDY_

# **Parkinson Disease Detection using a Convolutional Autoencoder with a SLM**

## **GPU**
"""

'''from IPython.display import HTML, clear_output
from subprocess import getoutput
s = getoutput('nvidia-smi')
if 'K80' in s:gpu = 'K80'
elif 'T4' in s:gpu = 'T4'
elif 'P100' in s:gpu = 'P100'
elif 'P4' in s:gpu = 'P4'
display(HTML(f"<h1>{gpu}</h1>"))'''

"""## **Libraries**"""

import pandas as pd # Library to process the dataframe
import numpy as np # Library to handle with numpy arrays
import warnings # Library that handles all the types of warnings during execution
import matplotlib.pyplot as plt# Library that handles ploting of  the graphs
from sklearn.model_selection import train_test_split
warnings.filterwarnings("ignore") # Ignore all the warnings

"""## **Data Preprocessing**"""

df=pd.read_csv('parkinsons.csv')
df=df.dropna(how='any')
df['MDVP:Avg(Hz)']=(df['MDVP:Fhi(Hz)']+df['MDVP:Flo(Hz)'])/2
df['Shimmer:APQ(Avg)']=(df['Shimmer:APQ3']+df['Shimmer:APQ3'])/2
df['NR(Avg)']=(df['NHR']+df['HNR'])/2
df['Disease']=df['status']
df=df.drop(columns=['name','status'])
df

lst=[df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df,df]
Df=pd.concat(lst)
Df=Df.reset_index(drop=True)

Df

X=Df.iloc[:,:-1].values
Y=Df.iloc[:,-1].values

X

Y

#Splitting training and testing dataset
ts=0.25
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=ts, random_state=42,shuffle=True)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

X_train = X_train.reshape(X_train.shape[0],5,5,1)
X_test = X_test.reshape(X_test.shape[0],5,5,1)

X_train.shape

"""## **Convolutional AutoEncoder**"""

from tensorflow.keras import layers 
import keras

input_shape = keras.Input(shape=(5,5,1))

x = layers.Conv2D(25, (1, 1), activation='relu', padding='same')(input_shape)
x = layers.MaxPooling2D((1, 1), padding='same')(x)
x = layers.Conv2D(15, (1, 1), activation='relu', padding='same')(x)
x = layers.MaxPooling2D((1, 1), padding='same')(x)
x = layers.Conv2D(5, (1,1), activation='relu', padding='same')(x)
encoded = layers.MaxPooling2D((1,1), padding='same')(x)

# at this point the representation is (5, 5, 1) 

x = layers.Conv2D(5, (1, 1), activation='relu', padding='same')(encoded)
x = layers.UpSampling2D((1, 1))(x)
x = layers.Conv2D(15, (1, 1), activation='relu', padding='same')(x)
x = layers.UpSampling2D((1, 1))(x)
x = layers.Conv2D(25, (1, 1), activation='relu')(x)
x = layers.UpSampling2D((1, 1))(x)
decoded = layers.Conv2D(1, (1, 1), activation='softmax', padding='same')(x)

autoencoder = keras.Model(input_shape, decoded)
autoencoder.compile(optimizer='adam', loss='categorical_crossentropy',metrics=['accuracy'])
encoder = keras.Model(input_shape, encoded)
encoder.save('CAE-Sm.h5')

hist=autoencoder.fit(X_train, X_train, epochs=1000,batch_size=128,shuffle=True,validation_data=(X_test, X_test))

plt.plot(hist.history['accuracy'], label='train')
plt.plot(hist.history['val_accuracy'], label='test')
plt.xlabel('Epochs--->')
plt.ylabel('Accuracy--->')
plt.title('Accuracy Chart')
plt.legend()

plt.plot(hist.history['loss'], label='train')
plt.plot(hist.history['val_loss'], label='test')
plt.xlabel('Epochs--->')
plt.ylabel('Loss--->')
plt.title('Loss Chart')
plt.legend()

"""### **Model Libraries**"""

from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from xgboost import XGBClassifier
from tensorflow.keras.models import load_model
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import RidgeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import StackingClassifier
import pickle

"""### **Model Metrics**"""

from sklearn.metrics import accuracy_score
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import f1_score
from sklearn.metrics import hamming_loss
from sklearn.metrics import jaccard_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

"""## **Superlearner Model Layout**"""

models = list()
models.append(('LogR',LogisticRegression(solver='liblinear')))
models.append(('PC',Perceptron()))
models.append(('PAC',PassiveAggressiveClassifier()))
models.append(('RIC',RidgeClassifier()))
models.append(('RC',RandomForestClassifier(n_estimators=250)))
models.append(('EXTC',ExtraTreesClassifier(n_estimators=250)))
models.append(('XGBC',XGBClassifier()))
models.append(('MLPC',MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, learning_rate='adaptive', max_iter=750)))

# meta model
meta = XGBClassifier()

#Splitting training and testing dataset
ts=0.25
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=ts, random_state=42,shuffle=True)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

X_train = X_train.reshape(X_train.shape[0],5,5,1)
X_test = X_test.reshape(X_test.shape[0],5,5,1)

"""### **Model Training/Validation**"""

#model = StackingClassifier(estimators=models, final_estimator=meta, cv=25)
model = VotingClassifier(estimators = models, voting ='hard')
encoder = load_model('CAE-Sm.h5')
print('Train', X_train.shape, y_train.shape, 'Test', X_test.shape, y_test.shape)
X_train_encode = encoder.predict(X_train)
X_test_encode = encoder.predict(X_test)
print(X_train_encode.shape)
print(X_test_encode.shape)
X_train=np.reshape(X_train_encode,(-1,125))
X_test = np.reshape(X_test_encode,(-1,125))
model.fit(X_train,y_train)
#score=model.score(X_test_encode,y_test)
filename = 'SLM.h5'
pickle.dump(model, open(filename, 'wb'))
print("Model saved succesfully!!!")
loaded_model = pickle.load(open(filename, 'rb'))
print("Loaded Model Sucessfully")
result = loaded_model.score(X_test, y_test)
print('Super learner model score: %.3f'%(result*100))
yhat = loaded_model.predict(X_test)
print('Super Learner: %.3f' % (accuracy_score(y_test, yhat) * 100))

loaded_model = pickle.load(open(filename, 'rb'))
print("Loaded Model Sucessfully")
yhat = loaded_model.predict(X_test)

y_test

yhat

"""### **Model Score Analysis**"""

print("\n Score Metrics:")
print('\n Accuracy score:', round(accuracy_score(y_test, yhat) * 100))
print('\n Balanced Accuracy score' ,round(balanced_accuracy_score(y_test, yhat) * 100))
print('\n Cohen Kappa score' ,round(cohen_kappa_score(y_test, yhat) * 100))
print('\n F1 Score (Macro):' ,round(f1_score(y_test, yhat,average='macro') * 100))
print('\n F1 Score (Micro):' ,round(f1_score(y_test, yhat,average='micro') * 100))
print('\n F1 Score (Weighted):' ,round(f1_score(y_test, yhat,average='weighted') * 100))
print('\n Jaccard Score (Macro):' ,round(jaccard_score(y_test, yhat,average='macro') * 100))
print('\n Jaccard Score (Micro):' ,round(jaccard_score(y_test, yhat,average='micro') * 100))
print('\n Jaccard Score (Weighted):' ,round(jaccard_score(y_test, yhat,average='weighted') * 100))
print("\n Loss Metrics:")
print('\n Hamming Loss :' ,hamming_loss(y_test, yhat))
print("\n Confusion matrix")
print('\n')
print(confusion_matrix(y_test,yhat))
print('\n')