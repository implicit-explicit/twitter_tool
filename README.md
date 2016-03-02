# Implicit-Explicit Twitter Growth Hacking Tool

## Requirements
Python 3.5.1
Tweepy

## Usage

```
pip tweepy
py ie-twtr-gh.py
```
Follow on screen instructions

## Limitations
Currently has hard coded Twitter app values from my Twitter account (@apleasantview) set up.
It is advised to replace these with an Implicit-Explicit app.

Due to the Twitter API rate limit you may want to limit the numbers to fetch on lines 29 - 30.
Changed values example:
```
29. for follower in limit_handled(tweepy.Cursor(api.followers, target).items(15)):
30.    if follower.followers_count > 500:
31.        print(follower.name + " | " + follower.screen_name + " | " , follower.followers_count)
```

## TODO
Have it all nicely sorted :/

## ERRATUM
Just notice that outputting to txt did not work :/
