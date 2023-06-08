#Twitter Sentiment Analysis
#Team 8
#Vignesh 36822026
#Subramaniyan 36822025
#Jeevanantham 36822015
#Dhaarani Priya 36822005
#Nithyasri 36822010
#Santhosh 36822020
#Date 20/11/2022
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from textblob.sentiments import NaiveBayesAnalyzer

from flask import Flask, render_template , redirect, url_for, request



def clean_tweet( tweet): 

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
         
def get_tweet_sentiment( tweet): 
        
        # analysis = TextBlob(clean_tweet(tweet), analyzer=NaiveBayesAnalyzer()) 

        # if analysis.sentiment.classification == "pos": 
        #     return 'positive'
        # elif analysis.sentiment.classification == "neg": 
        #     return 'negative'

        analysis = TextBlob(clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"


def get_tweets(api, query, count=5): 
        
        count = int(count)
        tweets = [] 
        try: 
            
            fetched_tweets = tweepy.Cursor(api.search_tweets, q=query, lang ='en', tweet_mode='extended').items(count)
            
            for tweet in fetched_tweets: 
                
                parsed_tweet = {} 

                if 'retweeted_status' in dir(tweet):
                    parsed_tweet['text'] = tweet.retweeted_status.full_text
                else:
                    parsed_tweet['text'] = tweet.full_text

                parsed_tweet['sentiment'] = get_tweet_sentiment(parsed_tweet['text']) 

                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
            return tweets 
        except tweepy.TweepyException as e: 
            print("Error : " + str(e)) 

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
  return render_template("index.html")

# ******Phrase level sentiment analysis
@app.route("/predict", methods=['POST','GET'])
def pred():
	if request.method=='POST':
            query=request.form['query']
            count=request.form['num']
            fetched_tweets = get_tweets(api,query, count) 
            return render_template('result.html', result=fetched_tweets)

# fetched_tweets
# [
#   {"text" : "tweet1", "sentiment" : "sentiment1"},
#   {"text" : "tweet2", "sentiment" : "sentiment2"},
#   {"text" : "tweet3", "sentiment" : "sentiment3"}
# ]

# *******Sentence level sentiment analysis
@app.route("/predict1", methods=['POST','GET'])
def pred1():
	if request.method=='POST':
            text = request.form['txt']
            blob = TextBlob(text)
            if blob.sentiment.polarity > 0:
                text_sentiment = "positive"
            elif blob.sentiment.polarity == 0:
                text_sentiment = "neutral"
            else:
                text_sentiment = "negative"
            return render_template('result1.html',msg=text, result=text_sentiment)


if __name__ == '__main__':
    
    consumer_key = 'NWD1NWwmrTrxBSKtY5d2GmtU3' 
    consumer_secret = 'olKFRd5DNdiXn0tFtH5ipAvOni8D47Z3sWQPb1JgdGK2LXK7if'
    access_token = '1599298879605772288-8qsbKIcw1njhdOuCmBVDjY5J01Cwzo'
    access_token_secret = 'zWX2GOU8kNAijXuSTqGd2jTMXHrUzb23MKFVeeFQQ5Qtp'

    try: 
        auth = OAuthHandler(consumer_key, consumer_secret)  
        auth.set_access_token(access_token, access_token_secret) 
        api = tweepy.API(auth)
    except: 
        print("Error: Authentication Failed") 

    app.debug=True
    app.run(host='localhost')

