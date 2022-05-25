from utils.utils import *
import pandas as pd
import requests
from nltk.tokenize import sent_tokenize, word_tokenize
import collections
import re


api_key = 'ywtzRoKABpwTD7YG6oAsUUSfGBlEEbGZ'


def compute_sent(data):
  sentences = []
  for d in data:
    sentences.extend(sent_tokenize(d))
  return len(sentences)

def compute_unit(data):
  return len(data)

def compute_token(data):
  tokens = []
  for d in data:
    tokens.extend(word_tokenize(d))

  return len(tokens)

def compute_vocab(data):
  tokens = []
  for d in data:
    tokens.extend(word_tokenize(d))
  tokens_unique = set(tokens)
  return len(tokens_unique)

def compute_stat(data, raw):
  data = data['news']
  unit_num = compute_unit(data)
  sent_num = compute_sent(raw['news'])
  token_num = compute_token(data)
  vocab_num = compute_vocab(data)
  return [unit_num,sent_num,token_num,vocab_num]

def get_tokens(cleaned_news):
  all_tokens = []
  for news in cleaned_news:
      all_tokens.extend(news.split(' '))

  token_counter = collections.Counter(all_tokens)
  return token_counter

def all_histogram_plot(cleaned_news):
  all_tokens = []
  for news in cleaned_news:
      all_tokens.extend(news.split(' '))

  token_counter = collections.Counter(all_tokens)
  top_word_bar_chart(token_counter, 'all')


def top_word_bar_chart(trends: dict, name='trend'):
    name = re.sub('/','-',name)
    # sort the dictionary
    sorted_trends = [(k, v) for k, v in sorted(trends.items(), key=lambda item: item[1], reverse=True)]
    x = []
    y = []
    for k, v in sorted_trends[:10]:
        x.append(v)
        y.append(k)
    plt.figure(figsize=(20, 10), facecolor=None)
    plt.bar(y, x)
    plt.xlabel(name, fontsize='18')
    plt.ylabel('times', fontsize='18')
    plt.tight_layout(pad=0)
    import os
    path = '/content/drive/MyDrive/nlp/histograms'
    isExist = os.path.exists(path)
    if not isExist:
      os.makedirs(path)
    plt.savefig(f'{path}/{name}.png')
    plt.close()
    print(f'{name}.png is saved to {path}')

def plot_table(df,raw):
  col_labels = ['unit num','sent num','token num', 'vocab num']
  sections_api = 'https://api.nytimes.com/svc/news/v3/content/section-list.json?api-key='
  response = requests.get(sections_api+api_key)
  sections = response.json()['results']
  row_labels = []
  data = []
  for s in sections:
    sec_data = df.where(df.category==s['section']).dropna()
    sec_sentences = raw.where(raw.category==s['section']).dropna()
    if len(sec_data['news'])<100:
      continue
    row_labels.append(s['section'])
    tokens = get_tokens(sec_data['news'])
    top_word_bar_chart(tokens, s['section'])
    data.append(compute_stat(sec_data,sec_sentences))
  fig, ax =plt.subplots(1,1)
  df=pd.DataFrame(data,columns=col_labels)
  ax.axis('tight')
  ax.axis('off')
  ax.table(cellText=df.values,
          colLabels=df.columns,
          rowLabels=row_labels,
          loc="center")

  plt.savefig("/content/drive/MyDrive/nlp/table.png", bbox_inches="tight")
  plt.close(fig)


if __name__=='__main__':
  df = pd.read_csv('/content/drive/MyDrive/nlp/cleaned_news.csv')
  raw = pd.read_csv('/content/drive/MyDrive/nlp/shffule_data.csv')
  plot_table(df,raw)
  x, y = read_news('/content/drive/MyDrive/nlp/shffule_data.csv')
  cleaned_news = cleaning(x)
  a = ' '.join(cleaned_news)
  create_word_cloud(a)
  all_histogram_plot(cleaned_news)


