import json
from logic_manager import FetchQuotes

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
    response_data = None
    
    post_quote = FetchQuotes()
    try:
        '''
        validations = post_quote.validate_data(body)
        if validations:
            response_data = post_quote.driver()['message']
            if post_quote.errors:
                response_data = post_quote.errors
            else:
                status_code = 200
        else:
            response_data = post_quote.errors
        '''

        response_data = post_quote.driver()['message']
        print(response_data)
        if post_quote.errors:
            response_data = post_quote.errors
        else:
            status_code = 200


    except Exception as e:
        response_data = {
            'error': f'Something went wrong!\nTRACEBACK\n{str(e)}'
        }
    
    return prepare_payload(status_code=status_code, response_data=response_data, aws_request_id=aws_request_id)
