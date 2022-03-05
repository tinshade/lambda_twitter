import json
from logic_manager import DummyFunction

def prepare_payload(status_code, response_data, aws_request_id):
    headers = {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Headers' : 'Content-Type',
        'Access-Control-Allow-Methods' : 'OPTIONS, POST, GET',
    }
    response = {
        'statusCode' : status_code,
        'body': json.dumps(response_data),
        'headers': headers
    }
    return response


def lambda_handler(event, context):
    aws_request_id = context.aws_request_id if context else None
    status_code = 400
    body = {}
    response_data = None
    try:
        body = json.loads(event.get('body', {}))
    except Exception as e:
        response_data = {
            'error': 'Found invalid keys'
        }
        return prepare_payload(status_code=status_code, response_data=response_data, aws_request_id=aws_request_id)
    
    dummy_fucntion = DummyFunction()
    #session = dummy_fucntion.session
    try:
        validations = dummy_fucntion.validate_data(body)
        if validations:
            response_data = dummy_fucntion.post_tweet()
            if dummy_fucntion.errors:
                response_data = dummy_fucntion.errors
            else:
                status_code = 200
        else:
            response_data = dummy_fucntion.errors

    except Exception as e:
        # session.rollback()
        response_data = {
            'error': f'Something went wrong!\nTRACEBACK\n{str(e)}'
        }
    finally:
        pass
        #session.close()
    
    return prepare_payload(status_code=status_code, response_data=response_data, aws_request_id=aws_request_id)
