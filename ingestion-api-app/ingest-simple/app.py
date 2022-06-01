import boto3
import os
from datetime import datetime
import io
import uuid
import json as j
from botocore.exceptions import ClientError


def lambda_handler(event, context):

    s3_errors = os.environ['S3ERRORS']

    s3_client = boto3.client('s3')
    now = datetime.now()
    dt_string = now.strftime('%Y%m%d%H%M%S%f')[:-3]

    try:

        request_type = event['pathParameters']['type']

        if request_type == 'Simple':
            to_return = ReturnObjectSimple()
        elif request_type == 'Medium':
            to_return = ReturnObjectMedium()
        elif request_type == 'Complex':
            to_return = ReturnObjectComplex()
        else:
            to_return = {
                'type':'invalid'
            }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',  # Allow from anywhere
                'Access-Control-Allow-Methods': 'GET, OPTIONS'  # Allow only GET, POST request
            },
            'body': j.dumps(to_return
                            )
        }

    except Exception as e:
        b = bytes(str(e)+'\n'+(str(event)), 'utf-8')
        f = io.BytesIO(b)
        s3_client.upload_fileobj(
            f, s3_errors, f'ingestapi_{dt_string}_error.log')
        return {
            'statusCode': 500,
            'body': j.dumps({
                'result': 'failure',
                'note': 'check s3 error log'
            })
        }


def ReturnObjectSimple():

    dict_to_return = {
        'policyid': '1234567A',
        'inception date': '2021-01-01',
        'expiry date': '2021-12-31',
        'status': 'live',
        'premium': 500000,
        'brokerage': '1545',
        'tax': '5%'
    }

    return dict_to_return
    
def ReturnObjectMedium():

    dict_to_return = {
        'policyid': '1234567A',
        'inception date': '2021-01-01',
        'expiry date': '2021-12-31',
        'status': 'live',
        'financials': {
            'premium': 500000,
            'brokerage': '1545',
            'tax': '5%'}
    }

    return dict_to_return

def ReturnObjectComplex():

    dict_to_return = {
        'policyid': '1234567A',
        'inception date': '2021-01-01',
        'expiry date': '2021-12-31',
        'status': 'live',
        'financials': [
            {
            'instalment_num':1,
            'premium': 100000,
            'brokerage': '545',
            'tax': '5%'},            
            {
            'instalment_num':2,
            'premium': 100000,
            'brokerage': '545',
            'tax': '5%'}
            ]
    }

    return dict_to_return
