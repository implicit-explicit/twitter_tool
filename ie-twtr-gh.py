import sys
import time
from twitter import *
# import win_unicode_console

# win_unicode_console.enable()

# Keys, tokens and secrets
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# OAuthHandler
t = Twitter(auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

target_name = sys.argv[1]
target_count = 200
target_cursor = -1

target_info = t.users.show(screen_name=target_name)
target_sn = target_info["name"]
target_fc = target_info["followers_count"]
target = t.followers.list(screen_name = target_name, count = target_count, target = target_cursor)

while target_cursor != 0:
    try:
        print(target_sn)
        print(target_fc)
        followers = target["users"]
        for follower in followers:
            print("{}, {}".format(follower["screen_name"], follower["followers_count"]))
        target_cursor = target["next_cursor"]
        print(target_cursor)        
    except TwitterHTTPError as e:
        print("Rate limit exceeded!")
        sys.exit(1)
