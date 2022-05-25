# NYT-news-classification
A Natural Language Processing project for guessing the section of each news from New York Times news.

## Overview

First, we featced data, almost 15000 news from almost 50 different sections, from [nytimes](https://www.nytimes.com/).  
After that, we do some preprocessing including stemming, lemmatization, lowercase and etc to our data to make it more clean and ready for NLP tasks.

## How To Run




### installation

1. Install [python3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/)

2. Install virtualenv
    > pip install virtualenv

3. Create virtual environment
    >  virtualenv [virtualenv_name]

4. Activate the Virtualenv on Linux/MacOs
    >  source [virtualenv_name]/bin/activate

5. Activate the Virtualenv on Windows
    >   .[virtualenv_name]\Scripts\activate

6. Install requirements

    >  pip install -r requirements.txt

## Run commands

    fetching data
    > python dataloader.py

    cleaning data 
    > python datacleaner.py

    > plot the bar chart and wordcloud
    python plot.py


# Enjoy 😊

