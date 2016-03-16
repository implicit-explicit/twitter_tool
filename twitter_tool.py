import os
import sys
import time
import urllib.error

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


def get_a_bearer_token(consumer_key, consumer_secret):
    """ The bearer token enables us to do Application only request and up our rate limit some """
    bearer_token_file = "bearer_token"
    if not os.path.isfile(bearer_token_file):
        oauth2_dance(consumer_key, consumer_secret, bearer_token_file)
    return


def target_info(target_name):
    """ Prints out basic info about our target """
    twitter = main_twitter_api_call()
    target_information = twitter.users.show(screen_name=target_name)
    real_name = target_information["name"]
    followers_count = target_information["followers_count"]
    print("Target: {0} - Followers: {1}".format(real_name, followers_count), file=sys.stderr)
    return


def get_target_followers(target_name):
    """ Gets followers and their followers count from our target """
    print("Getting requested data.", file=sys.stderr)
    twitter = main_twitter_api_call()
    count = 200
    cursor = -1
    while cursor != 0:
        try:
            target = twitter.followers.list(
                screen_name=target_name, count=count, cursor=cursor, skip_status="true", include_user_entities="false")
            followers = target["users"]
            for follower in followers:
                print("{0}, {1}, {2}".format(target_name, follower["screen_name"], follower["followers_count"]))
            cursor = target["next_cursor"]
        except TwitterHTTPError as e:
            if e.e.code == 429:
                rate_limit_status = twitter.application.rate_limit_status()
                time_to_wait = int(rate_limit_status.rate_limit_reset - time.time()) + 5  # avoid race
                print("Hit rate limit. Waiting {} secs.".format(time_to_wait), file=sys.stderr)
                time.sleep(time_to_wait)
                print("Getting requested data.", file=sys.stderr)
                continue
    return


def main_twitter_api_call():
    """ This the main Twitter API call via the Python Twitter Tools """
    bearer_token = read_bearer_token_file("bearer_token")
    twitter = Twitter(auth=OAuth2(bearer_token=bearer_token))
    return twitter


def format_error(exception, details):
    """ Error formatting function """
    print("{}: {}".format(exception, details), file=sys.stderr)
    return


def main():
    target_name = target_check()
    auth_keys = get_auth_keys()
    try:
        get_a_bearer_token(consumer_key=auth_keys[0], consumer_secret=auth_keys[1])
        target_info(target_name)
        get_target_followers(target_name)  # The nitty gritty
    except TwitterHTTPError as e:
        format_error(type(e).__name__, e)
    except urllib.error.HTTPError as e:
        format_error(type(e).__name__, e)
    except urllib.error.URLError as e:
        format_error(type(e).__name__, e)
    except KeyboardInterrupt as e:
        format_error(type(e).__name__, "Program halted by user.")
    else:
        print("Done.", file=sys.stderr)


if __name__ == '__main__':
    main()
