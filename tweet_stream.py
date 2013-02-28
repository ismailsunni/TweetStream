"""Tweet Stream
Custom implementation of tweepy.streamlistener for streaming tweets
and put them in the database.
"""

__author__ = 'ismailsunni'
__project_name = 'TweetStream'
__filename = 'tweet_stream.py'
__date__ = '28/02/13'
__copyright__ = 'imajimatika@gmail.com'

import sys
import tweepy
import constants
from database_connection import db_conn

consumer_key = constants.consumer_key
consumer_secret = constants.consumer_secret
access_key = constants.access_key
access_secret = constants.access_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.api = api or API()
        self.data = db_conn()

    def on_status(self, status):
        try:
            alpha = self.data.insert_tweet(status.id_str, status.text,
                                    status.created_at, '', 0,
                                    status.user.id_str,
                                    status.user.screen_name,
                                    False, False)
            print 'saved ', status.user.screen_name, alpha
        except UnicodeEncodeError as e:
            print e

    def on_error(self, status_code):
        print sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['indonesia'])