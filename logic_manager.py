import tweepy
import cerberus
from constants import VALIDATE_TWEET, FALLBACK_QUOTE,API_KEY,API_SECRET_KEY,ACCESS_TOKEN,ACCESS_TOKEN_SECRET



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
            api.update_status(status = tweet if tweet is not None else f"{FALLBACK_QUOTE}\n{self.signature}")
            return {"message" : 'Tweet sent successfully!'}
        except Exception as e:
            self.errors = {'error' : str(e)}
            return {"message" : f'Tweet failed!\n{str(e)}'}






