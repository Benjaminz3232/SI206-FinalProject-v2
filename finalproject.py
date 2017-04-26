
## Import statements
import unittest
import sqlite3
import requests
import json
import tweepy
import twitter_info
import re
#from pprint import pprint
import itertools
import collections


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
    #CACHE_DICTION["omdb"] = {}  ##might be more structured, not necessary though
    #CACHE_DICTION["twitter"] = {} ##might be more structured, not necessary though



##Getting OMDB data functions
def get_OMDB_data(omdb_search_term):
    if omdb_search_term in CACHE_DICTION:
        #print("\nUsing cached data for OMDB: " + omdb_search_term + "\n")
        response = CACHE_DICTION[omdb_search_term]

    else:
        #print("\nfetching data for OMDB: " + omdb_search_term + "\n")
        base_url = "http://www.omdbapi.com/?"
        params = {}
        params['t'] = omdb_search_term

        r = requests.get(base_url, params=params)
        response = json.loads(r.text)

        CACHE_DICTION[omdb_search_term] = response

        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return response


#movie_dict = get_OMDB_data("Mean Girls")
#print(movie_dict)


class Movie(object):
    def __init__(self, omdb_data):
        self.omdb_data = omdb_data
        self.imdbID = omdb_data["imdbID"] #$%^
        self.title = omdb_data["Title"] #$%^
        self.year = omdb_data["Year"]
        self.released = omdb_data["Released"]
        self.runtime = omdb_data["Runtime"]
        self.genre = omdb_data["Genre"]
        self.director = omdb_data["Director"] #$%^
        self.writer = omdb_data["Writer"]
        self.actors = omdb_data["Actors"]#.split(", ") #$%^
        self.plot = omdb_data["Plot"]
        self.language = omdb_data["Language"]#.split(", ") #$%^
        self.country = omdb_data["Country"]
        self.awards = omdb_data["Awards"]
        self.poster = omdb_data["Poster"]
        self.ratings_imdb = omdb_data["Ratings"][0]["Value"] #$%^
        self.ratings_imdbvotes = omdb_data["imdbVotes"]
        self.boxoffice = omdb_data["BoxOffice"]

    #def __str__(self):
    #    return("{} directed by {}, writing done by {},\nreleased {}, with actors {}, imdb rating of {}".format(self.title, self.director, self.writer, self.released, self.actors, self.ratings_imdb))

    def get_actors(self):
        return self.actors

    def __str__(self): #was get_title
        return self.title

    def get_languages(self):
        num_languages = self.language.split(", ")
        return (len(num_languages))

    def get_imdbID(self):
        return self.imbdID

    def get_list_of_actors(self):
        return self.actors.split(", ")

    def movie_info(self):
        lst = [
        self.title,
        self.director,
        self.rating_imdb,
        self.actors,
        self.imdbID
        ]

        return lst


##Getting Twitter data functions
def get_twitter_search_data(search_term):

    if search_term in CACHE_DICTION:
        #print("\nUsing cached data for TWITTER: " + search_term + "\n")
        response = CACHE_DICTION[search_term]

    else:
        #print("\nFetching data for TWITTER:" + search_term + "\n")
        results = api.search(q = search_term) # , count = 20 TAKEN OUT
        response = results["statuses"]

        CACHE_DICTION[search_term] = response

        f = open(CACHE_FNAME, "w")
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return response

##
def get_twitter_user_data(username):

    if username in CACHE_DICTION:
        #print("\nUsing cached data for twitter user: " + username + "\n")
        response = CACHE_DICTION[username]

    else:
        #print("\nFetching data for twitter user: " + username + "\n")
        response = api.get_user(username)
        CACHE_DICTION[username] = response

        f = open(CACHE_FNAME, "w")
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return response


class Tweet(object):
    def __init__(self, tweet_dict):
        self.id = tweet_dict["id"] ##primary key for tweet db
        self.user = tweet_dict["user"]["id"]
        self.text = tweet_dict["text"].encode("utf-8")
        self.numfavorites = tweet_dict["favorite_count"]
        self.numretweets = tweet_dict["retweet_count"]

    def tweet_content(self):
        return self.text

    def tweet_id(self):
        return self.id

    def tweet_info(self):
        lst = [
        self.text, 
        self.user, 
        self.movie, 
        self.numfavorites, 
        self.retweets
        ]

        return lst



##List of movies to search
movies_list = [
    "Mean Girls", 
    "Jason Bourne", 
    "The Dark Night", 
    "Pulp Fiction", 
    "The Lord of the Rings: The Return of the King"
    ]


##Making requests to the OMDB API
OMDB_movie_requests = [get_OMDB_data(movie) for movie in movies_list]


##Creating class instances of each movie from the movie list
movie_classinsts = []
for movie in OMDB_movie_requests:
    movie_classinsts.append(Movie(movie))


##Getting tweets about movies
#tweets = []
#for movie in movies_list:
#    tweets.append(get_twitter_search_data(movie))


#movie_tweets = []
#for movie in movies_list:
#    movie_tweets.append((movie, get_twitter_search_data(movie)))





















#make database thingy that does movies with ratings above 5 and 8

#make thing that reads if something has been retweeted 500 times

#make thingy that sorts the movies by number of awards then nomiations


conn = sqlite3.connect("si206finalproject.db")
cur = conn.cursor()

##Tweets table
cur.execute("DROP TABLE IF EXISTS Tweets")
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Tweets (tweet_id PRIMARY KEY, text TEXT, screen_name TEXT, movie_search TEXT, favorites INTEGER, retweets INTEGER)"
cur.execute(statement)

##Users table
cur.execute("DROP TABLE IF EXISTS Users")
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Users (user_id PRIMARY KEY, screen_name TEXT, favorites INTEGER, description TEXT, followers INTEGER)"
cur.execute(statement)

##Movies table
cur.execute("DROP TABLE IF EXISTS Movies")
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Movies (imdbID PRIMARY KEY, title TEXT, year TEXT, released TEXT, runtime TEXT, genre TEXT, director TEXT, writer TEXT, actors TEXT, plot TEXT, language TEXT, country TEXT, awards TEXT, poster TEXT, ratings_imdb INTEGER, ratings_imdbvotes INTEGER, boxoffice TEXT)"
cur.execute(statement)







##RIP MY TEST CASES

##Test cases
#print("\n*** OUTPUT OF TESTS BELOW THIS LINE ***\n")

class OMDB_tests(unittest.TestCase):
    def test_omdb_movie_search(self):
        #d = get_OMDB_data("Mean Girls")
        #movie = Movie(d)
        pass

class Twitter_tests(unittest.TestCase):
    pass

class Database_tests(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
