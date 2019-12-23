import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import mysql.connector
import pyodbc
import pandas as pd
from datetime import datetime

server = 'tcp:performancemlsvr.database.windows.net'
database = 'Sentiments'
username = 'performancemluser'
password = 'Pa$$w0rd'
driver= '{ODBC Driver 17 for SQL Server}'

# "SELECT top 100 * FROM siddy_terms WHERE term LIKE ? ORDER BY date DESC"
'''
    
    Initial file to create table sentiment in db and scrape tweets into db for initial graph 
    Should be run only once ever  

'''

try:
    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    mydb = mysql.connector.connect(
      host="localhost",
      user="otaladesuyi",
      passwd="phanmium",
        database="twitterdb"
    )
    mycursor = mydb.cursor()
except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')


term ="MondayMotivation"
print("Initial term is: ", term)

# consumer key, consumer secret, access token, access secret.
ckey = "AeiEWXqrh9TEZpMK6D3JXgYeR"
csecret = "IA3ACrYMSOZqcOcWOguQBwOsy47VZCEvGLBYauVr0iWbO4Dehr"
atoken = "381209092-08RQEfpldp6hoZTqCZu2LztCZ6Ub6y1YII1OUkxa"
asecret = "WkZaxwbeZmmUWOZR7tM5wk2CePTuI4LF9laV04NvayXor"


def create_table():
    '''
        Create table in DB to store tweets
    '''

    try:
        mycursor.execute("CREATE TABLE IF NOT EXISTS sentiment(date DATETIME, term VARCHAR(200), tweet TEXT, sentiment REAL)")
        mycursor.execute("CREATE INDEX fast_term ON sentiment(term(200))")
        mycursor.execute("CREATE INDEX fast_unix ON sentiment(date)")
        mycursor.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        mydb.commit()
    except Exception as e:
        print("We got real bitch problems at create_table", str(e))


create_table()


class listener(StreamListener):
    '''
        Class to save tweets in db
    '''
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = int(data['timestamp_ms'])/1000
            time_ms= datetime.utcfromtimestamp(time_ms).strftime('%Y-%m-%d %H:%M:%S')
            vs = self.analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            mycursor.execute("INSERT INTO sentiment (date, tweet, sentiment, term) VALUES (%s, %s, %s,%s)",
                      (time_ms, tweet, sentiment, term))
            print("Just inserted the following record: time: {}, tweet: {}, sentiment: {}, term: {}".format(time_ms,
                                                                                                                tweet,
                                                                                                                sentiment,
                                                                                                                term))
            mydb.commit()

        except KeyError as e:
            print('we got real bitch problems: at listener.on_data',str(e))
        return True

    def on_error(self, status):
        print('we got real bitch problems: from listener.on_error', status)


def scrape(senti_term):
    while True:
        try:
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitterStream = Stream(auth, listener())
            twitterStream.filter(track=[str(senti_term)])
        except Exception as e:
            print(str(e))
            time.sleep(5)



scrape(term)