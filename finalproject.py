## Your name: Benjamin Zeffer
## The option you've chosen: 2

# Put import statements you expect to need here!
#import unittest # for testing
#import requests 
#import tweepy
#import twitter_info # as always when dealing with twitter because proper authentication is needed!
#import json
#import sqlite3
#import itertools # for generators and list comprehension
#import collections # used for containers and Counter



##### Potential Functions/Sudo code ##############################


#### def getTwitterInfo(username):
#
# PURPOSE: Making a call to the Tweepy API to get data about posted Tweets by the specified twitter user
#
# INPUT: twitter username
#
# RETURN: JSON object that can be used for extracting data later on
#
#
#------------------------------------------------------------
#
#### def getOMDBInfo(search_info):
# 
# PURPOSE: Making a call to the OMDB API and requesting the specified data
# 
# INPUT: search terms like movie name, actors, director, IMDB rating, etc
# 
# RETURN: JSON object that can be used later for extracting data when necessary
# 
# API: http://www.omdbapi.com/?
# 
# EXAMPLE OF RETURN DATA:
# {"Title":"Jason Bourne","Year":"2016","Rated":"PG-13","Released":"29 Jul 2016",
#  "Runtime":"123 min","Genre":"Action, Thriller","Director":"Paul Greengrass",
#  "Writer":"Paul Greengrass, Christopher Rouse, Robert Ludlum (characters)",
#  "Actors":"Matt Damon, Tommy Lee Jones, Alicia Vikander, Vincent Cassel",
#  "Plot":"The CIA's most dangerous former operative is drawn out of hiding to
#   uncover more explosive truths about his past.","Language":"English, Greek, 
#   German","Country":"UK, China, USA", "Awards":"13 nominations.", "Poster":
#  "https://images-na.ssl-images-amazon.com/images/M/MV5BMTU1ODg2OTU1MV5BMl5BanB
#  nXkFtZTgwMzA5OTg2ODE@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie 
#  Database","Value":"6.7/10"},{"Source":"Rotten Tomatoes","Value":"56%"},
#  {"Source":"Metacritic","Value":"58/100"}],"Metascore":"58","imdbRating":
#  "6.7","imdbVotes":"143,037","imdbID":"tt4196776","Type":"movie","DVD":
#  "06 Dec 2016","BoxOffice":"$162,162,120.00","Production":"Universal",
#  "Website":"http://www.jasonbournemovie.com/","Response":"True"}
# 
# ----------------------------------------------------------------
# 
# #### class Movie(self, OMDB_obj = {}):
# 
# PURPOSE: this class will be for the movie attributes (title, director, IMDB rating, actors, etc).
# 
# INPUT: The JSON object that will be extracted using the OMDB function from the getOMBDInfo function which grabs data from the OMDB API
# 
# RETURN: it would return a string method containing the information being searched for (director, title, IMDB rating, actors, etc)
# 
# CONSTRUCTOR: will be defining all of the self variables so that they may be used for further methods in the class
# 
#     METHODS: there will be methods with are dedicated to returning each of the stated elements (and possibly more). There will be a method whose purpose is to put the data in a format that will be easy to push it into a database. More methods are coming...
# 
# Other functions/classes/things are in the making/still being thought of...
# 
##################################################################



# Write your test cases here.

#class MovieTestCases(unittest.TestCase):
#
#	# fetching data about a movie, in this case "Mean Girls"
#    base_url = "http://www.omdbapi.com/"
#    parameters = {}
#    parameters["t"] = "mean girls" # "t" came from the API pages, this is what the key is automatically
#    response = requests.get(base_url, params=parameters)
#    data = json.loads(response.text)
#
#
#    # Testing if the movie title is a string
#    def test_movie_title_type(self):
#        self.assertEqual(type(m.title), str)
#
#    # This will be testing the movie title
#    def test_movie_title(self):
#        m = Movie(data)
#        self.assertEqual(m.title, "Mean Girls")
#
#    # This will be testing the __str__ method for the class Movie and it's "output"
#    def test_movie_str(self):
#        m = Movie(data)
#        self.assertEqual(m.__str__(), "Mean Girls, directed by Mark Waters")
#
#    # This will be testing the plot of the movie
#    def test_movie_plot(self):
#        m = Movie(data)
#        self.assertEqual(m.plot, "Cady Heron is a hit with The Plastics, the A-list girl clique at her new school, until she makes the mistake of falling for Aaron Samuels, the ex-boyfriend of alpha Plastic Regina George.")
#
#    # This will be testin the movie's release date is a string
#    def test_movie_released(self):
#    	m = Movie(data)
#    	self.assertEqual(m.released, str)
#
#    # Tesing if the strings match
#    def test_movie_released(self):
#    	m = Movie(data)
#    	self.assertEqual(m.released, "30 Apr 2004")
#
#    # This will be testing the actors and seeing if they appear in a string
#    def test_movie_actors_type(self):
#        m = Movie(data)
#        self.assertEqual(type(m.actors), str)
#
#    # Tesing the number of actors is 4
#    def test_movie_actors_len(self):
#    	m = Movie(data)
#    	self.assertEqual(len(m.actors.split(",")), 4)
#
#    # Tesing that the actors are correct
#    def test_movie_actors_names(self):
#    	m = Movie(data)
#    	self.assertEqual(m.actors, "Lindsay Lohan, Rachel McAdams, Tina Fey, Tim Meadows")
#
#
#
## Remember to invoke all your tests...
#if __name__ == "__main__":
#    unittest.main(verbosity=2)


import tweepy
import twitter_info
import unittest
import json
import sqlite3
import re
import requests
import webbrowser


##Tweepy setup

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#twitter request
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Create initial cache setup

CACHE_FNAME = "206_final_project_cache.json"

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

except:
	CACHE_DICTION = {}


def get_twitter_handle(name):

	if name in CACHE_DICTION:

		print("\n")
		print("USING CACHED DATA")
		print("\n")

		r = CACHE_DICTION[name]

	else:

		print("\n")
		print("FETCHING DATA")
		print("\n")

		r = api.search_users(q=actor_name)

		CACHE_DICTION[actor_name] = r
		# print("fetching\n")
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	for dic in r:
		if dic['verified'] == True:
			return '@'+dic['screen_name']

def user_info(user_name):
	if user_name in CACHE_DICTION:
		r = CACHE_DICTION[user_name]

	else:
		r = api.get_user(user_name)
		CACHE_DICTION[user_name] = r
		# print("fetching\n")
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

	return r

def twitter_search(search_term):
	if search_term in CACHE_DICTION:
		r = CACHE_DICTION[search_term]

	else:
		r = api.search(q=search_term)
		CACHE_DICTION[search_term] = r
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

	return r['statuses']

def twitter_neighborhood(twitter_name):
	pass #still not sure about what the "neighborhood" consists of and what tweepy api method to use

#OMDB request
def omdb_search(move_title):

	base_url = "http://www.omdbapi.com/?"
	params_dict = {}
	params_dict['t'] = move_title

	r = requests.get(base_url, params=params_dict)

	if r in CACHE_DICTION:
		CACHE_DICTION[movie_title] = r

	else:
		r = json.loads(r.text)
		CACHE_DICTION[move_title] = r
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return r

#class to handle the return value of the OMDB search
class Movie():
	def __init__(self,movie_dict):
		self.director = movie_dict['Director']
		self.actors = movie_dict['Actors']
		self.plot = movie_dict['Plot']
		self.imdbrating = movie_dict['imdbRating']
		self.ratings = movie_dict['Ratings']
		self.title = movie_dict['Title']
		self.release_date = movie_dict['Released']
		self.rated = movie_dict["Rated"]
		self.languages = movie_dict['Language']
		self.runtime = movie_dict['Runtime']
		self.imdbID = movie_dict['imdbID']

	def movie_title(self):
		return self.title

	def num_languages(self):
		num = self.languages.split(', ')
		return (len(num))

	def movie_director(self):
		return self.director

	def imdb_ID(self):
		return self.imdbID #PRIMARY KEY FOR DB

	def list_of_actors(self):
		return self.actors.split(', ')

	def num1_actor(self):
		return self.actors.split(', ')[0]

	def imdb_rating(self):
		return float(self.imdbrating)

	def released(self):
		return self.release_date

	def __str__(self):
		return "Plot description: {}\n".format(self.plot)

	def first_actor(self):
		return self.lst_actors()[0]


	def tuple(self):
		t = (self.id, self.title, self. director, self.rating, self.first_actor(), self.num_language, self. num)



list_of_movies = ['the avengers', 'the big short', 'moonlight', 'manchester by the sea', 'zootopia', "captain america: civil war", 'la la land']
movie_requests = [omdb_search(movie) for movie in list_of_movies] #list comprehension
print(movie_requests)
movie_class_instances = [Movie(movie) for movie in movie_requests] #list comprehension for movie instances
top_actors_of_movies_not_repeated = []
for movie in movie_class_instances:
	actor_name = movie.num1_actor() #getting the top actor for every movie
	if actor_name not in top_actors_of_movies_not_repeated:
		top_actors_of_movies_not_repeated.append(actor_name)
 print(top_actors_of_movies_not_repeated)
twitter_name_search = [get_twitter_handle(actor) for actor in top_actors_of_movies_not_repeated] #retrieving twitter name for each top actor fromt the movie instances; list comprehension
print(twitter_name_search)

class Tweet(object):
	
	def __init__(self, tweet_list, movie_titles):
		self.search = []
		self.text = []
		self.id = []
		self.user = []
		self.favorites = []
		self.retweets = []
		for tweet in tweet_list:
			for movie in movie_titles:
				if movie in tweet["text"]:
					self.search.append(movie)
			self.text.append(tweet["text"])
			self.id.append(tweet["id"])
			self.user.append(tweet["user"]["screen_name"])
			self.favorites.append(tweet["favorite_count"])
			self.retweets.append(tweet["retweet_count"])

	def zip_lists(self):
		m = zip(self.search, self.text, self.id, self.user, self.favorites, self.retweets)
		w = list(m)
		return w


conn = sqlite3.connect('final_probject.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Tweets")
cur.execute("DROP TABLE IF EXISTS Users")
cur.execute("DROP TABLE IF EXISTS Movies")

#tweets db
table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += "Tweets (tweet_id PRIMARY KEY, text TEXT, screen_name TEXT, movie_search TEXT, favorites INTEGER, retweets INTEGER)"
cur.execute(table_spec)

#users db
table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += "Users (user_id PRIMARY KEY, screen_name TEXT, favorites INTEGER)"
cur.execute(table_spec)

#movies db
table_spec = "CREATE TABLE IF NOT EXISTS "
table_spec += "Movies (imdbID PRIMARY KEY, title TEXT, director TEXT, languages INTEGER, imdbRating INTEGER, top_actor TEXT)"
cur.execute(table_spec)

#passing information into database

movie_table = []

for movie in movie_class_instances:
	top_actor = movie.num1_actor()
	imdbID = movie.imdb_ID()
	title = movie.movie_title()
	director = movie.movie_director()
	imdbRating = movie.imdb_rating()
	languages = movie.num_languages()
	tup = (imdbID, title, director, languages, imdbRating, top_actor)
	movie_table.append(tup)

statement = 'INSERT INTO Movies VALUES (?,?,?,?,?,?)'
for m in movie_table:
	cur.execute(statement, m)

conn.commit()



conn.close()
#########