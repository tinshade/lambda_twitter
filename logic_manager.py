import tweepy
import cerberus
from constants import VALIDATE_TWEET, FALLBACK_QUOTE,API_KEY,API_SECRET_KEY,ACCESS_TOKEN,ACCESS_TOKEN_SECRET
import urllib.request
import json


class DummyFunction:
    def __init__(self):
        self.errors = None
        self.validated_data = None
        self.signature = "~ LMBot"
    
    def validate_data(self, payload) -> bool:
        try:
            validator = cerberus.Validator(purge_unknown=True)
            validator.schema = VALIDATE_TWEET
            if validator.validate(payload):
                self.validated_data = validator.document
                return True
            self.errors = validator.errors
            return False
        except Exception as e:
            self.errors = {'error' : str(e)}
            return 
    

    def post_tweet(self) -> dict:
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        tweet = self.validated_data.get("tweet")
        if tweet is not None:
            tweet = f"{tweet}\n{self.signature}"
        try:
            print(tweet)
            api.update_status(status = tweet if tweet is not None else f"{FALLBACK_QUOTE}\n{self.signature}")
            return {"message" : 'Tweet sent successfully!'}
        except Exception as e:
            self.errors = {'error' : str(e)}
            return {"message" : f'Tweet failed!\n{str(e)}'}


class FetchQuotes:
    def __init__(self) -> None:
        self.url = "https://programming-quotes-api.herokuapp.com/quotes/random/"
        self.errors = None
        self.validated_data = None

    def getResponse(self, url) -> dict:
        operUrl = urllib.request.urlopen(url)
        response_data = None
        if(operUrl.getcode()==200):
            data = operUrl.read()
            response_data = json.loads(data)
        else:
            self.errors = {"error" : f"Error receiving data {operUrl.getcode()}"}
        
        return response_data
    
    def driver(self) -> dict:
        url_eng = self.url
        quote_response = self.getResponse(url_eng)
        context = quote_response['en']
        author = quote_response['author']
        quote = context + " -" + author
        quote = {"tweet" : quote}
        response_data = {}
        status_code = 400
        
        if quote:
            dummy_function = DummyFunction()
            if dummy_function.validate_data(quote):
                response_data = dummy_function.post_tweet()
                status_code = 200
            else:
                response_data = dummy_function.errors
            
            return {"message":response_data, "statusCode" : status_code}
        return {"message":"No quotes to tweet!", "statusCode" : 204}