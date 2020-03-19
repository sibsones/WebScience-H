import pymongo
import csv

'''
Export an attribute of tweets to a csv file
Currently setup for hashtags, but could be made modular for other functions
'''

if __name__ == "__main__":
    client = pymongo.MongoClient('127.0.0.1',27017)
    db = client.twitterStreamTest
    tweet_collection = db.tweet_collection
    tweets = tweet_collection.find()
    print("Getting Data")
    data = []
    for tweet in tweets:
        try:
            tags = ""
            for tag in tweet['hashtags']:
                print(tweet['hashtags'])
                if tags == "":
                    tags = tag['text']
                else:
                    tags = tags + " " + tag['text']
            if tags != "":
                data.append(tags)
        except:
            pass

    print(data)
    print("Writing to CSV")
    with open('hashtags.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['hashtags'])
        for entry in data:
            writer.writerow([entry])

    print("Done")