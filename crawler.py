import pymongo
import json
import twitter
import tweepy
import twitter_credentials as tc

def trending_search(api):
    """
    Top trends from twitter (UK)
    """
    trends = api.trends_place(23424975)[0][
        "trends"
    ]  # The integer is the location of the UK
    trends_list = [trend["name"] for trend in trends]
    print(trends_list[:10])
    return(trends_list[:10])

class Listener(tweepy.StreamListener):
    def on_data(self,raw_data):
        self.process_data(raw_data)
        print("tweet")
        return True

    def process_data(self,raw_data):
        try:
            tweet = json.loads(raw_data)
            userid = tweet['id']
            user = tweet['user']['screen_name']
            text = tweet['text']
            hashtags = tweet['entities']['hashtags']
            language = tweet['lang']
            mentions = tweet['entities']['user_mentions']
            reply_to = tweet['in_reply_to_screen_name'] #empty = Null
            quote = tweet['is_quote_status'] #empty = False
            retweeted = tweet['retweeted'] #empty = False

            #created = datetime.datetime.striptime(time,  '%a %b %d %H:%M:%S +0000 %Y')
            tweetFormat = {'id':userid, 'username':user, 'text':text, 'hashtags':hashtags, 'language':language, 
            'mentions':mentions,'reply_to':reply_to,'quote':quote,'retweeted':retweeted}
            print(tweetFormat)
            tweet_collection.insert(tweetFormat)

        except BaseException:
            pass
        
    def on_error(self,status_code):
        if status_code == 420:
            return False
        if status_code == 11000:
            print("dup")    

class TweetStream():
    def __init__(self,auth,listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start_filtered(self,keywords):
        self.stream.filter(track=keywords,languages=['en'])

    def start_unfiltered(self):
        self.stream.sample(languages=['en'])

if __name__=="__main__":
    client = pymongo.MongoClient('127.0.0.1',27017)
    db = client.twitterStreamTest
    tweet_collection = db.tweet_collection
    tweet_collection.create_index([("id",pymongo.ASCENDING)],unique=True, dropDups=True)
    listener = Listener()
    
    auth = tweepy.OAuthHandler(tc.CONSUMER_KEY,tc.CONSUMER_SECRET)
    auth.set_access_token(tc.OAUTH_TOKEN,tc.OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)

    keywords = trending_search(api)
    stream = TweetStream(auth,listener)
    choice = False

    print("This crawler is restricted to tweets with language 'en'")
    while choice == False:
        try:
            options = input("Crawl trending topic tweets? (Y/N): ")
            if options.lower() == "y":
                stream.start_filtered(keywords)
                choice == True
            elif options.lower() == "n":
                stream.start_unfiltered()
                choice == True
        except ValueError:
            print("Invalid Input")

    print("starting")
    