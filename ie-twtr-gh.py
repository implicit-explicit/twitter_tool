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
        if e.e.code == 429:
            print("Fail: {} API rate limit exceeded".format(e.e.code), file = sys.stderr)
            rate_limit_status = t.application.rate_limit_status()
            time_to_reset_unix = rls.rate_limit_reset
            time_to_reset_asc = _time.asctime(_time.localtime(time_to_reset_unix))
            time_to_wait = int(rls.rate_limit_reset - _time.time()) + 5 # avoid race
            print("Interval limit of {} requests reached, next reset on {}: going to sleep for %i secs".format(rls.rate_limit_limit, time_to_reset_asc, time_to_wait))
            fail.wait(time_to_wait)
            continue
        # print("Rate limit exceeded!", file = sys.stderr)
        # time.sleep(60)