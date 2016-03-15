import sys
import time
import urllib.request

from twitter import *


def target_check():
    """ First check if a target has been given """
    try:
        if len(sys.argv[1]) > 0:
            return sys.argv[1]
    except IndexError:
        print("No target given! Please call with a target!")
        sys.exit(2)


def main():
    target_name = target_check()
    # Keys, tokens and secrets
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    # OAuthHandler
    twitter = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))
    count = 200
    cursor = -1

    target_info = twitter.users.show(screen_name=target_name)
    real_name = target_info["name"]
    followers_count = target_info["followers_count"]
    print(real_name, file=sys.stderr)
    print(followers_count, file=sys.stderr)

    while cursor != 0:
        try:
            target = twitter.followers.list(screen_name=target_name, count=count, cursor=cursor)
            followers = target["users"]
            # print(cursor, file = sys.stderr)
            # print(len(followers), file = sys.stderr)

            for follower in followers:
                print("{}, {}".format(follower["screen_name"], follower["followers_count"]))
            cursor = target["next_cursor"]

        except TwitterHTTPError as e:
            if e.e.code == 429:
                print("Fail: {} API rate limit exceeded".format(e.e.code), file=sys.stderr)
                rate_limit_status = twitter.application.rate_limit_status()
                time_to_reset_unix = rate_limit_status.rate_limit_reset
                time_to_reset_asc = time.asctime(time.localtime(time_to_reset_unix))
                time_to_wait = int(rate_limit_status.rate_limit_reset - time.time()) + 5  # avoid race
                print("Interval limit of {} requests reached, next reset on {}: going to sleep for {} secs".format(
                    rate_limit_status.rate_limit_limit, time_to_reset_asc, time_to_wait), file=sys.stderr)
                time.sleep(time_to_wait)
                continue
        except urllib.request.URLError as e:
            pass
            # print("Rate limit exceeded!", file = sys.stderr)
            # time.sleep(60)


if __name__ == '__main__':
    main()
