import json
import boto3
from datetime import datetime as dt


def lambda_handler(event, context):
    ''''
    Expected event format:
    {
        body:  {
            temperature: 21.2,
            humidity: 42,
            sector: north
        }
    }
    '''

    def assign_fire_risk(item):
        '''
        Calcule fire risk depends of temperature
        :param item:
        :return: json item with fire-risk field
        '''

        if item['temperature'] >= 30:
            item['fire-risk'] = 'high'
        elif item['temperature'] >= 20:
            item['fire-risk'] = 'medium'
        else:
            item['fire-risk'] = 'low'
        return item

    # Create DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # DynamoDB table
    table = dynamodb.Table('climatology')

    # Get data from event and add timestamp
    item = json.loads(event['body'])
    item['timestamp_update'] = dt.now()

    # Get fire risk depends of temperature
    item = assign_fire_risk(item)

    # Insert item in climatology table of dynamoDB
    response = table.put_item(Item=item)

    # Logging response in cloudWatch
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Item inserted successfully: {item}")
    else:
        print(f"Error inserting item: {response['Error']}")

    end_timestamp = dt.now()
    print(f'End of execution: {end_timestamp}')

