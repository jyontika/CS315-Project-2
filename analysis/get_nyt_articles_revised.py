"""
Script for Step 5:
Once you have done all of these in the notebook, create a Python script 
that can be called with a date (from a TikTok video). First, the script 
looks whether a CSV with cleaned articles is in our folder. 
If not, calls first the API function to get the articles and 
then the function that converts them into a CSV. 
Then, it loads the CSV into a dataframe and it uses filtering to get the articles 
for the desired date. These articles will be used for the Semantic Similarity 
portion of the TikTok Project.

Called in description-suggested-words-analysis.ipynb

Author: Audrey Yip (with help from Tayae Rogers)
"""

import os
import pandas as pd
import time
import requests

API_key = 'CvRk9Qjp9rbVhKThEcRSAphBVJYU5SDT'

def get_articles(date):
    year, month, _ = date.split('-')
    
    # remove leading 0 if month is a single digit
    if month[0] == '0':
        month = month[1:]
    
    url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={API_key}"
    
    response = requests.get(url)

    if response.status_code == 429:     # only return for successful requests
        time.sleep(10)
        get_articles(date)
    elif response.status_code != 200 and response.status_code != 429:
        print (f"Error making request to API for {date}")
        return
    else:
        # extract the articles from the response JSON corresponding to date
        article_list = response.json()['response']['docs']
        #article_list = [article for article in articles if article['pub_date'][:10] == date]
        #num_articles = len(article_list)
        
        print(f"Successfully got articles for {date}!")
        #print(f"Number of articles: {num_articles} \n")
        return article_list

def flat_dictionary(article):
    """
    Given an article, creates a flat dictionary with the abstract, lead paragraph, headline, keywords,
    pub_date, document_type, section_name, and type_of_material
    """
    dict = {}

    dict['abstract'] = article['abstract']
    dict['lead_paragraph'] = article['lead_paragraph']
    dict['headline'] = article['headline']['main']
    dict['pub_date'] = article['pub_date']
    dict['document_type'] = article['document_type']
    dict['section_name'] = article['section_name']
    dict['type_of_material'] = article['type_of_material']

    # get keywords
    keywords_list = []
    for keyword in article['keywords']:
        keywords_list.append(keyword['value'])
    keywords_concat = ';'.join(keywords_list)
    dict['keywords'] = keywords_concat

    return dict

def articles_to_csv(date):
    """
    Given a date, outputs a csv with all relevant information for each article
    Calls helper functions get_articles and flat_dictionary
    """
    # get data using helper function
    data = get_articles(date)

    # collect all article dictionaries 
    article_data =[]
    if data is not None: # tayae added (not sure if it messes something up elsewhere)
        for article in data:
            article_dict = flat_dictionary(article)
            article_data.append(article_dict)

    # create dataframe and write to csv
    df = pd.DataFrame(article_data)
    cwd = os.getcwd()
    nyt_dir = (f'{cwd}/../pre-processing/nyt-articles')
    df.to_csv(f"{nyt_dir}/NYT_articles_{date[:7]}.csv")

def filter_by_date(date):
    """
    Given a date, outputs a df with all the articles published on that date
    Calls function articles_to_csv if articles for that date are not in folder already
    """
    cwd = os.getcwd()
    #print("Current working directory:", cwd)
    nyt_dir = (f'{cwd}/../pre-processing/nyt-articles')
    #print("NYT directory:", nyt_dir)

    file_name = f"NYT_articles_{date[:7]}.csv"
    files_in_dir = set(os.listdir(nyt_dir))
    if file_name not in files_in_dir:
        print(f'NYT data for {date} not in folder, creating .csv now\n')
        articles_to_csv(date)
        time.sleep(1)
    else:
        print(f'NYT data for {date} already in folder\n')

    article_df = pd.read_csv(f"{nyt_dir}/NYT_articles_{date[:7]}.csv")
    article_df = article_df[article_df['pub_date'].str[:10] == date]

    return article_df