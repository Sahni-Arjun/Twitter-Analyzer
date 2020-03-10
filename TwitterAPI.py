
from pymongo import MongoClient
import tweepy

#authentication keys
CONSUMER_KEY="0FMVtFqsDVkZWZlrtSY6bzqQx"
CONSUMER_SECRET="OhYZ4wtSZTAvVNdhPGsW2A9wgKTFI9lVqhyJH6Ea7uKv3povUm"
OAUTH_TOKEN="1235355681496199169-AIzv98q9W8RLvlSLIoZpRteioRjeto"
OAUTH_TOKEN_SECRET="fnfKKlSSZttlMHf55dDqjunW9PohN4dSIgAEZPgfJaojSQ"

# Creating the authentication object
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# Creating the API object while passing in auth information
api = tweepy.API(auth)

#mongo client
client = MongoClient("mongodb+srv://test:Test123@cluster0-6occj.gcp.mongodb.net/test?retryWrites=true&w=majority")

#get the database
Users = client.get_database('Twitter_Users')

#get the collectionx
feeds = Users.Twitter_Feeds

#not needed but aim is to sort in ascending order
# feeds.create_index([("id",pymongo.ASCENDING)],unique=True)
name = "JustinTrudeau"

#list of current account info
tweets = feeds.find_one({"name":name})
print(len(tweets[name]))

#find total number of tweets

user = api.get_user(name)
total_tweets = api.get_user(name).statuses_count
print(total_tweets)

# find if current id exists in database to update curr_num of tweets
fail_safe = feeds.count_documents({"name": name})
#print(fail_safe)

curr_tweets = len(tweets[name]) if fail_safe != 0 else 0
#print(curr_tweets)

#find number of new tweets
tweetCount = total_tweets-curr_tweets

# collection of new tweets
results = api.user_timeline(id=name, count=tweetCount)

search_results = {'name':name}

#adding tweet results
for tweet in results:
   if name not in search_results:
       search_results[name] = []
   if tweet.text not in search_results[name]:
       search_results[name].append(tweet.text)

if fail_safe != 0: #already exists
    for i in range(curr_tweets):
        search_results[name].append(tweets[name][i])

#print(search_results)

if fail_safe != 0: #already exists in database
    feeds.delete_many({"name": name})

try:
    feeds.insert_one(search_results)
except:
    pass

'''
#tweet_cursor = feeds.find()


#for document in tweet_cursor:
   #for i in range(len(search_results[name])):
      #if(name in document):
         #print('-----')
         #print('name:-',name)
        # print('text:-',document[name][i])
'''
