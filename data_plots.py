import tweepy
import matplotlib
from matplotlib import pyplot
import pandas
from credentials import MorningYawn

auth = tweepy.OAuthHandler(MorningYawn.consumer_key, MorningYawn.consumer_secret)
auth.set_access_token(MorningYawn.access_token, MorningYawn.access_token_secret)


api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

user = api.get_user("winter_muse_")

dates = []

timeline = api.home_timeline()
followers = user.followers()
print(type(timeline))
print(type(followers))
print(len(followers))
# for follower in tweepy.Cursor(api.followers, "winter_muse_").items(50):
#     print(follower)
#     dates.append(follower['created at'])