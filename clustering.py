import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

'''
This program takes a while to run on larger datasets
But it's worth it!
'''

def getTweetText(tweet_collection):
    screennames,hashtag,text = [],[],[]
    alldata = tweet_collection.find()
    for tweet in alldata:
        #print(str(tweet['username']).lower())
        tlower = str(tweet['username']).lower()
        htlower = str(tweet['hashtags']).lower()
        tlower = str(tweet['text']).lower()
        screennames.append(tlower)
        hashtag.append(htlower)
        text.append(tlower)

    return screennames,hashtag,text
    
def cluster(screen_names,hashtags,texts):
    vectorizer = TfidfVectorizer(stop_words='english')
    k = 8

    vec_screen_names = vectorizer.fit_transform(screen_names)
    vec_hashtags = vectorizer.fit_transform(hashtags)
    vec_texts = vectorizer.fit_transform(texts)

    screennamesK = KMeans(n_clusters=k,init='k-means++',max_iter=100,n_init=1)
    screennamesK.fit(vec_screen_names)

    hashtagsK = KMeans(n_clusters=k,init='k-means++',max_iter=100,n_init=1)
    hashtagsK.fit(vec_hashtags)

    textK = KMeans(n_clusters=k,init='k-means++',max_iter=100,n_init=1)
    textK.fit(vec_texts)

    return vectorizer,screennamesK,hashtagsK,textK

def topResult(vectorizer,group):
    k = 8
    centroids = group.cluster_centers_.argsort()[:,::-1]
    text = vectorizer.get_feature_names()
    for centre in range(k):
        print ("CLUSTER %d:" % centre)
        for i in centroids[centre, :5]:
            print (' %s' % text[i])

if __name__ == "__main__":
    client = pymongo.MongoClient('127.0.0.1',27017)
    db = client.twitterStreamTest
    tweet_collection = db.tweet_collection

    sc,ht,t = getTweetText(tweet_collection)
    vec,scK,htK,tK = cluster(sc,ht,t)

    print("This program takes a while to run with large amounts of data.")

    print("++++ USERNAME CLUSTERS ++++")
    topResult(vec,scK)
    print("++++ HASHTAG CLUSTERS ++++")
    topResult(vec,htK)
    print("++++ TEXT CLUSTERS ++++")
    topResult(vec,tK)


