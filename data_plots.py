import random
import tweepy
import nltk
from nltk.corpus import stopwords as sw
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
from credentials import MorningYawn

print(sw.words('spanish'))
# auth = tweepy.OAuthHandler(MorningYawn.consumer_key, MorningYawn.consumer_secret)
# auth.set_access_token(MorningYawn.access_token, MorningYawn.access_token_secret)
#
# api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#
# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")
#
# user = api.get_user("winter_muse_")

# stopwords = stopwords.words('english') + stopwords.words('spanish') #
# #
# # tweets_text = []
# #
# # timeline = api.home_timeline()
# #
# # most_liked = {} #
# print(stopwords)
# most_liked = {'wordA': 56, 'wordB': 34, 'wordC': 29, 'wordD': 20, 'wordE': 18, 'wordF': 15, 'wordG': 3, 'wordH': 2, 'wordI': 1, 'you': 4, 'RT': 4, 'me': 3}
# # print('winter muse: ')
# # for tweet in tweepy.Cursor(api.favorites, "winter_muse_").items(500):
# #     if tweet.user.screen_name in most_liked.keys():
# #         most_liked[tweet.user.screen_name] += 1
# #     else:
# #         most_liked[tweet.user.screen_name] = 1
# #
# #     tweets_text.append(tweet.text)
# #
# # most_liked = dict(sorted(most_liked.items(), key=lambda item: item[1], reverse=True))
# #
# words_cleansed = {}
# for key, value in most_liked.items():
#     if not key in stopwords and key != 'RT':
#         words_cleansed[key] = value
#
# df = pd.DataFrame.from_dict(words_cleansed, orient='index')
# print(df[0].sum())
#
# print(words_cleansed)
# sum_check = 0
# remaining_sum = 0
# words_segregated = {}
# for key, value in words_cleansed.items():
#     if sum_check / df[0].sum()  <= 0.9:
#         sum_check += value
#         words_segregated[key] = value
#     else:
#         remaining_sum += value
#         print(key, value)
# words_segregated['Remaining\n words'] = remaining_sum
#
# print(sum_check, '\n', remaining_sum)
#
# fig, ax = plt.subplots()
# words_ax = [key for key, value in words_segregated.items()]
# uses = [value for key, value in words_segregated.items()]
# print(len(words_ax), len(uses))
# colours = ['turquoise', 'bisque', 'palegreen', 'orchid', 'peru', 'pink', 'lightcyan', 'gold', 'salmon']
# colours = (colours.pop(random.randint(0, len(colours)-1)), colours.pop(random.randint(0, len(colours)-2)), colours.pop(random.randint(0, len(colours)-3)))
# print(colours)
# ax.bar(words_ax, uses, color=colours[0])
# plt.xticks(rotation=-20)
# plt.ylabel('Number of uses')
# plt.title(f"Most popular words by use in {user.screen_name}'s tweets")
# ax.set_facecolor(colours[1])
# fig.patch.set_facecolor(colours[2])
# plt.show()
# fig.savefig('Graphs/used_words.png')

def commonly_used_words(user: str, number_of_tweets = 10):

    auth = tweepy.OAuthHandler(MorningYawn.consumer_key, MorningYawn.consumer_secret)
    auth.set_access_token(MorningYawn.access_token, MorningYawn.access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")



    #user = api.get_user(user)
    stopwords = sw.words('english') + sw.words('spanish')
    tweets_text = []

    for tweet in tweepy.Cursor(api.user_timeline,id=user).items(number_of_tweets):
        print(tweet)
        tweets_text.append(tweet.text)
    print('tweets text: ', tweets_text)

    if number_of_tweets > 200:
        alltweets = []
        new_tweets = api.user_timeline(screen_name=user, count=200)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=user, count=200, max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
            if len(alltweets) > number_of_tweets:
                break
    else:
        alltweets = api.user_timeline(screen_name=user, count=number_of_tweets)
    print(alltweets)
    most_used_words = []
    for tweet in tweets_text:
        most_used_words += tweet.split(' ')
    print('most used words: ', most_used_words)
    most_used_words_cleared = []
    for word in most_used_words:
        print(word)
        word = word.strip()
        if word == '' or len(word) == 1 or len(word) == 2:
            continue
        if word[-1] == '.' or word[-1] == ',':
            word = word[:-1]
        if word[0] == '@':
            continue
        word = word.lower()
        most_used_words_cleared.append(word)

    print(most_used_words)

    most_liked = {}
    for word in most_used_words_cleared:
        if word in most_liked.keys():
            most_liked[word] += 1
        else:
            most_liked[word] = 1

    most_liked = dict(sorted(most_liked.items(), key=lambda item: item[1], reverse=True))
    print('most liked: ', most_liked)
    words_cleansed = {}
    for key, value in most_liked.items():
        if not key in stopwords and key != 'RT':
            words_cleansed[key] = value

    df = pd.DataFrame.from_dict(words_cleansed, orient='index')
    #print(df[0].sum())
    print(df)
    print(words_cleansed)
    sum_check = 0
    remaining_sum = 0
    words_segregated = {}
    for key, value in words_cleansed.items():
        if sum_check / df[0].sum() <= 0.05:
            sum_check += value
            words_segregated[key] = value
        else:
            remaining_sum += value
            print(key, value)
    #words_segregated['Remaining\n words'] = remaining_sum # uncomment this to see the amount of uses of the remaining words

    print(sum_check, '\n', remaining_sum)

    fig, ax = plt.subplots()
    words_ax = [key for key, value in words_segregated.items()]
    uses = [value for key, value in words_segregated.items()]
    print(len(words_ax), len(uses))
    colours = ['turquoise', 'bisque', 'palegreen', 'orchid', 'peru', 'pink', 'lightcyan', 'gold', 'salmon']
    colours = (colours.pop(random.randint(0, len(colours) - 1)), colours.pop(random.randint(0, len(colours) - 2)),
               colours.pop(random.randint(0, len(colours) - 3)))
    print(colours)
    ax.bar(words_ax, uses, color=colours[0])
    plt.xticks(rotation=-20)
    plt.ylabel('Number of uses')
    plt.title(f"Most popular words by use in {user}'s tweets")
    ax.set_facecolor(colours[1])
    fig.patch.set_facecolor(colours[2])
    plt.show()
    fig.savefig('Graphs/used_words.png')

commonly_used_words('winter_muse_', 1000)