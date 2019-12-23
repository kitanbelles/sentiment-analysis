import time
from unidecode import unidecode
import pyodbc
import sys
import pandas as pd
from datetime import datetime, date
from components import config
import nltk 

server = config.server
database = config.database
username = config.username
password = config.password
driver= config.driver


try:
    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    mycursor = cnxn.cursor()
except Exception as e:
    with open('errors.txt', 'a') as f:
        f.write(str(e))
        f.write('\n')
    sys.exit(1)
'''
    This module fetches initial data from twitter for initial graphs.
    Also Fetches tweets by term. Returns null if tweets do not exist. 
    Challenge: If tweet do not exist, I Need to return control to the front end   
'''


'''
    Need to crate a generic errorlogger fxn that stores errors in an excel file 
'''

#term ="NationalBoyfriendDay" #senti.return_term()
# print("term is: ", term)



def fetch_initial_tweets():
    try:
        df = pd.read_sql("SELECT top 1000 * FROM siddy_sentiments ORDER BY date DESC", cnxn )
        df_terms = pd.read_sql("SELECT * FROM siddy_terms ORDER BY date DESC", cnxn)
        cnxn.close()
        # df = format_df(df)
        return df_terms, df
    except Exception as e:
        with open('dberrors.txt', 'a') as f:
            towrite='error from fetch_initial_tweets on the ' + str(date.today()) + ' '+ str(e)
            f.write(towrite)
            f.write('\n')
        print('we got real bitch problems: at tweetFetch.py.fetch_initial_tweets', str(e))
        return pd.DataFrame(), pd.DataFrame()


def check_term(term):
    try:
        df = pd.read_sql("SELECT top 100 * FROM siddy_sentiments WHERE term LIKE ? ORDER BY date DESC", cnxn,
                         params=('%' + term + '%',))
        if df.notnull:
            cnxn.close()
            return df
            # return update_graph_scatter(df)
        else:
            return pd.DataFrame()
            # return null df
            # return game graph
    except Exception as e:
        with open('errors.txt', 'a') as f:
            towrite = 'error from check_term on the ' + str(date.today()) + str(e)
            f.write(towrite)
            f.write('\n')


def format_df(df):
    # df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df) / 2)).mean()
    # df['unix'] /= 1000
    # df['date'] = pd.to_datetime(df['date'])
    df.sort_values('Date', inplace=True)
    max_d = df['Date'].max().to_pydatetime()
    min_d = df['Date'].min().to_pydatetime()
    diff_date = max_d - min_d
    diff_d = diff_date.total_seconds()
    hours = diff_d // 3600
    days = hours // 24
    weeks = days // 7
    months = days // 30
    years = months // 12
    if (diff_d <= 600):
        df = df.resample('30S', on='Date').mean()
    elif (diff_d > 600 and diff_d < 3600):
        df = df.resample('1min', on='Date').mean()
    elif (hours >= 1 and hours <= 12):
        df = df.resample('30min', on='Date').mean()
    elif (hours > 12 and hours < 24):
        df = df.resample('60min', on='Date').mean()
    elif (days >= 1 and days <= 7):
        df = df.resample('8H', on='Date').mean()
    elif (days > 7 and days < 31):
        df = df.resample('1D', on='Date').mean()
    elif (months >= 1 and months <= 8):
        df = df.resample('1W', on='Date').mean()
    elif (months > 8 and months < 24):
        df = df.resample('1M', on='Date').mean()
    elif (years >= 2 and years <= 10):
        df = df.resample('1Q', on='Date').mean()
    elif (years > 10):
        df = df.resample('1Y', on='Date').mean()
    df['Date'] = df.index.values
    # df.set_index('date', inplace=True)
    # df = df.resample('1min', on='date').mean()
    #df.dropna(subset=['sentiment'], inplace=True)
    return df


# tweets_df = fetch_initial_tweets()
# termlist = tweets_df['Term'].unique()
# print ("first five rows in tweets_df is: ", tweets_df.head())
# print('termlist is : ', termlist)
# check_term(termlist[0])