#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-stream-format:
#  - ultra-real-time stream of twitter's public timeline.
#    does some fancy output formatting.
#-----------------------------------------------------------------------

from twitter import *
import re
from nltk.corpus import stopwords



#-----------------------------------------------------------------------
# import a load of external features, for text display and date handling
# you will need the termcolor module:
#
# pip install termcolor
#-----------------------------------------------------------------------
from time import strftime
from textwrap import fill
from termcolor import colored
from email.utils import parsedate

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

search_term = ",".join(stopwords.words('spanish'))
allowed_languages = ["es"]
#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"])
stream = TwitterStream(auth = auth, secure = True)

#-----------------------------------------------------------------------
# iterate over tweets matching this filter text
#-----------------------------------------------------------------------
tweet_iter = stream.statuses.filter(track = search_term)

pattern = re.compile("%s" % search_term, re.IGNORECASE)

i=0
for tweet in tweet_iter:
	if not ("created_at" in tweet.keys()): continue
	if not ("lang" in tweet.keys()): continue
	if not (tweet["lang"] in allowed_languages): continue


	# turn the date string into a date object that python can handle
	timestamp = parsedate(tweet["created_at"])

	# now format this nicely into HH:MM:SS format
	timetext = strftime("%H:%M:%S", timestamp)

	# colour our tweet's time, user and text
	time_colored = colored(timetext, color = "white", attrs = [ "bold" ])
	user_colored = colored(tweet["user"]["screen_name"], "green")
	text_colored = tweet["text"]

	# replace each instance of our search terms with a highlighted version
	# text_colored = pattern.sub(colored(search_term.upper(), "yellow"), text_colored)

	# add some indenting to each line and wrap the text nicely
	indent = " " * 11
	text_colored = fill(text_colored, 80, initial_indent = indent, subsequent_indent = indent)

	# now output our tweet
	# print "(%s) @%s" % (time_colored, user_colored)
	i+=1
	print "(%s)(%s) %s" % (str(i),tweet["lang"], unicode(tweet["text"]))
