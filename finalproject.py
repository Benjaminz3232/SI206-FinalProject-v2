# SI 206 FINAL PROJECT OPTION 2
# by BENJAMIN ZEFFER


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

#Imports to handle emojis and other uncommon characters not in windows operating systems
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer) # had to learn about this online and from others



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
CACHE_FNAME = "si206_final_project_cache.json"

try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)

except:
    CACHE_DICTION = {}
    CACHE_DICTION["OMDB"] = {}  ## Specific part of cache for omdb
    CACHE_DICTION["Twitter"] = {} ## Sepcific part of cache for twitter stuff


## List of movies
movies_list = ["Mean Girls", "Jason Bourne", "The Dark Knight", "Pulp Fiction", "Deadpool", "Guardians of the Galaxy"]


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


def emotion_score(plot):
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
	plot_words = []
	for words in plot.split():
		plot_words.append(words)

	#compiling an emotion score of each tweet_words list about an entire movie
	emotion_score = 0

	for words in plot_words:
		if words in pos_ws:
			emotion_score += 1
		else:
			pass

	for words in plot_words:
		if words in neg_ws:
			emotion_score += -1
		else:
			pass

	#making a relative rating based on people's responses to the movie
	num_words = len(plot_words)
	rating = int(emotion_score / num_words)


	return emotion_score


def get_twitter_search_data(search):
    if search in CACHE_DICTION["Twitter"]:
        results = CACHE_DICTION["Twitter"][search]

    else:
        results = api.search(q = search, count = 50)
        CACHE_DICTION["Twitter"][search] = results

        f = open(CACHE_FNAME, "w")
        f.write(json.dumps(CACHE_DICTION))
        f.close()

    return results["statuses"]


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
		self.boxoffice = omdb_dict["BoxOffice"][1:]

	def __str__(self):
		return self.title

	def get_title(self):
		return self.title

	def get_director(self):
		return self.director

	def get_rating(self):
		return self.rating

	def get_actor(self):
		return self.actors.split(", ")[0]

	def infotuple(self):
		return (self.id, self.title, self.director, self.rating, self.actors, self.plot, self.boxoffice, self.languages, self.awards)


class Tweet(object):

	def __init__(self, tweet_dict, movie=""):
		self.tweet_id = tweet_dict["id"]
		self.text = tweet_dict["text"]
		self.user = tweet_dict["user"]["id"]
		self.num_favs = tweet_dict["favorite_count"]
		self.num_rt = tweet_dict["retweet_count"]
		self.movie = movie

	def __str__(self):
		return self.text

	def text(self):
		return self.text

	def num_rt(self):
		return self.num_rt

	def movie(self):
		return movie

	def infotuple(self):
		return (self.user, self.text, self.num_rt, self.user, self.num_favs, self.movie)


class TwitterUser(object):
	def __init__(self, twitter_user_dict):
		self.id = twitter_user_dict["id"]
		self.username = twitter_user_dict["screen_name"]
		self.num_favs = twitter_user_dict["favourites_count"] #THIS MESSED ME UP BC THEY SPELLED IT "FAVOURITE"...I'm petty
		self.num_followers = twitter_user_dict["followers_count"]

	def infotuple(self):
		return (self.id, self.username, self.num_favs, self.num_followers)



##Setting up databases
conn = sqlite3.connect("si206finalproject.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Tweets")
cur.execute("DROP TABLE IF EXISTS Users")
cur.execute("DROP TABLE IF EXISTS Movies")

##Movies table
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Movies (imdbID PRIMARY KEY, title TEXT, director TEXT, rating TEXT, actors TEXT, plot TEXT, boxoffice INTEGER, language TEXT, awards TEXT)"
cur.execute(statement)

##Tweets table
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Tweets (user INTEGER PRIMARY KEY, username TEXT, text TEXT, num_favs INTEGER, rt INTEGER)"
cur.execute(statement)

##Users table
statement = "CREATE TABLE IF NOT EXISTS "
statement += "Users (user_id PRIMARY KEY, screen_name TEXT, num_favs INTEGER, num_followers INTEGER)"
cur.execute(statement)


## Inserting into movies db ##########
statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

movie_insts = [Movie(get_OMDB_data(movie)) for movie in movies_list]
movie_info_list = [inst.infotuple() for inst in movie_insts]

for movie in movie_info_list:
	cur.execute(statement, movie)

conn.commit()


## Inserting into Tweets db ##########
statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'

tweet_dicts = []
for movie in movies_list:
	tweet_dicts.append((movie, get_twitter_search_data(movie)))

list_of_tweets = []
for tpl in tweet_dicts:
	list_of_tweets.append(tpl[1])
#print(Tweet(list_of_tweets[0][0]))

list_of_insts = []
for x in list_of_tweets:
	for tweet in x:
		list_of_insts.append(Tweet(tweet, x[0]))


for tweet_inst in list_of_insts:
	info_to_insert = tweet_inst.infotuple()
	try:
		cur.execute(statement, info_to_insert)
	except:
		pass

conn.commit()


## Inserting into Users db ##########
statement = 'INSERT INTO Users VALUES (?, ?, ?, ?)'

def find_mentioned_users(lst_o_tweets):
	lst = []
	for tweet in lst_o_tweets:
		users = re.findall("(@[A-Za-z0-9_]+)", tweet.__str__())
		lst.append(users)

	repeats_mentioned = []
	for alist in lst:
		for name in alist:
			repeats_mentioned.append(name)

	unique_mentioned = []
	for name in repeats_mentioned:
		if name not in unique_mentioned:
			unique_mentioned.append(name)

	return unique_mentioned

mentioned_users = find_mentioned_users(list_of_tweets)

#print(mentioned_users)

working_mentioned_users = []
user_data = []
for user in mentioned_users:
	try:
		data = get_twitter_user(user)
		working_mentioned_users.append(user)
	except:
		pass

	user_data.append(data)

user_insts = [TwitterUser(user) for user in user_data]

#print(TwitterUser(get_twitter_user("@yahoo")))

for user in user_insts:
	info_to_insert = user.infotuple()
	try:
		cur.execute(statement, info_to_insert)
	except:
		pass

conn.commit()

##Passing data into databases
good_movies = "SELECT title, rating FROM Movies WHERE rating > 7.5"
cur.execute(good_movies)
good_movies = cur.fetchall()

high_earning_movies = "SELECT title, boxoffice FROM Movies WHERE boxoffice > 50000000" # 50 milion
cur.execute(high_earning_movies)
high_earning_movies = cur.fetchall()

movies = "SELECT title, rating FROM Movies"
cur.execute(movies)
movies = cur.fetchall()

sorted_by_ratings = sorted(movies, key=lambda x: x[1], reverse=True)

good_tweets = "SELECT Tweets.user, Tweets.text, Tweets.num_favs FROM Tweets INNER JOIN Users ON Users.user_id WHERE Tweets.num_favs > 1500"
cur.execute(good_tweets)
good_tweets = cur.fetchall()


##Create an output
output_fname = "si206_final_project_output.txt"
f = open(output_fname, "w")



f.write("The following movies were searched:\n")

f.write("\nMovie: 'Mean Girls'")
f.write("\n      " + "Directed by:   " + movie_info_list[0][2])
f.write("\n      " + "With actors:   " + movie_info_list[0][4])
f.write("\n      " + "IMDB Rating:   " + movie_info_list[0][3])
f.write("\n      " + " Movie plot:   " + movie_info_list[0][5])
f.write("\n      " + " Box office:   " + movie_info_list[0][6])
f.write("\n      " + "     Awards:   " + movie_info_list[0][8])
f.write("\n      " + "  Languages:   " + movie_info_list[0][7])
f.write("\n    " + "OMDB Movie ID:   " + movie_info_list[0][0])
f.write("\n    " + "Emotion score:   " + str(emotion_score(movie_info_list[0][5])))


f.write("\n\nMovie: 'Jason Bourne'")
f.write("\n      " + "Directed by:   " + movie_info_list[1][2])
f.write("\n      " + "With actors:   " + movie_info_list[1][4])
f.write("\n      " + "IMDB Rating:   " + movie_info_list[1][3])
f.write("\n      " + " Movie plot:   " + movie_info_list[1][5])
f.write("\n      " + " Box office:   " + movie_info_list[1][6])
f.write("\n      " + "     Awards:   " + movie_info_list[1][8])
f.write("\n      " + "  Languages:   " + movie_info_list[1][7])
f.write("\n    " + "OMDB Movie ID:   " + movie_info_list[1][0])
f.write("\n    " + "Emotion score:   " + str(emotion_score(movie_info_list[1][5])))


f.write("\n\nMovie: 'The Dark Knight'")
f.write("\n      " + "Directed by:   " + movie_info_list[2][2])
f.write("\n      " + "With actors:   " + movie_info_list[2][4])
f.write("\n      " + "IMDB Rating:   " + movie_info_list[2][3])
f.write("\n      " + " Movie plot:   " + movie_info_list[2][5])
f.write("\n      " + " Box office:   " + movie_info_list[2][6])
f.write("\n      " + "     Awards:   " + movie_info_list[2][8])
f.write("\n      " + "  Languages:   " + movie_info_list[2][7])
f.write("\n    " + "OMDB Movie ID:   " + movie_info_list[2][0])
f.write("\n    " + "Emotion score:   " + str(emotion_score(movie_info_list[2][5])))


f.write("\n\nMovie: 'Pulp Fiction'")
f.write("\n      " + "Directed by:   " + movie_info_list[3][2])
f.write("\n      " + "With actors:   " + movie_info_list[3][4])
f.write("\n      " + "IMDB Rating:   " + movie_info_list[3][3])
f.write("\n      " + " Movie plot:   " + movie_info_list[3][5])
f.write("\n      " + " Box office:   " + movie_info_list[3][6])
f.write("\n      " + "     Awards:   " + movie_info_list[3][8])
f.write("\n      " + "  Languages:   " + movie_info_list[3][7])
f.write("\n    " + "OMDB Movie ID:   " + movie_info_list[3][0])
f.write("\n    " + "Emotion score:   " + str(emotion_score(movie_info_list[3][5])))

f.write("\n\nMovie: 'Deadpool'")
f.write("\n      " + "Directed by:   " + movie_info_list[4][2])
f.write("\n      " + "With actors:   " + movie_info_list[4][4])
f.write("\n      " + "IMDB Rating:   " + movie_info_list[4][3])
f.write("\n      " + " Movie plot:   " + movie_info_list[4][5])
f.write("\n      " + " Box office:   " + movie_info_list[4][6])
f.write("\n      " + "     Awards:   " + movie_info_list[4][8])
f.write("\n      " + "  Languages:   " + movie_info_list[4][7])
f.write("\n    " + "OMDB Movie ID:   " + movie_info_list[4][0])
f.write("\n    " + "Emotion score:   " + str(emotion_score(movie_info_list[4][5])))

f.write("\n\nMovie: 'Guardians of the Galaxy'")
f.write("\n      " + "Directed by:   " + movie_info_list[5][2])
f.write("\n      " + "With actors:   " + movie_info_list[5][4])
f.write("\n      " + "IMDB Rating:   " + movie_info_list[5][3])
f.write("\n      " + " Movie plot:   " + movie_info_list[5][5])
f.write("\n      " + " Box office:   " + movie_info_list[5][6])
f.write("\n      " + "     Awards:   " + movie_info_list[5][8])
f.write("\n      " + "  Languages:   " + movie_info_list[5][7])
f.write("\n    " + "OMDB Movie ID:   " + movie_info_list[5][0])
f.write("\n    " + "Emotion score:   " + str(emotion_score(movie_info_list[5][5])))


f.write("\n--------------------------------------\n")

f.write("\nHere's a list of the movies which were rated above a 7.5/10.0 on IMDB")
for movie in good_movies:
	f.write("\n     {} with a rating of {}".format(movie[0], movie[1]))

f.write("\n\n--------------------------------------\n")

f.write("\nHere's a list of movies which earned over $50,000,000 in box office revenue:")
for movie in high_earning_movies:
	f.write("\n     {} with a box office of ${}".format(movie[0], movie[1]))

f.write("\n\n--------------------------------------\n")

f.write("\nHere's a list of tweets about the movies that had over 1,500 favorites:")
for tweet in good_tweets:
	f.write("\n     " + tweet)

if good_tweets == []:
	f.write("\n     N/A -- no tweets over that number of favorites\n")

f.write("\n--------------------------------------\n")

f.write("\nHere's a list of all of the users who were mentioned in recent tweets regarding the movies above:")
for name in mentioned_users:
	f.write("\n      " + name + "\n")


f.close()


conn.close()



##Test cases
#print("\n*** OUTPUT OF TESTS BELOW THIS LINE ***\n")

class Access_tests(unittest.TestCase):
	def test_01_movies(self):
		self.assertEqual(movies_list, ["Mean Girls", "Jason Bourne", "The Dark Knight", "Pulp Fiction", "Deadpool", "Guardians of the Galaxy"])
	
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


class OMDB_tests(unittest.TestCase):
	def test_plot_01(self):
		self.assertEqual("Cady Heron is a hit with The Plastics, the A-list girl clique at her new school, until she makes the mistake of falling for Aaron Samuels, the ex-boyfriend of alpha Plastic Regina George.", movie_info_list[0][5])
	
	def test_plot_02(self):
		self.assertEqual("The CIA's most dangerous former operative is drawn out of hiding to uncover more explosive truths about his past.", movie_info_list[1][5])
	
	def test_plot_03(self):
		self.assertEqual("When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, the Dark Knight must come to terms with one of the greatest psychological tests of his ability to fight injustice.", movie_info_list[2][5])


if __name__ == "__main__":
    unittest.main(verbosity=2)