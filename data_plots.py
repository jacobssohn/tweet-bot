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

tweets_text = []

timeline = api.home_timeline()

#
# for tweet in tweepy.Cursor(api.user_timeline, "winter_muse_").items(50):
#     tweets_text.append(tweet.text)
# print(tweets_text)
#
# most_used = {}
# for tweet in tweets_text:
#     tweet = tweet.split()
#     for word in tweet:
#         if not word in most_used.keys():
#             most_used[word] = 1
#         else:
#             most_used[word] += 1
# print(most_used)
# print(dict(sorted(most_used.items(), key=lambda item: item[1], reverse=True)))
most_liked = {}
print('winter muse: ')
for tweet in tweepy.Cursor(api.favorites, "winter_muse_").items(500):
    if tweet.user.screen_name in most_liked.keys():
        most_liked[tweet.user.screen_name] += 1
    else:
        most_liked[tweet.user.screen_name] = 1

    tweets_text.append(tweet.text)

print(dict(sorted(most_liked.items(), key=lambda item: item[1], reverse=True)))
#
# most_liked = {}
# print('twistshoutx: ')
# for tweet in tweepy.Cursor(api.favorites, "twistshoutx").items(500):
#     if tweet.user.screen_name in most_liked.keys():
#         most_liked[tweet.user.screen_name] += 1
#     else:
#         most_liked[tweet.user.screen_name] = 1
#     tweets_text.append(tweet.text)
#
# print(dict(sorted(most_liked.items(), key=lambda item: item[1], reverse=True)))