import tweepy
import theSecrets
import os.path
import json

# The system
"""
1. For the first time run tokenrefreshener.py, after that it will be ran every 1 hour and 55 minutes to keep 
the token alive
2. The token is saved to twittertoken.json and it can be used by reading the file
3. Use the token for your app anywhere
"""

# OAuth 2.0 Authorization See the list of scopes (permssions) here ->
# https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code

token_data = ""
with open("twittertoken.json", "r") as f:
    a_token_str = f.read()
    token_data = json.loads(a_token_str)  # Transforms string into a json obj

# Intiliaze with api keys and Oauth 2.0 (Bearer token type)
client = tweepy.Client(token_data["access_token"], theSecrets.twt_api_key, theSecrets.twt_api_key_secret)

# -------- Tweet or do polls --------
# res = client.create_tweet(text="testing twt api", poll_options=["Dope", "Stop it!!!"],
# user_auth=False, poll_duration_minutes=60)

# -------- Returns a variety of information about a single user specified by the requested ID or username. --------
# Such as User id, name, username etc.
# Note: Username starts with a @"text"

res = client.get_user(username="elonmusk", user_auth=False)
# accessing the fetched data from a response obj: res.data.id)
timeline = client.get_users_tweets(res.data.id, exclude=["retweets", "replies"], max_results=5, end_time="2023-01-01T00:20:00.52Z")

i = 1
for tweet in timeline.data:
    print(f"--- TWEET No.{i} ---")
    print(tweet.text.split("\n"))
    print("---------")
    i += 1


