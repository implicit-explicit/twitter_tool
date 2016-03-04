import sys
import time
from twitter import *


# Keys, tokens and secrets
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# OAuthHandler
t = Twitter(auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

target_name = sys.argv[1]
count = 200
cursor = -1

target_info = t.users.show(screen_name=target_name)
real_name = target_info["name"]
followers_count = target_info["followers_count"]
print(real_name, file = sys.stderr)
print(followers_count, file = sys.stderr)

while cursor != 0:
    try:
        target = t.followers.list(screen_name = target_name, count = count, cursor = cursor)
        followers = target["users"]
        # print(cursor, file = sys.stderr)
        # print(len(followers), file = sys.stderr)

        for follower in followers:
            print("{}, {}".format(follower["screen_name"], follower["followers_count"]))

        cursor = target["next_cursor"]
    except TwitterHTTPError as e:
        print("Rate limit exceeded!", file = sys.stderr)
        time.sleep(60)