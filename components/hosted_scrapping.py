import sys
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
#import mysql.connector
import pyodbc
import pandas as pd
from datetime import datetime
from flask import Flask, request
import git
from components import config
import nltk

server = config.server
database = config.database
username = config.username
password = config.password
driver = config.driver


'''
    
    Initial file to create table sentiment in db and scrape tweets into db for initial graph 
    Should be run only once ever  

'''

try:
    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')
        sys.exit(1)


#term ="MondayMotivation"
df_terms = pd.read_sql("SELECT * FROM siddy_terms ORDER BY date DESC", cnxn)
termlist= df_terms.Term.unique() #['Sidmach', 'technologies', 'database', 'algorithms', 'data science']
#print("Initial term is: ", term)

# consumer key, consumer secret, access token, access secret.
ckey = config.ckey
csecret = config.csecret
atoken = config.atoken
asecret =config.asecret


# def create_table():
#     '''
#         Create table in DB to store tweets
#     '''
#
#     try:
#         mycursor.execute("CREATE TABLE IF NOT EXISTS sentiment(date DATETIME, term VARCHAR(200), tweet TEXT, sentiment REAL)")
#         mycursor.execute("CREATE INDEX fast_term ON sentiment(term(200))")
#         mycursor.execute("CREATE INDEX fast_unix ON sentiment(date)")
#         mycursor.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
#         mydb.commit()
#     except Exception as e:
#         print("We got real bitch problems at create_table", str(e))


#create_table()


class listener(StreamListener):
    '''
        Class to save tweets in db
    '''
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    def on_data(self, data):
        try:
            data = json.loads(data)
            post = unidecode(data['text'])
            time_ms = int(data['timestamp_ms'])/1000
            date_time= datetime.utcfromtimestamp(time_ms).strftime('%Y-%m-%d %H:%M:%S')
            vs = self.analyzer.polarity_scores(post)
            user = data['user']
            medium = 'twitter'
            RetweetCount  = data['retweet_count']
            LikeCount = data['favorite_count']
            keywords = ['', '']
            hashtags = data['Entities']["hashtags"]
            QuoteCount = data['quote_count']
            ReplyCount = data['reply_count']
            username = user['screen_name']
            FollowerCount = user['followers_count']
            isVerified = user['verified']
            location = user['location']  # "Lagos"
            sentiment = vs['compound']
            category = 1 if sentiment > 0 else -1 if sentiment < 0 else 0
            sentiment_insert = "INSERT INTO siddy_sentiments\
                (Post, [Location], Sentiment, Category, Term, Medium, [Date])\
                  VALUES (?,?,?,?,?,?,?)"
            cnxn.execute(sentiment_insert, (post, location, sentiment, category, termlist[0], medium, date_time))
            print("Just inserted the following record: time: {}, tweet: {}, sentiment: {}, term: {}".format(date_time,
                                                                                                                post,
                                                                                                                sentiment,
                                                                                                                termlist))
            cnxn.commit()

        except KeyError as e:
            print('we got real bitch problems: at listener.on_data',str(e))
            with open('errors.txt', 'a') as f:
                f.write(str(e))
                f.write('\n')
            sys.exit(1)
        return True

    def on_error(self, status):
        print('we got real bitch problems: from listener.on_error', status)
        with open('errors.txt', 'a') as f:
            f.write(str(status))
            f.write('\n')
        sys.exit(1)


def scrape(senti_term):
    while True:
        try:
            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            twitterStream = Stream(auth, listener(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            twitterStream.filter(track=senti_term)
        except Exception as e:
            print('we got real bitch problems: from scrape()',str(e))
            with open('errors.txt', 'a') as f:
                f.write(str(e))
                f.write('\n')
            sys.exit(1)


app = Flask(__name__)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('https://github.com/kitanbelles/Hosted_scrapping')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


scrape(termlist)
