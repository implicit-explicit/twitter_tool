import sys
import time
import tweepy

# Keys, tokens and secrets
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Tweepy OAuthHandler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Variables
target = sys.argv[1]
user = api.get_user(target)

print("User name: ", user.name)
print("User followers count: ", user.followers_count)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("Rate Limit reached! Sleeping!")
            time.sleep(15 * 60)
            

for follower in limit_handled(tweepy.Cursor(api.followers, target).items()):
    print("{}, {}, {}".format(target, follower.screen_name, follower.followers_count))