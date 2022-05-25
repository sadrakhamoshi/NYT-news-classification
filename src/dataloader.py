import requests
from sklearn.utils import shuffle
import time 
import pandas as pd 
import sys
import getopt
from tqdm import tqdm


def get_data(api):
  sections_api = 'https://api.nytimes.com/svc/news/v3/content/section-list.json?api-key='
  api_key = 'ywtzRoKABpwTD7YG6oAsUUSfGBlEEbGZ'

  response = requests.get(sections_api+api_key)
  sections = response.json()['results']

  df = pd.DataFrame()

  for section in tqdm(sections):
    response = requests.get(api+section['section']+'.json?limit=500&api-key=' + api_key)
    if response.status_code != 200 :
      continue
    data_list = []
    data_target = []
    for r in response.json()['results']:
      data = r['title'] +'. ' + r['abstract']
      data_list.append(data)
      data_target.append(section['section'])
    
    data = {'news': data_list,
          'category': data_target
          }
    if len(data['news'])>100:
      df = df.append(pd.DataFrame(data),ignore_index = True)
    time.sleep(10)

  return df

def main(argv):
  arg_api = "https://api.nytimes.com/svc/news/v3/content/all/"
  arg_help = "{0} -a <api>".format(argv[0])
  
  try:
    opts, args = getopt.getopt(argv[1:], "ha:", ["help", "api="])
  except:
    print(arg_help)
    sys.exit(2)
  
  for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(arg_help)
        sys.exit(2)
    elif opt in ("-a", "--api"):
        arg_api = arg

  df = get_data(arg_api)
  df = shuffle(df)
  df.to_csv('/content/drive/MyDrive/nlp/shffule_data.csv')
  print('Data is saved to /content/drive/MyDrive/nlp/shffule_data.csv')

if __name__ == "__main__":
  main(sys.argv)
  

