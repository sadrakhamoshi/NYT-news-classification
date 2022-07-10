# -*- coding: utf-8 -*-
"""FinalPhase.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K8QuFBG7X_jv6OEVWLRy_chCu7eeI2__

# imports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
import tensorflow as tf
from tensorflow import keras
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
!pip install plot-keras-history
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
import seaborn as sns
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from plot_keras_history import plot_history
from sklearn.metrics import confusion_matrix

a = [1,2,3,4]
b = [8,7,6,5]
f, x = shuffle(a, b)
f, x

from google.colab import drive
drive.mount('/content/drive')

"""# Load Data

## NYT news Data

In this cell we try to use the data which we prepared in previos phase of project. it is an news dataset from New York Times news different section.
"""

nyt_data_path = '/content/drive/MyDrive/nlp/cleaned_news.csv'

df = pd.read_csv(nyt_data_path)
df.head()

nyt_news = df['news'].values
nyt_cat = df['category'].values
nyt_news.shape, nyt_cat.shape

nyt_category_str = np.unique(nyt_cat)
cat_to_index = {val:idx for idx, val in enumerate(nyt_category_str)}
NYT_CLASS_NUMBERS = len(nyt_category_str)
print(cat_to_index), len(nyt_category_str)

nyt_y = np.array([cat_to_index.get(key) for key in nyt_cat])
nyt_y.shape

np.unique(nyt_y)

"""` DATA Visualization `"""

plt.figure(figsize=(14,8))
count = df.category.value_counts()
sns.barplot(x=count.index, y=count)
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=90);

## The maximum number of words to be used. (most frequent)
MAX_NB_WORDS = 20000

## Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 150

## This is fixed.
EMBEDDING_DIM = 100


tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
# tokenizer.fit_on_texts(news_con)

## for nyt
tokenizer.fit_on_texts(nyt_news)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

## for NYT
X = tokenizer.texts_to_sequences(nyt_news)

X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)

## NYT
y = tf.keras.utils.to_categorical(nyt_y)

print('Shape of data input tensor:', X.shape)
print('Shape of target class tensor:', y.shape)

"""## Ag News

This cell is for using AG news which you can find it data in [kaggle](https://www.kaggle.com/datasets/amananandrai/ag-news-classification-dataset).
"""

TRAIN_DATA_PATH = '/content/drive/MyDrive/Ag_news_dataset/cleaned_train_data.csv'
TEST_DATA_PATH = '/content/drive/MyDrive/Ag_news_dataset/cleaned_test_data.csv'

df = pd.read_csv(TRAIN_DATA_PATH)
df_test = pd.read_csv(TEST_DATA_PATH)
df.head()

"""we seperate the content of the news and it's category."""

news_train = df['description'].tolist()
news_test = df_test['description'].tolist()

categories_train = df['category'].tolist()
categories_test = df_test['category'].tolist()

print(len(news_train), len(news_test))
print(len(categories_train), len(categories_test))

"""here we tokenize each news by whitespaces.  
`NOTE : Our data was preprocessed before in the previous phase of project` 
"""

tokenized_news = [a.split(' ') for a in news_train]
print(tokenized_news[10])

"""`this cell is just for AG news dataset`  
in here we concatenate train and test data to get the whole of data and vectorize seprate it for our model.
"""

# concatenate news train and test
news_con = np.array(news_train + news_test)
categories_con = np.array(categories_train + categories_test, dtype=np.float32)

news_con.shape, categories_con.shape, categories_train[:120000] == categories_con[:120000]

"""we shuffle our data with sklearn library"""

# shuffle data
news_con, categories_con = shuffle(news_con, categories_con, random_state=13)

"""in the below cell you can check out the visualization of our AG news data."""

df_all = pd.concat([df, df_test])
plt.figure(figsize=(14,8))
count = df_all.category.value_counts()
sns.barplot(x=count.index, y=count)
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=90);

""" in the following cell, we use keras library to tokenize our news and create vectorization from them. The Tokenizer class allows to vectorize a text corpus and after we use this vectorezie to a embedding layer."""

## The maximum number of words to be used. (most frequent)
MAX_NB_WORDS = 20000

## Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 250

## This is fixed.
EMBEDDING_DIM = 100


tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
tokenizer.fit_on_texts(news_con)

## for Ag
tokenizer.fit_on_texts(news_con)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

"""1. In the below cell, we convert each news to its vectorize representation.  
2. also we add 0 padding to reach the maximum size of a sentence.
3. next we convert the true labels to the categorical one since we have classification task and we are going to use binary cross entropy for classification. 
"""

X = tokenizer.texts_to_sequences(news_con)

X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)

class_num = len(np.unique(categories_con))

## conver the target class co categorical.
y = tf.keras.utils.to_categorical(categories_con - 1, num_classes= class_num)

print('Shape of data input tensor:', X.shape)
print('Shape of target class tensor:', y.shape)

"""## Break News Category Dataset

This data set is taken from [kaggle](https://www.kaggle.com/datasets/rmisra/news-category-dataset)
"""

! pip install kaggle

! mkdir ~/.kaggle

! cp kaggle.json ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

! kaggle datasets download -d rmisra/news-category-dataset

! unzip news-category-dataset.zip

! cp News_Category_Dataset_v2.json /content/drive/MyDrive/nlp/

"""### visualize data"""

data_path = '/content/drive/MyDrive/nlp/News_Category_Dataset_v2.json'
df = pd.read_json(data_path, lines=True)
df.head()

df['category'].value_counts()

plt.figure(figsize=(14,8))
count = df.category.value_counts()
sns.barplot(x=count.index, y=count)
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=90);

LABEL_USED_COUNT = 12
label_used = df.category.value_counts().index[:LABEL_USED_COUNT]
print('label used for prediction the {}'.format(label_used))

df['text'] = df['headline'] +'. ' +df['short_description']
df_v2 = df[['text', 'category']]
df_v2.head()

df_top_category = df_v2[df_v2['category'].isin(label_used)]
df_top_category['category'].value_counts()

df_top_category.to_csv('/content/drive/MyDrive/nlp/Breaking_News_Top.csv')

## get the cleaned data
df_clean = pd.read_csv('/content/drive/MyDrive/nlp/cleaned_Breaking_News_Top.csv')
df_clean.head()

byn_news = df_clean['news'].values
byn_cat = df_clean['category'].values
byn_news.shape, byn_cat.shape

byn_category_str = np.unique(byn_cat)
cat_to_index = {val:idx for idx, val in enumerate(byn_category_str)}
BYN_CLASS_NUMBERS = len(byn_category_str)
print(cat_to_index), len(byn_category_str)

byn_y = np.array([cat_to_index.get(key) for key in byn_cat])
byn_y.shape

## The maximum number of words to be used. (most frequent)
MAX_NB_WORDS = 20000

## Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 150

## This is fixed.
EMBEDDING_DIM = 100

tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)

## for byn
tokenizer.fit_on_texts(byn_news)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

## for BYN
X = tokenizer.texts_to_sequences(byn_news)

X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)

## BYN
y = tf.keras.utils.to_categorical(byn_y)

print('Shape of data input tensor:', X.shape)
print('Shape of target class tensor:', y.shape)

"""## Create ataset

here we splite the train and the test data which `0.2` of them are for test-data and the rest is for train-data.
"""

# seperate the test and train data
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

"""# Section `2`

## build model

### For AG news

here we build our model with sequential and embedding layers.
also we use some dropout to almost make sure that we won't face overfitting.
"""

from keras.layers.core.dropout import Dropout
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=X.shape[1]),
    SpatialDropout1D(0.2),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, recurrent_regularizer='l1_l2')),
    Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(4)
])

"""`
{
  "optimizer": "adam",
  "loss function": "binary cross entropy",
  "epochs": 10
}
`
"""

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=['accuracy'])
print(model.summary())

"""Train our model with batch_size 512 and validation data."""

history = model.fit(X_train , Y_train, epochs=10,batch_size=512,
                    validation_data=(X_test, Y_test))

# save model
model.save('/content/drive/MyDrive/Ag_news_dataset/baseline_model.h5')
print('.... model save ...')

## plot the accuracy and loss
plot_history(histories=history)

"""now we load our model from where the model is saved and plot the confusion matrix.

"""

new_model = tf.keras.models.load_model('/content/drive/MyDrive/Ag_news_dataset/baseline_model.h5')
y_pred = new_model.predict(X_test)

#Get the confusion matrix
cf_matrix = confusion_matrix(np.argmax(Y_test, axis=1), np.argmax(y_pred, axis=1))
sns.heatmap(cf_matrix, cmap="Blues", annot=True)

"""### for NYT"""

from keras.layers.core.dropout import Dropout
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=X.shape[1]),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64,  return_sequences=True, recurrent_regularizer='l1_l2')),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, recurrent_regularizer='l1_l2')),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(NYT_CLASS_NUMBERS)
])

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=['accuracy'])
print(model.summary())

history = model.fit(X_train , Y_train, epochs=20, batch_size=32,
                    validation_data=(X_test, Y_test))

# save model
model.save('/content/drive/MyDrive/Ag_news_dataset/baseline_model_nyt.h5')
print('.... model save ...')

## plot the accuracy and loss
plot_history(histories=history)

new_model = tf.keras.models.load_model('/content/drive/MyDrive/Ag_news_dataset/baseline_model_nyt.h5')
y_pred = new_model.predict(X_test)

#Get the confusion matrix
plt.figure(figsize = (15,10))
cf_matrix = confusion_matrix(np.argmax(Y_test, axis=1), np.argmax(y_pred, axis=1))
sns.heatmap(cf_matrix, cmap="Blues", annot=True)

"""### for BYN"""

from keras.layers.core.dropout import Dropout
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=X.shape[1]),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32,  return_sequences=True, recurrent_regularizer='l1_l2')),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, recurrent_regularizer='l1_l2')),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(BYN_CLASS_NUMBERS)
])

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=['accuracy'])
print(model.summary())

history = model.fit(X_train , Y_train, epochs=10, batch_size=512,
                    validation_data=(X_test, Y_test))

model.save('/content/drive/MyDrive/Ag_news_dataset/baseline_model_byn.h5')
print('.... model save ...')

## plot the accuracy and loss
plot_history(histories=history)

new_model = tf.keras.models.load_model('/content/drive/MyDrive/Ag_news_dataset/baseline_model_byn.h5')
y_pred = new_model.predict(X_test)

#Get the confusion matrix
plt.figure(figsize = (15,10))
cf_matrix = confusion_matrix(np.argmax(Y_test, axis=1), np.argmax(y_pred, axis=1))
sns.heatmap(cf_matrix, cmap="Blues", annot=True)