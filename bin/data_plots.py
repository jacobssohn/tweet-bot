import random

import tweepy
from matplotlib import pyplot as plt
from nltk.corpus import stopwords as sw

from bin.credentials import MorningYawn


def commonly_used_words(user: str, number_of_tweets: int = 100):

    auth = tweepy.OAuthHandler(MorningYawn.consumer_key, MorningYawn.consumer_secret)
    auth.set_access_token(MorningYawn.access_token, MorningYawn.access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    stopwords = sw.words('english') + sw.words('spanish')
    tweets_text = []

    for tweet in tweepy.Cursor(api.user_timeline,id=user).items(number_of_tweets):
        tweets_text.append(tweet.text)

    most_used_words = []
    for tweet in tweets_text:
        most_used_words += tweet.split(' ')
    most_used_words_cleared = []
    for word in most_used_words:
        word = word.strip()
        if word == '' or len(word) < 3:
            continue
        if word[-1] == '.' or word[-1] == ',':
            word = word[:-1]
        if word[0] == '@':
            continue
        if word in stopwords or 'RT' in word or  '.' in word or '#' in word:
            continue
        word = word.lower()
        if "í" in word:
            word = list(word)
            for i in range(len(word)-1):
                if word[i] == 'í':
                    word[i] = 'i'
            word = "".join(word)
        most_used_words_cleared.append(word)

    words_dict = {}
    for word in most_used_words_cleared:
        if word in words_dict.keys():
            words_dict[word] += 1
        else:
            words_dict[word] = 1

    words_dict = dict(sorted(words_dict.items(), key=lambda item: item[1], reverse=True))

    # df = pd.DataFrame.from_dict(words_dict, orient='index')
    sum_check = 0
    remaining_sum = 0
    dict_segregated = {}
    iter = 1
    for key, value in words_dict.items():
        if iter <= 10:
            sum_check += value
            dict_segregated[key] = value
            iter += 1
        else:
            remaining_sum += value

    #dict_segregated['Remaining\n words'] = remaining_sum # uncomment this to see the amount of uses of the remaining words


    fig, ax = plt.subplots()
    words_ax = [key for key, value in dict_segregated.items()]
    uses = [value for key, value in dict_segregated.items()]
    colours = ['turquoise', 'bisque', 'palegreen', 'orchid', 'peru', 'pink', 'lightcyan', 'gold', 'salmon']
    colours = (colours.pop(random.randint(0, len(colours) - 1)), colours.pop(random.randint(0, len(colours) - 2)),
               colours.pop(random.randint(0, len(colours) - 3)))
    ax.bar(words_ax, uses, color=colours[0])
    plt.xticks(rotation=-20)
    plt.ylabel('Number of uses')
    plt.title(f"Most popular words by use in {user}'s tweets")
    ax.set_facecolor(colours[1])
    fig.patch.set_facecolor(colours[2])
    plt.show()
    fig.savefig('Graphs/used_words.png')
    return 'Graphs/used_words.png'


