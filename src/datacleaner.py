from utils.utils import *

def main():
  x, y = read_news('/content/drive/MyDrive/nlp/shffule_data.csv')
  cleaned_news = cleaning(x)  
  cleaned_data = [[a, b] for a, b in zip(cleaned_news, y)]
  cleaned_data = remove_empty(cleaned_data)
  with open('/content/drive/MyDrive/nlp/cleaned_news.csv', 'w', encoding='utf-8', newline='') as fw:
    writer = csv.writer(fw)
    writer.writerow(['news','category'])
    writer.writerows(cleaned_data)

if __name__ == "__main__":
   main()
   