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


def read_auth_file(filename):
    """ Reads our auth_keys file """
    try:
        with open(filename, 'r') as file:
            read_authentication_keys = []
            for line in file:
                read_authentication_keys.append(line.strip())
        return read_authentication_keys
    except FileNotFoundError:
        print("The 'auth_keys' file has not been found! Make sure you have one!")
        sys.exit(1)


def get_auth_keys():
    """ Gets the authorisation keys and tries for a bearer token w/ oauth2_dance()  """
    filename = "auth_keys"
    authorisation_keys = read_auth_file(filename)
    return authorisation_keys


def main():
    target_name = target_check()
    auth_keys = get_auth_keys()
    # OAuthHandler
    twitter = Twitter(auth=OAuth(auth_keys[2], auth_keys[3], auth_keys[0], auth_keys[1]))
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
