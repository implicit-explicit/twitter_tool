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
target = input("Enter Twitter handle without @: ")
user = api.get_user(target)

print("User name: ", user.name)
print("User followers count: ", user.followers_count)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("Rate Limit reached! Exiting program.")
            sys.exit(1)

for follower in limit_handled(tweepy.Cursor(api.followers, target).items()):
    if follower.followers_count < 100:
        print(follower.name, "|", follower.screen_name, "|" , follower.followers_count)
        with open("results.txt", "w") as f:
            for name in follower.name:
                f.write(follower.name)