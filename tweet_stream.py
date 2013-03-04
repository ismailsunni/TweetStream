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
from unicodedata import normalize
import tweepy
import constants
from database_connection import db_conn

# constant
consumer_key = constants.consumer_key
consumer_secret = constants.consumer_secret
access_key = constants.access_key
access_secret = constants.access_secret


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        tweepy.StreamListener.__init__(self, api)
        self.data = db_conn()

    def on_status(self, status):
        try:
            added = self.data.insert_tweet(status.id_str, status.text,
                                           status.created_at,
                                           status.user.id_str,
                                           status.user.screen_name,
                                           False, False)
            if added:
                print 'added new tweet...'
        except UnicodeEncodeError as e:
            print 'UnicodeEncodeError', e
            try:
                my_normal_text = normalize('NFKD',
                                           status.text.decode('latin-1')
                                           ).encode('ascii', 'ignore')
                added = self.data.insert_tweet(status.id_str, my_normal_text,
                                               status.created_at,
                                               status.user.id_str,
                                               status.user.screen_name,
                                               False, False)
                if added:
                    print 'added new tweet....'
            except Exception as ex:
                print 'Exception', ex

    def on_error(self, status_code):
        print sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
    sapi.filter(track=['indonesia'])

if __name__ == '__main__':
    main()
