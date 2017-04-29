## Import statements
import unittest
import sqlite3
import requests
import json
import tweepy
import twitter_info
import re
from pprint import pprint
import itertools
import collections
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)



##Twitter authentication
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


##Setting up Tweepy API
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


##Caching try/except loop
CACHE_FNAME = "206_final_project_cache.json" ##CHANGE THIS CHACHE NAME
try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}
    CACHE_DICTION["OMDB"] = {}  ## Specific part of cache for omdb
    CACHE_DICTION["Twitter"] = {} ## Sepcific part of cache for twitter stuff


## Getting OMDB data functions
def get_OMDB_data(omdb_search_term):
    if omdb_search_term in CACHE_DICTION["OMDB"]:
        omdb_dict = CACHE_DICTION["OMDB"][omdb_search_term]

    else:
        base_url = "http://www.omdbapi.com/?"
        params = {}
        params['t'] = omdb_search_term

        r = requests.get(base_url, params=params)
        omdb_dict = json.loads(r.text)
        CACHE_DICTION["OMDB"][omdb_search_term] = omdb_dict

        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()

    return omdb_dict


def get_twitter_search_data(movie):
    if movie in CACHE_DICTION["Twitter"]:
        movie_tweets = CACHE_DICTION["Twitter"][movie]

    else:
        results = api.search(q = movie, count = 20)
        movie_tweets = results["statuses"]
        CACHE_DICTION["Twitter"][movie] = movie_tweets

        f = open(CACHE_FNAME, "w")
        f.write(json.dumps(CACHE_DICTION))
        f.close()

    return movie_tweets


def get_twitter_user(username):
    if username in CACHE_DICTION["Twitter"]:
        user_data = CACHE_DICTION["Twitter"][username]

    else:
        user_data = api.get_user(username)
        CACHE_DICTION["Twitter"][username] = user_data

        cache_file = open(CACHE_FNAME, "w")
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()

    return user_data


def emotion_score(movie_tweet_dict):
    #creating list of positive words
    pos_ws = []
    f = open('positive-words.txt', 'r')
    for l in f.readlines()[35:]:
        pos_ws.append(l.strip())
    f.close()

    #creating a list of negative words
    neg_ws = []
    f = open('negative-words.txt', 'r')
    for l in f.readlines()[35:]:
        neg_ws.append(l.strip())
    f.close

    #putting all of the words from the text of the tweets into a single list
    tweet_words = []
    for tweet in movie_tweet_dict:
        tweet_inst = Tweet(tweet)
        text = tweet_inst.get_text()
        tweet_words.append(text.split())


    #compiling an emotion score of each tweet_words list about an entire movie
    emotion_score = 0

    for words in news_words:
        if words in pos_ws:
            emotion_score += 1
        else:
            pass

    for words in news_words:
        if words in neg_ws:
            emotion_score += -1
        else:
            pass

    #making a relative rating based on people's responses to the movie
    num_words = len(tweet_words)
    rating = int(emotion_score / num_words)


    return emo_score


class Movie(object):
    def __init__(self, omdb_dict):
        self.id = omdb_dict["imdbID"]
        self.title = omdb_dict["Title"]
        self.director = omdb_dict["Director"].split(", ")[0]
        self.rating = omdb_dict["imdbRating"]
        self.actors = omdb_dict["Actors"]
        self.plot = omdb_dict["Plot"]
        self.languages = omdb_dict["Language"]
        self.awards = omdb_dict["Awards"]
        self.boxoffice = omdb_dict["BoxOffice"]

    def __str__(self):
        return self.title

    def get_title(self):
        return self.title

    def get_director(self):
        return self.director

    def get_rating(self):
        return self.rating

    def infotuple(self):
        return (self.id, self.title, self.director, self.rating, self.actors, self.plot, self.boxoffice, self.languages, self.awards)


class Tweet(object):

    def __init__(self, tweet_dict):
        self.tweet_id = tweet_dict["id"]
        self.user_id = tweet_dict["user"]["id"]
        self.text = tweet_dict["text"]
        self.num_favs = tweet_dict["favorite_count"]
        self.num_rt = tweet_dict["retweet_count"]

    def __str__(self):
        return self.text

    def tweet_content(self):
        return self.text

    def infotuple(self):
        return (self.tweet_id, self.user_id, self.text, self.num_favs, self.num_rt)

class TwitterUsers(object):
    def __init__(self, twitter_user_dict):
        self.id = twitter_user_dict["id"]
        self.username = twitter_user_dict["screen_name"]
        self.num_followers = twitter_user_dict["followers_count"]

    def __str__(self):
        pass

    def infotuple(self):
        return (self.id, self.username, self.num_followers)




## List of movies
movies_list = ["Mean Girls", "Jason Bourne", "The Dark Knight", "Pulp Fiction"]





##Setting up databases
conn = sqlite3.connect("si206finalproject.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Tweets")
cur.execute("DROP TABLE IF EXISTS Users")
cur.execute("DROP TABLE IF EXISTS Movies")

##Movies table
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Movies (imdbID PRIMARY KEY, title TEXT, director TEXT, rating TEXT, actors TEXT, plot TEXT, boxoffice TEXT, language TEXT, awards TEXT)"
cur.execute(statement)

##Tweets table
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Tweets (tweet_id INTEGER PRIMARY KEY, username TEXT, text TEXT, num_favs INTEGER, rt INTEGER)"
cur.execute(statement)

##Users table
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Users (user_id PRIMARY KEY, screen_name TEXT, favorites INTEGER, description TEXT, followers INTEGER)"
cur.execute(statement)


##inserting into movies db
statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

movie_stuff = []

movie_insts = [Movie(get_OMDB_data(movie)) for movie in movies_list]
movie_info_list = [inst.infotuple() for inst in movie_insts]

for movie in movie_info_list:
    cur.execute(statement, movie)

conn.commit()


##inserting into Tweets db
statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'






##Create an output
output_fname = "si206_final_project_output.txt"
f = open(output_fname, "w")

f.write("The following movies were searched:\n")
for movie in movies_list:
    f.write("   " + movie + "\n")

f.close()







conn.close()



##Test cases
#print("\n*** OUTPUT OF TESTS BELOW THIS LINE ***\n")

class Access_tests(unittest.TestCase):
    def test_01_MeanGirls(self):
        self.assertTrue("Mean Girls" in movies_list)
    def test_02_MeanGirls(self):
        self.assertTrue("Mean Girls" in CACHE_DICTION["OMDB"])
    def test_03_JasonBourne(self):
        self.assertTrue("Jason Bourne" in movies_list)
    def test_04_JasonBourne(self):
        self.assertTrue("Jason Bourne" in CACHE_DICTION["OMDB"])
    def test_05_DarkKnight(self):
        self.assertTrue("The Dark Knight" in movies_list)
    def test_06_DarkKnight(self):
        self.assertTrue("The Dark Knight" in CACHE_DICTION["OMDB"])
    def test_07_PulpFiction(self):
        self.assertTrue("Pulp Fiction" in movies_list)
    def test_08_PulpFiction(self):
        self.assertTrue("Pulp Fiction" in CACHE_DICTION["OMDB"])


if __name__ == "__main__":
    unittest.main(verbosity=2)