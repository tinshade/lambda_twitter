import unittest
import json
from lambda_function import lambda_handler
from constants import SAMPLE_TWEET, LOREM_TEXT

class TestDummy(unittest.TestCase):
    
    def test_invalidInput(self):
        payload_short = {"tweet": "A"}
        payload_long = {"tweet": LOREM_TEXT}
        payload_wrong = {"wrong_key": SAMPLE_TWEET}
        results = lambda_handler(event={"body": json.dumps(payload_short)}, context={})
        self.assertEqual(results['statusCode'],400)
        
        results = lambda_handler(event={"body": json.dumps(payload_long)}, context={})
        self.assertEqual(results['statusCode'],400)
        
        results = lambda_handler(event={}, context={})
        self.assertEqual(results['statusCode'],400)

        results = lambda_handler(event={"body": json.dumps(payload_wrong)}, context={})
        self.assertEqual(results['statusCode'],400)
    
    def test_validInput(self):
        payload_og = {"tweet": SAMPLE_TWEET}
        results = lambda_handler(event={"body": json.dumps(payload_og)}, context={})
        if results['statusCode'] != 200:
            print(results)
        self.assertEqual(results['statusCode'],200)

    
if __name__ == '__main__':
    unittest.main()