import tweepy

from bin.credentials import MorningYawn

auth = tweepy.OAuthHandler(MorningYawn.consumer_key, MorningYawn.consumer_secret)
auth.set_access_token(MorningYawn.access_token, MorningYawn.access_token_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

