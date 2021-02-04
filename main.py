import tweepy

from credentials import MorningYawn

auth = tweepy.OAuthHandler(MorningYawn.consumer_key, MorningYawn.consumer_secret)
auth.set_access_token(MorningYawn.access_token, MorningYawn.access_token_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

user = api.get_user("winter_muse_")

timeline = api.home_timeline(100)
for tweet in timeline:
    try:
        #tweet.favorite()
        api.destroy_favorite(tweet.id)
    except tweepy.error.TweepError:
        continue
    print(type(tweet))
    print(f"{tweet.user.name} said {tweet.text}")
