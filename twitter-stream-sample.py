#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-stream-format:
#  - ultra-real-time stream of twitter's public timeline.
#    does some fancy output formatting.
#-----------------------------------------------------------------------

from twitter import *
import re

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

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"])
stream = TwitterStream(auth = auth, secure = True)

allowed_languages = ["es"]
#-----------------------------------------------------------------------
# iterate over tweets matching this filter text
#-----------------------------------------------------------------------
tweet_iter = stream.statuses.sample()

pattern = re.compile("%s" % "sample", re.IGNORECASE)

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

	# now output our tweet
	# print "(%s) @%s" % (time_colored, user_colored)
	print "(%s) %s" % (tweet["lang"], tweet["text"])
