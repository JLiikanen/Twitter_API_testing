import tweepy
import json
import os.path
import theSecrets

# ALWAYS RUN THIS FIRST, AND THEN EVERY 1 HOUR AND 55 MINUTES.

# ------------ AUTOMATING THE AUTHENTICATION WITH THE REFRESH TOKEN ---------------
class MyOAuth2UserHandler(tweepy.OAuth2UserHandler):

    def refresh_token(self, refresh_token):
        new_token = super().refresh_token(
            "https://api.twitter.com/2/oauth2/token",
            refresh_token=refresh_token,
            body=f"grant_type=refresh_token&client_id={self.client_id}",
        )
        return new_token


# Using a raw string
tokenJsonFilePath = r"C:\Users\jacqu\Tiedostoja\Koodaus-harjoitukset\PdfReport\Twitter API\twittertoken.json"
oauth2_user_handler = None


# Once refreshed, the old token is no longer valid.
# THIS CODE IS INEFFIECNT AS IT REFRESH THE CODE EVERYTIME IT IS RUN

def authenticator():
    if os.path.isfile(tokenJsonFilePath):
        # if the file exsists, it means we already have a token and use the refresh token instead
        a_token = ""
        with open("twittertoken.json", "r") as f:
            a_token_str = f.read()
            token_data = json.loads(a_token_str)  # Transforms string into a json obj

        auth2 = MyOAuth2UserHandler(
            client_id=theSecrets.client_id,
            scope=["tweet.read", "offline.access", "users.read", "tweet.write"],
            redirect_uri="https://twitter.com/home",
            client_secret=theSecrets.client_secret
        )

        new_token = auth2.refresh_token(token_data["refresh_token"])

        with open("twittertoken.json", "w") as f:  # updates the existing token with a refreshed one.
            jsonstr = json.dumps(new_token)
            f.write(jsonstr)

        return new_token, True
    else:
        # y default, the access token you create through the Authorization Code Flow with PKCE,
        # will only stay valid for two hours,
        # unless you’ve used the offline.access scope, then a refresh_token will be issued.

        # Then, you can get the authorization URL:
        # This can be used to have a user authenticate your app.
        # Once they’ve done so, they’ll be redirected to the Callback / Redirect URI / URL you provided.
        # You’ll need to pass that authorization response URL to fetch the access token:

        oauth2 = tweepy.OAuth2UserHandler(
            client_id=theSecrets.client_id,
            scope=["tweet.read", "offline.access", "users.read", "tweet.write"],
            redirect_uri="https://twitter.com/home",
            client_secret=theSecrets.client_secret
        )

        print(oauth2.get_authorization_url())
        authresponse = input(
            "Pass the authorization response URL: ")  # copy the url you get when you give the permssions.
        # IMPORTANT: You will have to exchange it with an access token within 30 seconds, or the auth_code will expire.

        # access_token returns a dictionary with keys: token_type, expires_in, access_token, scope, refresh_token,
        # expires_at
        access_token = oauth2.fetch_token(
            authresponse
        )

        # Write the token to memory
        with open("twittertoken.json", "w") as f:  # open creates a file automatically.
            jsonstr = json.dumps(access_token)
            f.write(jsonstr)

        return access_token, True


access_token = authenticator()

print(access_token[1])
