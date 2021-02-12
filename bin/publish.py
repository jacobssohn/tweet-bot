import logging
import json

import tweepy

from bin.credentials import MorningYawn

from bin.data_plots import commonly_used_words

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):

        file_dir = commonly_used_words(tweet.user.screen_name)
        file = open(file_dir, 'rb')
        r1 = api.media_upload(filename=file_dir, file=file)
        media_ids = [r1.media_id]
        api.update_status(status= f"{tweet.user.screen_name}'s most common words",
                          in_reply_to_status_id= tweet.id_str, media_ids=media_ids,
                          auto_populate_reply_metadata=True)

    def on_error(self, status):
        print("Error detected")


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()

def new_api():
    auth = tweepy.OAuthHandler(MorningYawn.consumer_key, MorningYawn.consumer_secret)
    auth.set_access_token(MorningYawn.access_token, MorningYawn.access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    return api


api = new_api()

my_listener = MyStreamListener(api)
my_stream = tweepy.Stream(api.auth, my_listener)
my_stream.filter(track= ["@BotYawn"])