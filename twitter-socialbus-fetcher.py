# -*- coding: utf-8 -*-

import click
import csv
import sys
import urllib2
import urllib
import json
from urlparse import urlparse

SOCIALECHO_TWEETS_ENDPOINT = "http://reaction.fe.up.pt/portugal/tweets/select"
PAGE_SIZE = 10000

def find_collection_size(http_get, http_endpoint, query):
    params = {}
    params['wt'] = 'json'
    params['rows'] = 0
    params['start'] = 0
    params['q'] = query

    get_params = urllib.urlencode(params)

    response = http_get.open(SOCIALECHO_TWEETS_ENDPOINT + "?" + get_params)
    content = response.read()
    json_content = json.loads(content)

    total_hits = int(json_content["response"]["numFound"])
    return total_hits

def find_tweets(http_get, http_endpoint, page_size, query):

    total_hits = find_collection_size(http_get, http_endpoint, query)
    pagination = range(0, total_hits + page_size, page_size)

    for page in pagination:
        # print(page)
        params = {}
        params['wt'] = 'json'
        params['rows'] = page_size
        params['start'] = page
        params['q'] = 'language_s:es'

        get_params = urllib.urlencode(params)

        response = http_get.open(http_endpoint + "?" + get_params)
        content = response.read()

        json_content = json.loads(content)

        tweets = json_content["response"]["docs"]

        for tweet in tweets:
            if not ("created_at" in tweet.keys()): continue
            if not ("text" in tweet.keys()): continue

            tweet_text = tweet["text"].replace("  "," ")
            tweet_text = tweet_text.replace("\t"," ")
            tweet_text = tweet_text.replace("\n"," ")
            tweet_text = tweet_text.replace("\r"," ")
            tweet_text = tweet_text.strip()
            tweet_text = tweet_text.encode("utf-8")

            tweet_id = str(tweet["id"])
            user_id = str(tweet["user_id"])
            user_screename = tweet["screen_name"].strip()
            user_screename = user_screename.encode("utf-8")

            # now output our tweet
            print "%s;%s;%s;%s" % (tweet_id,user_id,user_screename,tweet_text)


@click.command()
@click.option('--query',default="*:*", prompt='Inform lucene query', help='Inform lucene query')
@click.option('--http_address', prompt='Inform solr http address', help='Solr address')
@click.option('--page_size', default=100,prompt='Inform page size', help='Number of rows per request')
@click.option('--http_user', prompt='Inform http user', help='HTTP User')
@click.option('--http_pass', prompt='Inform http password', help='HTTP Password')
def main(query, http_address, page_size, http_user, http_pass):
    """Console script for socialbus tweets collector"""

    url_parse = urlparse(http_address)
    domain = url_parse.scheme + "://" + url_parse.netloc

    http_endpoint = http_address + "/portugal/tweets/select"
    page_size = int(page_size)

    # Create an OpenerDirector with support for Basic HTTP Authentication...
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None,domain,
                              http_user,
                              http_pass)

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    http_get = urllib2.build_opener(handler)
    urllib2.install_opener(http_get)

    find_tweets(http_get,http_endpoint,page_size,query)


if __name__ == "__main__":
    main()
