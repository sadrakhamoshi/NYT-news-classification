import argparse
import sys
import collections
import csv
import re
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import WordPunctTokenizer, WhitespaceTokenizer, TreebankWordTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
STOPWORDS = set(stopwords.words('english'))

def read_news(path):
    x = []
    y = []
    with open(path,'r', encoding='utf-8') as csv_file:
      csv_reader = csv.reader(csv_file)
      header = next(csv_reader)
      for row in csv_reader:
        x.append(row[1])
        y.append(row[2])

    return x, y

def remove_stop_words(tokens):
    new_tokens = [t for t in tokens if t not in STOPWORDS]
    return new_tokens


def remove_short_words(tokens: list):
    new_tokens = [t for t in tokens if len(t) > 2]
    return new_tokens


def lemmatization_reconstruct_sentence(tokens):
    new_tokens = lemmatization(tokens)
    return ' '.join(new_tokens)


def stemming(tokens):
    new_tokens = [PorterStemmer().stem(token) for token in tokens]
    return new_tokens

def remove_white_space(text):
    # text = re.sub(r'(\s)*(\n)(\s)*', '\n', text)
    return re.sub(r'\s\s+', ' ', text)

def lemmatization(tokens):
    new_tokens = [WordNetLemmatizer().lemmatize(token) for token in tokens]
    return new_tokens

def to_lowercase(tokens):
    new_tokens = [token.lower() for token in tokens]
    return new_tokens


def remove_handle(tokens):
    new_tokens = [re.sub(r'@(\S+)', '', token) for token in tokens]
    return new_tokens


def remove_specials_numbers(tokens):
    new_tokens = [re.sub(r'[^a-z\s]+', '', token) for token in tokens]
    return new_tokens


def tokenization(text):
    tokens = TreebankWordTokenizer().tokenize(text)
    return tokens

def create_word_cloud(text: str):
    wordcloud = WordCloud(width=800, height=800,
                          background_color='black',
                          stopwords=STOPWORDS,
                          min_font_size=10).generate(text)

    # plot the WordCloud image
    plt.figure(figsize=(25, 15), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('/content/drive/MyDrive/wordcloud.png')

def top_word_bar_chart(trends: dict):
    # sort the dictionary
    sorted_trends = [(k, v) for k, v in sorted(trends.items(), key=lambda item: item[1], reverse=True)]
    x = []
    y = []
    for k, v in sorted_trends[:10]:
        x.append(v)
        y.append(k)
    plt.figure(figsize=(20, 10), facecolor=None)
    plt.bar(y, x)
    plt.xlabel('trend', fontsize='18')
    plt.ylabel('times', fontsize='18')
    plt.tight_layout(pad=0)
    plt.savefig('top_trends.png')

def remove_empty(cleaned_data):
  for i,news in enumerate(cleaned_data):
    if len(news[0])<1:
      cleaned_data.pop(i)
  return cleaned_data

def cleaning(x):
    cleaned_data = []

    for line in x:
      news_org = line

      # step 1
      tokens = tokenization(news_org)

      # step 2
      tokens = to_lowercase(tokens)

      # step 3
      tokens = remove_handle(tokens)

      # step 4
      tokens = remove_specials_numbers(tokens)

      # step 6
      tokens = remove_stop_words(tokens)

      # step 7
      tokens = remove_short_words(tokens)

      # step 8
      final_tweet = lemmatization_reconstruct_sentence(tokens)
      
      cleaned_data.append(final_tweet)

    return cleaned_data
