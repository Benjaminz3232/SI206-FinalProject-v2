README


Option 2 -- API Mashup: Twitter and OMDB


Benjamin Zeffer


What does it do?
* The code which I've written essentially searches through list of movies and pulls data from Twitter and the OMDB API. Additionally, there's some data manipulation involved when generating what to put in the output file.


What is needed:
* Files needed to make finalproject.py run:
   * finalproject.py
      * Run this by typing “python finalproject.py” in the command line
      * This is the code of the project
   * twitter_info.py
      * This isn’t included in the given files, but this is needed in order to access twitter and should be filled with the appropriate confidential number strings
   * negative_words.txt
      * Used to iterate through words and compile an emotion score
   * positive_words.txt
      * Used to iterate through words and compile an emotion score
* You also need to have the following python modules installed:
   * unittest
   * sqlite3
   * requests
   * json
   * tweepy
   * re
   * pprint
   * itertools
   * collections
   * sys
   * codecs


Files included:
* 206_finalproject_plan
*  si206_final_project_cache.json
* finalproject.py
* twitter_info.py
* negative_words.txt
* positive_words.txt
* si206_final_project_output.txt
* screenshot57.png


Functions/Classes
* Name: get_OMDB_data
   * Input: Omdb_search term (req)
   * Returns: dictionary containing omdb data
   * Other: Caches this omdb data into the cache created in the lines before its definition
* Emotion_score
   * Input: Movie plot (req)
   * Returns: integer
* Name: get_twitter_search_data
   * Input: search → aka movie name (req)
   * Returns: dictionary containing twitter data
   * Other: caches this data
* Name: get_twitter_user
   * Input: twitter username (req)
   * Returns: dictionary containing information about the twitter user
   * Other: caches this data
* Name: find_mentioned_users
   * Input: list of tweets (in dictionary format)
   * Returns: a list of twitter users who were mentioned in the tweets being gathered.


* Name: (CLASS) Movie
   * Each instance presents a movie
   * Input: dictionary containing data from omdb about movie (req)
   * Methods:
      * __str__
         * Returns the title
      * Get_title
         * Also returns the title
      * Get_director
         * Returns the name of the director
      * get _rating
         * Returns the rating from imdb
      * Get_actor
         * Returns the first actor
      * Info_tuple
         * Returns mainly just a tuple containing a bunch of information bundled from the movie dictionary
* Name: (CLASS) Tweet
   * One instance represents a tweet about one of the movies in the list given
   * Input: tweet dictionary from the get_twitter_search_data function (req)
      * Optional = movie (didn’t actually do anything with this, thought I was going to need it and didn’t want to take it out bc cI was afraid I would screw something up)
   * Methods:
      * __str__
         * returns the text of the tweet
      * Text
         * Also returns the text of the tweet
      * Num_rt
         * Returns the number of retweets
      * Movie
         * Returns the movie associated with the tweets
      * Infotuple
         * Returns: same thing as the MOvie dictionary, except and tuple containing info about each tweet
* Name: (CLASS) TwitterUser
   * One instance represents a twitter user
   * Input: dictionary containing data about twitter user
   * Methods:
      * Infotuple
         * Returns: information packed tuple (just like previous two classes) expect it’s about the twitter user


Databases
* “Movies”
   * Each row represents a movie and all of its data
   * Has imdbID PRIMARY KEY, title TEXT, director TEXT, rating TEXT, actors TEXT, plot TEXT, boxoffice INTEGER, language TEXT, awards TEXT
* “Tweets”
   * Each row represents a tweet about the movie and all of its data
   * user INTEGER PRIMARY KEY, username TEXT, text TEXT, num_favs INTEGER, rt INTEGER
* “Users”
   * Each row represents twitter user
   * user_id PRIMARY KEY, screen_name TEXT, num_favs INTEGER, num_followers INTEGER


Data manipulation
* Firstly, all of the data manipulation code which I have created allows for ease of access as well as being able to use this data to tell interesting things about the movies being searched
   * I am able to create a list of mentioned_users which compiles all of the users and returns a master list
   * I am also able to grab all of the movies which have a rating over 7.5/10.0
   * Furthermore, I am able to create a list of movies which is ordered by the ratings in reverse order
   * Lastly, I am able to get tweets over a certain number of favorites by joining two tables and returning the movie in addition to seeing this favorite count


Why did I choose this option?
* I felt that this option was the most interesting and allowed me to expand upon things which I have previously learned and felt strongly about in the class.


Lines for code
* Line(s) on which each of your data gathering functions begin(s): 56-105
* Line(s) on which your class definition(s) begin(s): 151-216
* Line(s) where your database is created in the program: 220-241
* Line(s) of code that load data into your database: 244-331
* Line(s) of code (approx) where your data processing code: 333-350
* Line(s) of code that generate the output: 353-459