from pymongo import MongoClient
from flask import Flask, render_template,request, jsonify,redirect,url_for
import pymongo
import tweepy
import pandas as pd
import praw
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html') 
@app.route('/twitter', methods=['POST'])
def twitter():
    if request.method =='POST':
        if request.form['submit_button'] == 'Scrap':
            key=request.form['Name']
            datadict=tweetScrape(key)
            db = MongoClient("mongodb://BDAT1004:Password@cluster0-shard-00-00.gzlae.mongodb.net:27017,cluster0-shard-00-01.gzlae.mongodb.net:27017,cluster0-shard-00-02.gzlae.mongodb.net:27017/Mydatabase3?ssl=true&replicaSet=atlas-qnmzak-shard-0&authSource=admin&retryWrites=true&w=majority")
            x = db["Mydatabase3"]["Tweet_scrape"].insert_many(datadict)
            return render_template('home.html')
        elif request.form['submit_button'] == 'Post':
            key=request.form['Name']
            datadict=tweetPost(key)
            return render_template('home.html')
@app.route('/reddit', methods=['POST'])
def reddit():
    if request.method=='POST':
        if request.form['submit_button'] == 'Scrap':
            key=request.form['Name']
            datadict=redditScrape(key)
            db = MongoClient("mongodb://BDAT1004:Password@cluster0-shard-00-00.gzlae.mongodb.net:27017,cluster0-shard-00-01.gzlae.mongodb.net:27017,cluster0-shard-00-02.gzlae.mongodb.net:27017/Mydatabase3?ssl=true&replicaSet=atlas-qnmzak-shard-0&authSource=admin&retryWrites=true&w=majority")
            x = db["Mydatabase3"]["Reddit_scrape"].insert_many(datadict)
            return render_template('home.html')
        elif request.form['submit_button'] == 'Post':
            key=request.form['Name']
            datadict=redditPost(key)
            return render_template('home.html')
    #data=barchart1()          
    #return render_template('Home.html',data=data)


def redditScrape(key):
    Client_ID="Esg_SY4QYiDtWw"
    Client_SECRET="n-YaZIFn-7LTKmaOhje4RY5eePJ8xw"
    PASSWORD="92~h'$nn34mSqxe"
    USER_AGENT="test (by /u/BatPrestigious9187 )"
    USERNAME='BatPrestigious9187'
    reddit = praw.Reddit(client_id='Esg_SY4QYiDtWw', client_secret='n-YaZIFn-7LTKmaOhje4RY5eePJ8xw', user_agent='my_user_agent')
    posts = []
    ml_subreddit = reddit.subreddit(key)
    for post in ml_subreddit.hot(limit=100):
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
    posts.to_csv('file1.csv')
    df = pd.read_csv("file1.csv", usecols = ['title','score','id','url','num_comments','body'])
    df.reset_index(inplace=True)
    datadict = df.to_dict('records')
    return datadict

def redditPost(msg):
    reddit = praw.Reddit(client_id='Esg_SY4QYiDtWw',client_secret='n-YaZIFn-7LTKmaOhje4RY5eePJ8xw',user_agent='test by /u/BatPrestigious9187 ',redirect_uri='http://localhost:8080',refresh_token='826684171550-q4OO9oVV1iDLvRsm0Z1THrfgD-jD2w')
    subr = 'pythonsandlot'
    subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable
 
    title = msg
    selftext = msg
    
    d=subreddit.submit(title,selftext=selftext)

    return d









def tweetScrape(userid):
    consumer_key = "KuuPY4dskxE1YP9ymgGsv844A"
    consumer_secret = "56DRD0MK57mxTKQe5r1JA4YD5JOqlqXceXEQczExW8L95aVC1l"
    access_token = "727087799304884225-BkvQsF3IJ4Il8GxmNwKP9FEVJlp35OJ"
    access_token_secret = "lzhr3ErGT5NsHus2kkXtl8ECrQbgVwGEoLLj9JTkrgL1n"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    username = userid
    count = 150
    tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
    # Pulling information from tweets iterable object
    tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
    # Creation of dataframe from tweets list
    # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list)
    tweets = tweepy.Cursor(api.search, q=username).items(count)
    # Pulling information from tweets iterable 
    tweets_list = [[tweet.created_at, tweet.id, tweet.text, tweet.user, tweet.favorite_count] for tweet in tweets]
    # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(tweets_list)
    tweets_df.to_csv('file2.csv')
    df = pd.read_csv("file2.csv", usecols = ['0','2','3'])
    df.reset_index(inplace=True)
    datadict = df.to_dict('records')
    return datadict
def tweetPost(msg):
    consumer_key = "KuuPY4dskxE1YP9ymgGsv844A"
    consumer_secret = "56DRD0MK57mxTKQe5r1JA4YD5JOqlqXceXEQczExW8L95aVC1l"
    access_token = "727087799304884225-BkvQsF3IJ4Il8GxmNwKP9FEVJlp35OJ"
    access_token_secret = "lzhr3ErGT5NsHus2kkXtl8ECrQbgVwGEoLLj9JTkrgL1n"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(status =msg)
    return 1
if __name__ == "__main__":
    app.run()