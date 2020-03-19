import pymongo
import operator

# This program takes advantage of tweet.json's "mentioned_users" attribute, providing
# convinient links between users

def mentions(tweets_list):
    usermentions = {}
    tweets = tweets_list.find()
    most_mentioned_times = 0
    most_mentioned_user = None

    # Users mentioning eachother added to a dictionary
    # .i.e. - {RealDonaldTrump: {BorisJohnson: 3, BarackObama: 10}}
    for tweet in tweets:
        if len(tweet['mentions']) != 0:
            if not tweet['username'] in usermentions:
                usermentions[tweet['username']] = {}
        else:
            continue

        for mentioned in tweet["mentions"]:
            if mentioned["screen_name"] in usermentions[tweet["username"]]:
                usermentions[tweet["username"]][mentioned["screen_name"]] += 1
            else:
                usermentions[tweet["username"]][mentioned["screen_name"]] = 1

    # finding the most mentioned about user
    for user in usermentions.keys():
        if len(usermentions[user]) > most_mentioned_times:
            most_mentioned_times = len(usermentions[user])
            most_mentioned_user = user

    print(most_mentioned_user, most_mentioned_times)
    #print(usermentions)
    return usermentions

def hashtag_groups(tweets_list):
    hashtags = {}
    tweets = tweets_list.find()
    biggest_hashtag_group = None

    # Grouping of hashtags that occur together frequently
    
    for tweet in tweets:
        if len(tweet["hashtags"]) != 0:
            for hashtag in tweet["hashtags"]:

                if hashtag["text"] not in hashtags:
                    hashtags[hashtag["text"]] = []

                for hashtag2 in tweet["hashtags"]:
                    if (
                        hashtag2["text"] != hashtag["text"]
                        and hashtag2["text"] not in hashtags[hashtag["text"]]
                    ):
                        hashtags[hashtag["text"]].append(hashtag2["text"])
        else:
            continue
    
    # Printing the largest groups of hashtags occuring together
    count = 0
    for hashtag in hashtags.keys():
        size_hashtag = len(hashtags[hashtag])
        if size_hashtag > count:
            biggest_hashtag_group = hashtag
            count = size_hashtag

    print(hashtags[biggest_hashtag_group])
    return hashtags

def ties(usermentions):
    '''
    tie/link between nodes
    • This means if there is a link between nodes, then there is a tie/link
    • Tie is when two users connect
    '''
    ties = 0
    for user in usermentions:
        for mentioned_user in usermentions[user]:
            if mentioned_user == user:
                continue
            if (
                mentioned_user in usermentions
                and user in usermentions[mentioned_user]
            ):
                ties += 1
    print("Total # of Ties: ",ties)
    return ties

def triads(usermentions):
    '''
    Triad: a group of 3 users – node i, j and u forming a path of length 2 (i. e, node i is connected to node j; and
    node j is connected to node u); when node u is also connected to node i then the path is closed; forming a
    loop of length 3 or a triangle.
    '''
    triads = 0
    for user in usermentions:
        for mentioned_user in usermentions[user]:
            if mentioned_user != user and check(
                mentioned_user, user, usermentions
            ):
                for mentioned_user2 in usermentions[user]:
                    if (
                        mentioned_user2 != mentioned_user
                        and user != mentioned_user
                        and check(
                            user, mentioned_user2, usermentions
                        )
                    ):
                        if check(
                            mentioned_user, mentioned_user2, usermentions
                        ) and check(
                            mentioned_user2, mentioned_user, usermentions
                        ):
                            triads += 1

    print("Total # of Triads: ",triads)
    return triads

def check(user1, user2, mentions):
    # check if 2 users are in the same mentioned user dictionary
    if user1 not in mentions:
        return False
    if user2 in mentions[user1]:
        return True
    else:
        return False

if __name__ == "__main__":
    client = pymongo.MongoClient('127.0.0.1',27017)
    db = client.twitterStreamTest
    tweet_collection = db.tweet_collection
    mentions_dict = mentions(tweet_collection)
    hashtags = hashtag_groups(tweet_collection)
    ties(mentions_dict)
    triads(mentions_dict)
